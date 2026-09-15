#!/usr/bin/env python3
"""
Figma'dan eksport qilingan freym SVG'sidan 1:1 sayt yig'adi.

  python3 tools/svg2site.py "Site 1.svg" example/d

Ishlash tartibi
  * rasm to'ldirgan <rect>  -> <img> (3x WebP, Figma kesimi bilan)
  * qolgan hamma vektor+matn -> sahifa ustidagi SVG qatlamlar (z-tartib saqlanadi)
  * matn SVG ichida qoladi: Figma bergan bazaviy chiziq (x/y) aynan takrorlanadi
  * litsenziyali shriftlar (HelveticaNeue, Gilroy) bepul analogga almashtiriladi
"""
import base64, hashlib, io, os, re, subprocess, sys, copy
import xml.etree.ElementTree as ET
from PIL import Image

SVG='http://www.w3.org/2000/svg'; XLINK='http://www.w3.org/1999/xlink'
ET.register_namespace('',SVG); ET.register_namespace('xlink',XLINK)
Q=lambda t:'{%s}%s'%(SVG,t)
loc=lambda e:e.tag.split('}')[-1]
SCALE=2                       # rasm eksport masshtabi
AVIF_Q=58                     # AVIF sifati (58 ~ WebP q88 ko'rinishi, yarmi hajm)

# litsenziyali shrift -> bepul analog (kenglik bo'yicha tanlangan)
FONT_SUB={
 'HelveticaNeue':'Arimo,Helvetica Neue,Helvetica,Arial,sans-serif',
 'Helvetica Neue':'Arimo,Helvetica Neue,Helvetica,Arial,sans-serif',
 'Gilroy':'Urbanist,Poppins,sans-serif',
}
# Google Fonts'dan yuklanadiganlar
WEB_FONTS={'Antonio':'Antonio:wght@400;700','Poppins':'Poppins:wght@400;500;600;700',
 'Mulish':'Mulish:wght@400;600;700','Bebas Neue':'Bebas+Neue','Sora':'Sora:wght@400;500;600',
 'Montserrat':'Montserrat:wght@400;600;700','Big Shoulders Display':'Big+Shoulders+Display:wght@400;700',
 'HelveticaNeue':'Arimo:wght@400;700','Gilroy':'Urbanist:wght@400;600;700'}

def shade(hex_color,k):
    """#RRGGBB ni k marta qoraytiradi (k<1) yoki oqartiradi (k>1)."""
    c=hex_color.lstrip('#')
    r,g,b=(int(c[i:i+2],16) for i in (0,2,4))
    f=lambda v:max(0,min(255,round(v*k)))
    return '#%02X%02X%02X'%(f(r),f(g),f(b))

def parse_matrix(s):
    if not s: return (1,0,0,1,0,0)
    m=re.match(r'matrix\(([-\d.eE ,]+)\)',s)
    if m:
        v=[float(x) for x in re.split('[ ,]+',m.group(1).strip())]
        return tuple(v[:6])
    m=re.match(r'scale\(([-\d.eE]+)[ ,]*([-\d.eE]*)\)',s)
    if m:
        a=float(m.group(1)); d=float(m.group(2)) if m.group(2) else a
        return (a,0,0,d,0,0)
    m=re.match(r'translate\(([-\d.eE]+)[ ,]*([-\d.eE]*)\)',s)
    if m: return (1,0,0,1,float(m.group(1)),float(m.group(2) or 0))
    return (1,0,0,1,0,0)

def pad_for_box(im,box):
    """Kesim qutisi rasm chegarasidan chiqsa — shaffof hoshiya qo'shadi."""
    L,T,R,B=box
    px0=max(0,int(-L)+1) if L<0 else 0
    py0=max(0,int(-T)+1) if T<0 else 0
    px1=max(0,int(R-im.width)+1) if R>im.width else 0
    py1=max(0,int(B-im.height)+1) if B>im.height else 0
    if not (px0 or py0 or px1 or py1): return im,box
    # xavfsizlik: noto'g'ri transform tufayli ulkan tuval ajratilmasin
    if (im.width+px0+px1)*(im.height+py0+py1) > 80_000_000:
        raise SystemExit('pad_for_box: kesim qutisi haddan tashqari katta %r '
                         '(rasm %dx%d) — transform noto\'g\'ri o\'qilgan'
                         % ([round(v,1) for v in box],im.width,im.height))
    new=Image.new('RGBA',(im.width+px0+px1,im.height+py0+py1),(0,0,0,0))
    new.paste(im,(px0,py0))
    return new,(L+px0,T+py0,R+px0,B+py0)

