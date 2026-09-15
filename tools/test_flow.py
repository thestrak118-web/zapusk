"""Ro'yxatdan o'tish oqimi sinovi — haqiqiy yozuv YUBORILMAYDI:
script.google.com CDP orqali bloklanadi."""
import sys, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

BASE={'ildiz':'http://127.0.0.1:8899/index.html',
      'a':'http://127.0.0.1:8899/a/index.html',
      'b':'http://127.0.0.1:8899/b/index.html',
      'c':'http://127.0.0.1:8899/c/index.html'}
opts=Options()
for a in ('--headless=new','--no-sandbox','--disable-gpu','--window-size=390,900'):
    opts.add_argument(a)
d=webdriver.Chrome(options=opts,service=Service('/usr/bin/chromedriver'))
d.execute_cdp_cmd('Network.enable',{})
d.execute_cdp_cmd('Network.setBlockedURLs',{'urls':['*script.google.com*']})

fail=0
def check(v,cond,msg):
    global fail
    print('   %s %s'%('OK  ' if cond else 'XATO',msg))
    if not cond: fail+=1

for v in ('ildiz','a','b','c'):
    print('--- variant',v)
    d.get(BASE[v])
    time.sleep(1.2)
    btns=d.find_elements(By.CSS_SELECTOR,'[data-register]')
    check(v,len(btns)==2,'2 ta CTA tugma (topildi: %d)'%len(btns))
    # modal sahifada oldindan yo'q
    pre=d.find_elements(By.ID,'registrationModal')
    check(v,len(pre)==0,'modal boshida sahifada yo\'q')
    btns[0].click(); time.sleep(0.8)
    modal=d.find_elements(By.ID,'registrationModal')
    check(v,len(modal)==1,'CTA bosilgach modal paydo bo\'ldi')
    if not modal: continue
    check(v,modal[0].is_displayed(),'modal ko\'rinadi')
    ids=['name','phone','submitBtn','selectedCountry','countryDropdown',
         'registrationForm','closeModalBtn','nameError','phoneError']
    miss=[i for i in ids if not d.find_elements(By.ID,i)]
    check(v,not miss,'forma ID lari joyida%s'%('' if not miss else ' — yetishmaydi: '+','.join(miss)))
    code=d.find_element(By.ID,'selectedCountryCodeText').text.strip()
    check(v,code=='+998','mamlakat kodi +998 (%s)'%code)
    # bo'sh forma -> xato
    d.find_element(By.ID,'submitBtn').click(); time.sleep(0.5)
    ne=d.find_element(By.ID,'nameError'); pe=d.find_element(By.ID,'phoneError')
    check(v,ne.is_displayed() or pe.is_displayed(),'bo\'sh forma xato beradi')
    check(v,'thankYou' not in d.current_url,'bo\'sh forma bilan o\'tkazmaydi')
    # noto'g'ri telefon
    d.find_element(By.ID,'name').send_keys('Sinov Foydalanuvchi')
    d.find_element(By.ID,'phone').send_keys('123')
    d.find_element(By.ID,'submitBtn').click(); time.sleep(0.5)
    check(v,'thankYou' not in d.current_url,'qisqa raqam bilan o\'tkazmaydi')
    # to'g'ri telefon
    ph=d.find_element(By.ID,'phone'); ph.clear(); ph.send_keys('901234567')
    d.find_element(By.ID,'submitBtn').click(); time.sleep(1.5)
    check(v,'thankYou' in d.current_url,'to\'g\'ri ma\'lumot -> thankYou.html (%s)'%d.current_url.rsplit('/',1)[-1])
    body=d.find_element(By.TAG_NAME,'body').text.strip()
    check(v,len(body)>20,'rahmat sahifasi matni ko\'rinadi (%d belgi)'%len(body))

d.quit()
print('\nNATIJA:', 'hammasi o\'tdi' if not fail else '%d ta xato'%fail)
sys.exit(1 if fail else 0)
