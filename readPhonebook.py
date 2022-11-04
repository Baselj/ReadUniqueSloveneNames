from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import random
import time
import os
import time

def perform_actions(driver, keys):
    actions = ActionChains(driver)
    actions.send_keys(keys)
    time.sleep(4)
    print('Deleting cache')
    actions.perform()

def delete_cache(driver):
    driver.execute_script("window.open('')")  # Create a separate tab than the main one
    driver.switch_to.window(driver.window_handles[-1])  # Switch window to the second tab
    driver.get('chrome://settings/clearBrowserData')  # Open your chrome settings.
    perform_actions(driver, Keys.TAB * 2 + Keys.DOWN * 4 + Keys.TAB * 5 + Keys.ENTER)  # Tab to the time select and key down to say "All Time" then go to the Confirm button and press Enter
    driver.close()  # Close that window
    driver.switch_to.window(driver.window_handles[0])  # Switch Selenium controls to the original tab to continue normal functionality.

def restart_browser(browser,url,s,chrome_options):
        browser.quit()
        browser = webdriver.Chrome(service=s, options= chrome_options)
        delete_cache(browser)
        browser.get(url)
        return browser

def addRandomWait(maxWait):
    time.sleep(random.uniform(1,maxWait))

def removeFileIfExists(name):
    if os.path.exists(name):
        os.remove(name)

def writeToFiles(nameSurname,name,namecsv,nameCollection):
    #name+surname
    with open(nameSurname,"a", encoding="utf-8") as f:
        for i in nameCollection:
            f.write(f"{i}\n")

    #read existing file and remove duplicates
    uniqueNameCollection= []

    for i in nameCollection:
        splitI =i.split(" ")
        lastWord=  splitI.pop();
        writeWord = lastWord if ("." not in lastWord) else splitI.pop()
        if writeWord != "":
            uniqueNameCollection.append(writeWord)

    with open(name, encoding="utf-8") as m:
        uniqueNameCollection= uniqueNameCollection + m.read().splitlines()

    uniqueNameCollection = set(uniqueNameCollection)

    with open(name,"w", encoding="utf-8") as f1:
        for i in uniqueNameCollection:
            f1.write(f"{i}\n")

    with open(namecsv,"w", encoding="utf-8") as f1:
        for i in uniqueNameCollection:
            f1.write(f"{i};")


#folders
osnovniFolder =os.path.dirname(os.path.realpath(__file__))
chromeDriverFolder = osnovniFolder+ r"\SeleniumDrivers\chromedriver.exe"
nameSurname="nameSurname.txt"
name= "name.txt"
namecsv= "namecsv.txt"
dumpToFile =8000
cities="cities.txt"
skipped = 0

url="https://www.itis.si/iskanje"

s=Service(chromeDriverFolder)
chrome_options = webdriver.ChromeOptions()
chrome_options = Options()

#configure chrome for long term scraping (12h +)
chrome_options.add_experimental_option("prefs", {
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing_for_trusted_sources_enabled": False,
        "safebrowsing.enabled": False
        
})

chrome_options.add_argument("start-maximized"); #// https://stackoverflow.com/a/26283818/1689770
chrome_options.add_argument("enable-automation"); #// https://stackoverflow.com/a/43840128/1689770
chrome_options.add_argument("--no-sandbox"); #//https://stackoverflow.com/a/50725918/1689770
chrome_options.add_argument("--disable-dev-shm-usage"); #//https://stackoverflow.com/a/50725918/1689770
chrome_options.add_argument("--disable-browser-side-navigation"); #//https://stackoverflow.com/a/49123152/1689770
chrome_options.add_argument("--disable-gpu"); #//https://stackoverflow.com/questions/51959986/how-to-solve-selenium-chromedriver-timed-out-receiving-message-from-renderer-exc

with open(cities, encoding="utf-8") as m:
    Mesta=m.read().splitlines()
nameCollection = []
stImen=0
browser = webdriver.Chrome(service=s, options= chrome_options)
browser.get(url)

try:
    for m in Mesta:
        try:
            browser.implicitly_wait(40)
            browser.find_element(By.CLASS_NAME, "people").click()
            browser.find_element(By.NAME, "ctl00$search$tbWhere").clear()
            browser.find_element(By.NAME, "ctl00$search$tbWhere").send_keys(m)
            browser.find_element(By.ID, "search_btnSearch").click()
        except:
            skipped+=1
            if skipped > 5:
                time.sleep(100)
            elif skipped >10:
                break
                print("too many skipped")    

            print (f"Skipped {m} number {Mesta.index(m)} from {len(Mesta)}")
            browser=restart_browser(browser,url,s,chrome_options)
            continue
        addRandomWait(2)
        

        try:
            imena= browser.find_elements(By.CLASS_NAME, "title")
        except:
            continue
        currentNames = [i.text for i in imena if i.text != ""]
        #if less then 30 entries means no more pages
        if len(currentNames)<30:
            nameCollection = nameCollection+ currentNames
            print(f"Currently reading {m}, number {Mesta.index(m)} from {len(Mesta)}, collection of names has {stImen+ len(nameCollection)} entries")
        #click to new page
        if len(nameCollection)>dumpToFile:
            writeToFiles(nameSurname,name,namecsv,nameCollection)
            stImen=len(nameCollection)+stImen
            nameCollection=[]
            with open(cities, 'w', encoding="utf-8") as fout:
             fout.writelines(f"{l}\n" for l in Mesta[Mesta.index(m):])
            browser=restart_browser(browser,url,s,chrome_options)
        else:
            time1= time.perf_counter()
            time2=time1
            while(len(currentNames)<=30 and len(currentNames)!=0 and (time2-time1) < 60):
                addRandomWait(1)
                if currentNames[0]!="":
                    try:
                        browser.find_element(By.ID, "CPH_bodyMain_SearchResultsStatic1_ResultsPagerStatic1_aNextPage").click()
                    except:
                        time2=time.perf_counter()
                        break;    
                    currentNames = [i.text for i in browser.find_elements(By.CLASS_NAME, "title") if i.text != ""]
                    nameCollection = nameCollection+ currentNames
                    print(f"Currently reading {m}, number {Mesta.index(m)} from {len(Mesta)}, collection of names has {stImen+len(nameCollection)} entries")
                time2=time.perf_counter()
            
finally:
    browser.quit()
    writeToFiles(nameSurname,name,namecsv,nameCollection)    


