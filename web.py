import sys
import time
import datetime
from fake_useragent import UserAgent


from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def Wait(dt):
 print('Start to waiting ')
 print('Waiting...')
 while datetime.datetime.now() < dt:
  time.sleep(0.5)

def prepare(account,password):
 ua = UserAgent()
 chrome_options = Options()
 No_Image_loading = {"profile.managed_default_content_settings.images": 2}
 chrome_options.add_experimental_option("prefs", No_Image_loading)
 chrome_options.add_argument('user-agent={}'.format(ua.chrome))

 driver = webdriver.Chrome('/Users/ht1965/Downloads/chromedriver', options=chrome_options)
 driver.maximize_window()
 driver.get("https://soton.leisurecloud.net/Connect/MRMLogin.aspx")
 WebDriverWait(driver,3,0.5).until(EC.presence_of_all_elements_located((By.XPATH,'//*[@id="ctl00_MainContent_InputLogin"]')))
 print('input account name and password')
 driver.find_element_by_xpath('//*[@id="ctl00_MainContent_InputLogin"]').send_keys("yh14n21@soton.ac.uk")
 driver.find_element_by_xpath('//*[@id="ctl00_MainContent_InputPassword"]').send_keys("Hyy020425615561.")
 driver.find_element_by_xpath('//*[@id="ctl00_MainContent_btnLogin"]').click()
 print('Sucuessfully log into main page , try to login into basketball field')
 WebDriverWait(driver, 10, 0.1).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="ctl00_MainContent__advanceSearchResultsUserControl_Activities_ctrl5_lnkActivitySelect_lg"]')))
 driver.find_element_by_xpath('//*[@id="ctl00_MainContent__advanceSearchResultsUserControl_Activities_ctrl5_lnkActivitySelect_lg"]').click()
 for a in range(8):
  WebDriverWait(driver, 10, 0.1).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="ctl00_MainContent_Button2"]')))
  driver.find_element_by_xpath('//*[@id="ctl00_MainContent_Button2"]').click()
  time.sleep(1)
 return(driver)

def weblisttest(driver):
 court=[]
 print('into recycle list')
 #get the available field list
 #only get the available field before target time(1 pm)
 for i in range(8,17):
  xp='//*[@id="ctl00_MainContent_grdResourceView"]/tbody/tr['+str(i)+']/td'
  WebDriverWait(driver, 5, 0.1).until(
   EC.presence_of_all_elements_located((By.XPATH, xp)))
  if driver.find_element_by_xpath(xp).get_attribute('class') == 'itemavailable':
   print('{}00 is available'.format(i+5))
   court.append(i)

#get the first three field before target time
 if len(court)>0:
  tar='//*[@id="ctl00_MainContent_grdResourceView"]/tbody/tr['+str(court[0])+']/td'
  print('book {}'.format(court[0]+5))
  return(tar)
 else:
  print('Nothing available, try to refresh the page')
  return('')

def web(driver,dt2):
 #Refresh before available field show up
 print('Start time：',datetime.datetime.now())
 Availability = ''
 print('Start to refresh')
 while Availability == '':
  print('Enter refresh loop determination')
  driver.refresh()
  Availability = weblisttest(driver)
  if datetime.datetime.now()>dt2:
   print('Already passed the relase time, exit the program')
   driver.quit()
   sys.exit()

 # find the target field and click
 WebDriverWait(driver, 10, 0.1).until(EC.element_to_be_clickable((By.XPATH, Availability)))
 driver.find_element_by_xpath(Availability).click()

 print('Book time slot:',datetime.datetime.now())
 WebDriverWait(driver, 5, 0.1).until(
  EC.element_to_be_clickable((By.XPATH, '//*[@id="ctl00_MainContent_btnBasket"]')))
 driver.find_element_by_xpath('//*[@id="ctl00_MainContent_btnBasket"]').click()
 print('Successful！')
 time.sleep(10)

def nowtime():
 n=datetime.datetime.now().replace(hour=23).replace(minute=59).replace(second=59).replace(microsecond=0)
 return(n)

def main(account,password):
 driver = prepare(account, password)
 try:
  n=nowtime()
  Wait(n)
  n2=n + datetime.timedelta(seconds=16)
  web(driver,n2)
 except Exception as e:
  print('Error：')
  print(e)
  driver.quit()

if __name__ == '__main__':
  #my account name 
 account=""

 #my password
 password=''
 main(account,password)