NUM=re.compile(r'[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?')
def path_bbox(d):
    """Path'ning tayanch nuqtalari bo'yicha bbox — burchak radiusli
    to'rtburchak uchun aniq (ekstremumlar egri uchlarida yotadi)."""
    toks=re.findall(r'[A-Za-z]|'+NUM.pattern,d or '')
    xs=[];ys=[];cx=cy=sx=sy=0.0;cmd=None;i=0
    def num():
        nonlocal i
        v=float(toks[i]); i+=1; return v
    while i<len(toks):
        t=toks[i]
        if re.match(r'[A-Za-z]',t): cmd=t; i+=1; continue
        if cmd is None: i+=1; continue
        c=cmd.upper(); rel=cmd.islower()
        if c=='M' or c=='L' or c=='T':
            x=num(); y=num()
            cx,cy=(cx+x,cy+y) if rel else (x,y)
            if c=='M': sx,sy=cx,cy; cmd='l' if rel else 'L'
        elif c=='H':
            x=num(); cx=cx+x if rel else x
        elif c=='V':
            y=num(); cy=cy+y if rel else y
        elif c=='C':
            num();num();num();num();x=num();y=num()
            cx,cy=(cx+x,cy+y) if rel else (x,y)
        elif c in 'SQ':
            num();num();x=num();y=num()
            cx,cy=(cx+x,cy+y) if rel else (x,y)
        elif c=='A':
            num();num();num();num();num();x=num();y=num()
            cx,cy=(cx+x,cy+y) if rel else (x,y)
        elif c=='Z':
            cx,cy=sx,sy
        else:
            i+=1; continue
        xs.append(cx); ys.append(cy)
    if not xs: return None
    return (min(xs),min(ys),max(xs),max(ys))

def shape_bbox(e):
    t=loc(e)
    g=lambda k,dv=0.0: float(e.get(k,dv) or dv)
    if t=='rect':  return (g('x'),g('y'),g('x')+g('width'),g('y')+g('height'))
    if t=='circle':return (g('cx')-g('r'),g('cy')-g('r'),g('cx')+g('r'),g('cy')+g('r'))
    if t=='ellipse':return (g('cx')-g('rx'),g('cy')-g('ry'),g('cx')+g('rx'),g('cy')+g('ry'))
    if t=='line':  return (min(g('x1'),g('x2')),min(g('y1'),g('y2')),
                           max(g('x1'),g('x2')),max(g('y1'),g('y2')))
    if t=='path':  return path_bbox(e.get('d'))
    return None

def union(a,b):
    if a is None: return b
    if b is None: return a
    return (min(a[0],b[0]),min(a[1],b[1]),max(a[2],b[2]),max(a[3],b[3]))

# CTA matni — shu so'zlardan biri bo'lsa, o'rab turgan guruh tugmaga aylanadi
CTA_WORDS=('QATNASHISH','QATNASHAMAN','RO‘YXATDAN','ROYXATDAN','RO’YXATDAN',
           'BEPUL DARSGA','JOY BAND','BOSHLASH','OLMOQCHIMAN')

def text_bbox(e):
    """<text>/<tspan> uchun taxminiy chegara: bazaviy chiziqdan yuqoriga va
    pastga shrift o'lchami bo'yicha, kengligi belgilar soniga qarab. Aniq
    emas, lekin qatlam chegarasi uchun yetarli — atrofiga zaxira qo'shiladi."""
    xs=[];ys=[]
    fs=float(e.get('font-size') or 16)
    for t in list(e.iter()):
        if loc(t) not in ('text','tspan'): continue
        try: x=float(t.get('x')); y=float(t.get('y'))
        except (TypeError,ValueError): continue
        txt=''.join(t.itertext())
        xs += [x, x+len(txt)*fs*0.75]
        ys += [y-fs*1.3, y+fs*0.5]
    if not xs: return None
    return (min(xs),min(ys),max(xs),max(ys))

class Site:
    def __init__(self,svg_path,out_dir,name):
        self.out=out_dir; self.name=name
        self.tree=ET.parse(svg_path); self.root=self.tree.getroot()
        self.W=float(self.root.get('width')); self.H=float(self.root.get('height'))
        self.defs=self.root.find(Q('defs'))
        self.patterns={p.get('id'):p for p in self.root.iter(Q('pattern'))}
        self.images={i.get('id'):i for i in self.root.iter(Q('image'))}
        self.frame=[g for g in self.root if loc(g)=='g'][0]
        self.items=[]      # ('img',info) yoki ('vec',[leaf indekslari])
        self.imgs=[]
        self.fonts={}
        self._hashes={}

    # ---------- 1. barglarni yig'ish ----------
    def collect(self):
        leaves=[]
        def walk(e,mask,style):
            st=dict(style)
            for k in ('opacity','filter'):
                if e.get(k): st[k]=e.get(k)
            if e.get('style') and 'mix-blend-mode' in e.get('style'):
                st['blend']=e.get('style').split('mix-blend-mode:')[1].split(';')[0].strip()
            for c in list(e):
                t=loc(c)
                if t=='mask':
                    r=c.find(Q('rect'))
                    if r is not None:
                        mask=(float(r.get('x',0)),float(r.get('y',0)),float(r.get('width')),float(r.get('height')))
                    continue
                if t in ('defs','clipPath','filter','pattern','linearGradient','radialGradient'): continue
                if t=='g': walk(c,mask,st)
                else:
                    c.set('data-leaf',str(len(leaves)))
                    leaves.append((c,mask,dict(st)))
        walk(self.frame,None,{})
        self.leaves=leaves
        # ota-xarita: CTA guruhining chegarasini topish uchun kerak
        self.parent={}
        for e in self.frame.iter():
            for c in e: self.parent[c]=e
        # bo'laklarga ajratish: rasm -> alohida, qolgani -> ketma-ket SVG qatlam
        chunk=[]
        for i,(e,mask,st) in enumerate(leaves):
            fill=e.get('fill','')
            if loc(e)=='rect' and fill.startswith('url(#pattern'):
                if chunk: self.items.append(('vec',chunk)); chunk=[]
                self.items.append(('img',i))
            else:
                chunk.append(i)
        if chunk: self.items.append(('vec',chunk))

    # ---------- 2. rasmlar ----------
    def extract_images(self):
        os.makedirs(os.path.join(self.out,'assets'),exist_ok=True)
        for k,(kind,payload) in enumerate(self.items):
            if kind!='img': continue
            e,mask,st=self.leaves[payload]
            x,y=float(e.get('x',0)),float(e.get('y',0))
            w,h=float(e.get('width')),float(e.get('height'))
            pid=e.get('fill')[5:-1]
            pat=self.patterns[pid]
            use=pat.find(Q('use'))
            a,b,c,d,tx,ty=parse_matrix(use.get('transform'))
            iid=use.get('{%s}href'%XLINK).lstrip('#')
            img_el=self.images[iid]
            data=img_el.get('{%s}href'%XLINK).split(',',1)[1]
            im=Image.open(io.BytesIO(base64.b64decode(data))).convert('RGBA')
            # <use transform> tasvir foydalanuvchi birligini bbox (0..1) ga
            # o'tkazadi:  u = a*px + tx  ->  teskarisi:  px = (u - tx)/a.
            # <image width/height> odatda piksel bilan bir xil, lekin bir xil
            # bo'lmasa — rasterga nisbat bilan tuzatamiz.
            uw=float(img_el.get('width') or im.width) or im.width
            uh=float(img_el.get('height') or im.height) or im.height
            sx=im.width/uw; sy=im.height/uh
            L=(0-tx)/a*sx;  R=(1-tx)/a*sx
            T=(0-ty)/d*sy;  B=(1-ty)/d*sy
            box=(L,T,R,B)
            # niqob (mask) bo'lsa — ko'rinadigan qismi
            cx,cy,cw,ch=x,y,w,h
            if mask:
                mx,my,mw,mh=mask
                nx,ny=max(x,mx),max(y,my)
                nx2,ny2=min(x+w,mx+mw),min(y+h,my+mh)
                if nx2>nx and ny2>ny:
                    fx0,fy0=(nx-x)/w,(ny-y)/h
                    fx1,fy1=(nx2-x)/w,(ny2-y)/h
                    box=(L+(R-L)*fx0, T+(B-T)*fy0, L+(R-L)*fx1, T+(B-T)*fy1)
                    cx,cy,cw,ch=nx,ny,nx2-nx,ny2-ny
            im,box=pad_for_box(im,box)
            out=im.resize((max(1,round(cw*SCALE)),max(1,round(ch*SCALE))),Image.LANCZOS,box=box)
            fp=io.BytesIO(); out.save(fp,'PNG')
            hsh=hashlib.sha1(fp.getvalue()).hexdigest()[:8]
            if hsh in self._hashes:
                fname=self._hashes[hsh]
            else:
                # AVIF — bir xil ko'rinishda WebP'dan ~2 barobar yengil.
                # Ikki o'lchamda: oddiy ekran 1x ni, retina 2x ni oladi
                # (srcset). Shu bilan telefonda aniqlik ham saqlanadi,
                # ortiqcha bayt ham yuklanmaydi.
                n=len(self._hashes)+1
                fname='%s-%02d.avif'%(self.name,n)
                one=im.resize((max(1,round(cw)),max(1,round(ch))),Image.LANCZOS,box=box)
                one.save(os.path.join(self.out,'assets',fname),'AVIF',
                         quality=AVIF_Q,speed=4)
                out.save(os.path.join(self.out,'assets',fname[:-5]+'@2x.avif'),'AVIF',
                         quality=AVIF_Q,speed=4)
                self._hashes[hsh]=fname
            op=float(e.get('fill-opacity',1))*float(st.get('opacity',1) or 1)
            blur=None
            f=st.get('filter') or e.get('filter')
            if f:
                fid=f[5:-1]
                fe=self.root.find('.//%s[@id="%s"]'%(Q('filter'),fid))
                if fe is not None:
                    g=fe.find(Q('feGaussianBlur'))
                    if g is not None: blur=float(g.get('stdDeviation'))
            self.imgs.append(dict(i=payload,file=fname,x=cx,y=cy,w=cw,h=ch,op=op,
                                  blend=st.get('blend'),blur=blur,name=e.get('id') or ''))

    # ---------- 3. vektor qatlamlar ----------
    def build_overlays(self):
        overlays={}; self.vbox={}
        for n,(kind,payload) in enumerate(self.items):
            if kind!='vec': continue
            keep=set(str(i) for i in payload)
            fr=copy.deepcopy(self.frame)
            for e in list(fr.iter()):
                for c in list(e):
                    if c.get('data-leaf') is not None and c.get('data-leaf') not in keep:
                        e.remove(c)
            # bo'sh guruhlarni tozalash
            for _ in range(8):
                for e in list(fr.iter()):
                    for c in list(e):
                        if loc(c)=='g' and len(list(c))==0: e.remove(c)
            defs=copy.deepcopy(self.defs) if self.defs is not None else ET.Element(Q('defs'))
            for c in list(defs):
                if loc(c) in ('pattern','image'): defs.remove(c)
            # Qatlamni butun sahifa balandligida qoldirmaymiz: brauzer har
            # biri uchun to'liq kattalikdagi bufer ajratadi va birinchi
            # bo'yalish kechikadi. Faqat mazmuni sig'adigan quti olinadi.
            box=None
            for i in payload:
                e=self.leaves[i][0]
                box=union(box, text_bbox(e) if loc(e) in ('text','tspan')
                               else shape_bbox(e))
            PAD=70                      # soya/blur chetga chiqishi mumkin
            if box:
                x0=max(0.0,box[0]-PAD); y0=max(0.0,box[1]-PAD)
                x1=min(self.W,box[2]+PAD); y1=min(self.H,box[3]+PAD)
            else:
                x0,y0,x1,y1=0.0,0.0,self.W,self.H
            if x1-x0<1 or y1-y0<1: x0,y0,x1,y1=0.0,0.0,self.W,self.H
            self.vbox[n]=(x0,y0,x1-x0,y1-y0)
            svg=ET.Element(Q('svg'),{'width':'%g'%(x1-x0),'height':'%g'%(y1-y0),
                'viewBox':'%g %g %g %g'%(x0,y0,x1-x0,y1-y0),
                'fill':'none','class':'v','aria-hidden':'false'})
            svg.append(defs); svg.append(fr)
            xml=ET.tostring(svg,encoding='unicode')
            xml=re.sub(r' data-leaf="\d+"','',xml)
            # id'lar qatlamlar orasida takrorlanmasin
            xml=re.sub(r'(id="|url\(#)([A-Za-z0-9_]+)',lambda m:m.group(1)+m.group(2)+'_c%d'%n,xml)
            xml=xml.replace('<ns0:','<').replace('</ns0:','</').replace(' xmlns:ns0="%s"'%SVG,'')
            xml=xml.replace('ns0:','').replace('ns1:','xlink:')
            # litsenziyali shrift -> bepul analog (aks holda brauzer tasodifiy
            # fallback chizadi va yozuv Figma'dagidan boshqacha chiqadi)
            for lic,free in FONT_SUB.items():
                xml=xml.replace('font-family="%s"'%lic,'font-family="%s"'%free)
            overlays[n]=xml
        self.overlays=overlays

    # ---------- 4. shriftlar ----------
    def scan_fonts(self):
        for t in self.frame.iter(Q('text')):
            fam=t.get('font-family'); w=t.get('font-weight','400')
            if fam: self.fonts.setdefault(fam,set()).add(w)

    # ---------- 5. CTA tugmalari ----------
    def find_ctas(self):
        """CTA — yozuvi bo'yicha topiladi: matn nuqtasini o'z ichiga olgan eng
        kichik "tugmasimon" shakl (kengligi >=200, balandligi 40..160) tugma
        maydoni bo'ladi. Guruh ierarxiyasiga tayanilmaydi — Figma'da tugma
        shakli ba'zan hero bloki bilan bitta guruhda yotadi, ba'zan <rect>
        emas, gradientli <path> bo'ladi."""
        MINW,MINH,MAXH=200,40,160
        shapes=[]
        for e in self.frame.iter():
            if loc(e) in ('path','rect','circle','ellipse','line'):
                b=shape_bbox(e)
                if b: shapes.append((e,b))
        self.ctas=[]; seen=set()
        for t in self.frame.iter(Q('text')):
            txt=''.join(t.itertext()).strip()
            if not any(w in txt.upper() for w in CTA_WORDS): continue
            sp=t.find(Q('tspan'))
            src=sp if sp is not None else t
            try: tx,ty=float(src.get('x')),float(src.get('y'))
            except (TypeError,ValueError): continue
            best=None
            for e,b in shapes:
                if not (b[0]<=tx<=b[2] and b[1]<=ty<=b[3]): continue
                w,h=b[2]-b[0],b[3]-b[1]
                if w<MINW or not (MINH<=h<=MAXH): continue
                area=w*h
                if best is None or area<best[0]: best=(area,b,e)
            if best is None: continue
            _,(x,y,x2,y2),el=best
            key=(round(x),round(y),round(x2),round(y2))
            if key in seen: continue
            seen.add(key)
            h=y2-y
            r=float(el.get('rx') or 0) or round(h/2,2)
            self.ctas.append(dict(x=round(x,2),y=round(y,2),w=round(x2-x,2),
                                  h=round(h,2),r=r,label=txt))
        self.ctas.sort(key=lambda c:c['y'])
        return self.ctas

    # ---------- 6. HTML + CSS ----------
    def emit(self,meta):
        self.scan_fonts(); self.find_ctas()
        fams=[]
        for fam in self.fonts:
            g=WEB_FONTS.get(fam)
            if g and g not in fams: fams.append(g)
        link='https://fonts.googleapis.com/css2?'+'&'.join('family='+f for f in sorted(fams))+'&display=swap'

        body=[]; css=[]
        imgs={d['i']:d for d in self.imgs}
        vseq={}; k=0
        for n,(kind,_) in enumerate(self.items):
            if kind!='img': k+=1; vseq[n]=k
        for n,(kind,payload) in enumerate(self.items):
            if kind=='img':
                d=imgs[payload]
                cls='i%d'%payload
                alt=meta.get('alt',{}).get(d['name'],'')
                body.append('  <img class="im %s" src="assets/%s" '
                            'srcset="assets/%s 1x, assets/%s 2x" '
                            'alt="%s" width="%g" height="%g"%s>'%(
                    cls,d['file'],d['file'],d['file'][:-5]+'@2x.avif',
                    alt,round(d['w']),round(d['h']),
                    ' loading="lazy"' if d['y']>700 else ''))
                rules=['left:%gpx'%d['x'],'top:%gpx'%d['y'],'width:%gpx'%d['w'],'height:%gpx'%d['h']]
                if d['op']<0.999: rules.append('opacity:%.2f'%d['op'])
                if d['blend']: rules.append('mix-blend-mode:%s'%d['blend'])
                if d['blur']: rules.append('filter:blur(%gpx)'%d['blur'])
                css.append('.%s{%s}'%(cls,';'.join(rules)))
            else:
                body.append('  '+self.overlays[n])
                x,y,w,h=self.vbox[n]
                if (x,y,w,h)!=(0,0,self.W,self.H):
                    css.append('.page>svg.v:nth-of-type(%d){left:%gpx;top:%gpx}'
                               %(vseq[n],x,y))
        # CTA — shartnoma bo'yicha <button type="button" data-register>.
        # Modal, mamlakat ro'yxati va uslublarni js/main.js birinchi bosishda
        # o'zi qo'shadi; sahifada modal markupi bo'lmasligi kerak.
        for k,c in enumerate(self.ctas,1):
            body.append('  <button class="cta cta-%d" type="button" data-register '
                        'data-cta="%s">%s</button>'%(
                k,'hero' if k==1 else 'pastki',c.get('label') or 'Bepul qatnashish'))
            css.append('.cta-%d{left:%gpx;top:%gpx;width:%gpx;height:%gpx;border-radius:%gpx}'%(
                k,c['x'],c['y'],c['w'],c['h'],c['r']))

        # Ro'yxatdan o'tish oynasi shartnoma uslubi bilan keladi (qizil).
        # Uni har bir variantning o'z rangiga bo'yaymiz: ID li selektor
        # main.js keyinroq qo'shadigan <style> dan ustun turadi.
        acc=meta.get('accent')
        if acc:
            css.append(
              '\n/* Ro\'yxatdan o\'tish oynasi — variant rangi */\n'
              '#registrationModal.homeModal .HomeFormBtn{background:%s}\n'
              '#registrationModal.homeModal .HomeFormBtn:hover{background:%s}\n'
              '#registrationModal.homeModal .HomeFormRowInput:focus{border-color:%s}\n'
              '#registrationModal.homeModal .phone-input-container:focus-within{border-color:%s}\n'
              '#registrationModal.homeModal button:focus-visible,\n'
              '#registrationModal.homeModal [role="option"]:focus-visible{outline-color:%s}'
              %(acc,shade(acc,.85),acc,acc,acc))

        html=TEMPLATE.format(title=meta['title'],desc=meta['desc'],theme=meta['theme'],
            og=meta.get('og',''),link=link,body='\n'.join(body),variant=meta['variant'])
        open(os.path.join(self.out,'index.html'),'w',encoding='utf-8').write(html)
        os.makedirs(os.path.join(self.out,'css'),exist_ok=True)
        open(os.path.join(self.out,'css','site.css'),'w',encoding='utf-8').write(
            SITE_CSS.format(h=self.H,w=self.W,wm=int(self.W)-1,sub='\n'.join(css),bg=meta.get('bg','#ffffff')))
        return dict(fonts=self.fonts,ctas=self.ctas,imgs=len(self.imgs),overlays=len(self.overlays))

TEMPLATE='''<!doctype html>
<html lang="uz">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=390, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="{theme}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 32 32%27%3E%3Crect width=%2732%27 height=%2732%27 rx=%278%27 fill=%27{theme}%27/%3E%3C/svg%3E">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{og}">
<meta property="og:type" content="website">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{link}" rel="stylesheet">
<link rel="stylesheet" href="css/base.css">
<link rel="stylesheet" href="css/site.css">
</head>
<body data-variant="{variant}">

<main class="page">
{body}
</main>

<!-- Ro'yxatdan o'tish oynasi sahifada YO'Q: js/main.js uni birinchi
     CTA bosilganda o'zi yaratadi (integration shartnomasi). -->
<script src="./js/config.js" defer></script>
<script src="./js/main.js" defer></script>
<!-- Meta Pixel Code — Bio Hil bilan bir xil eventlar: shu sahifada PageView,
     forma yuborilganda CompleteRegistration (js/main.js), thankYou.html da PageView.
     Split test yo‘q, shuning uchun oddiy PageView to‘g‘ri. defer qo‘yilmaydi. -->
<script>
!function(f,b,e,v,n,t,s)
{{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)}};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '2982763675408670');
fbq('track', 'PageView');
</script>
<noscript><img height="1" width="1" style="display:none"
src="https://www.facebook.com/tr?id=2982763675408670&ev=PageView&noscript=1"
/></noscript>
<!-- End Meta Pixel Code -->
</body>
</html>
'''

SITE_CSS='''/* Figma freymidan avtomatik yig'ilgan — tools/svg2site.py.
   Qo'lda tahrirlamang: SVG qayta eksport qilinsa, qaytadan yaratiladi. */
body{{ background:{bg}; }}

/* Figma freymi: qat'iy {w}px kanvas, har bir qatlam absolyut koordinatada.
   .im — rasm to'ldirgan shakl, .v — vektor+matn qatlami (z-tartib DOM bo'yicha) */
.page{{ position:relative; width:{w}px; height:{h}px; margin-inline:auto; overflow:hidden; }}

/* Kanvas qat'iy {w}px. Telefonda <meta viewport width={w}> uni ekran
   kengligiga moslab kattalashtiradi — u yerda hech narsa qilish shart emas.
   Desktop brauzer esa bu meta'ni e'tiborsiz qoldiradi va sahifa keng
   ekranning o'rtasida tor ustun bo'lib qoladi. Shuning uchun faqat keng
   ekranlarda o'lchamini oshiramiz (zoom layoutga ta'sir qiladi, ya'ni
   balandlik ham o'zi to'g'rilanadi). */
@media (min-width:480px){{ .page{{ zoom:1.15; }} }}
@media (min-width:640px){{ .page{{ zoom:1.3;  }} }}
@media (min-width:900px){{ .page{{ zoom:1.45; }} }}
/* {w}px dan tor desktop oynasida kesilib qolmasin */
@media (max-width:{wm}px){{ .page{{ zoom:.92; }} }}
.im{{ position:absolute; display:block; max-width:none; }}
.v{{ position:absolute; left:0; top:0; pointer-events:none; }}
/* CTA — Figma shakli ustidagi shaffof tugma (yozuv SVG qatlamida) */
.cta{{ position:absolute; display:block; padding:0; border:0; background:none;
      font:inherit; color:transparent; cursor:pointer;
      -webkit-tap-highlight-color:transparent; }}
.cta:focus-visible{{ outline:3px solid #fff; outline-offset:3px; }}
{sub}
'''

def main():
    import json
    svg,out=sys.argv[1],sys.argv[2]
    meta=json.loads(sys.argv[3]) if len(sys.argv)>3 else {}
    meta.setdefault('title','Bepul vebinar'); meta.setdefault('desc','')
    meta.setdefault('theme','#ffffff'); meta.setdefault('variant','1')
    s=Site(svg,out,meta.get('prefix','img'))
    s.collect(); s.extract_images(); s.build_overlays()
    info=s.emit(meta)
    print(out,'| rasm:',info['imgs'],'| qatlam:',info['overlays'],'| CTA:',len(info['ctas']))
    for f,w in info['fonts'].items(): print('   shrift:',f,sorted(w))

if __name__=='__main__': main()
