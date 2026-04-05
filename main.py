from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd

def note_information(): 
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(30) 
    driver.get("https://myges.fr/student/home")
    driver.current_url

    xpath_username = "/html/body/div/div/div[2]/b/div/div/form/div[1]/input"
    username = driver.find_element(By.XPATH, xpath_username)
    username.send_keys('YOUR_ACCOUNT')
    time.sleep(1)

    xpath_password = "/html/body/div/div/div[2]/b/div/div/form/div[2]/input"
    password = driver.find_element(By.XPATH, xpath_password)
    password.send_keys('YOUR_PASSWORD')
    time.sleep(1)

    xpath_login = "/html/body/div/div/div[2]/b/div/div/form/div[3]/input[4]"
    driver.find_element(By.XPATH, xpath_login).submit()
    time.sleep(1) 

    xpath_scolarite = "/html/body/div[3]/div[1]/div/div[2]/div/ul/li[4]/a"
    driver.find_element(By.XPATH, xpath_scolarite).click()
    time.sleep(1)

    xpath_notes_absence = "/html/body/div[3]/div[1]/div/div[2]/div/ul/li[4]/ul/li[5]/a"
    driver.find_element(By.XPATH, xpath_notes_absence).click()
    time.sleep(1)

    xpath_change_semestre = "/html/body/div[3]/div[2]/div[3]/div/form[2]/table/tbody/tr/td[2]/div/label"
    driver.find_element(By.XPATH, xpath_change_semestre).click() 
    time.sleep(1)

    xpath_semetre1 = "/html/body/div[8]/div/ul/li[2]"
    driver.find_element(By.XPATH, xpath_semetre1).click()
    time.sleep(1)
    
    xpath_notes_absence = "//*[@id='marksForm:marksWidget:coursesTable']/div/table/tbody"
    note = driver.find_elements(By.XPATH, xpath_notes_absence) 
    time.sleep(1)
    
    notes = []
    for tr in driver.find_elements(By.XPATH,"//*[@id='marksForm:marksWidget:coursesTable']/div/table/tbody/tr"):
        tds = tr.find_elements("tag name", 'td')
        temp = [] 
        for td in tds: 
            temp.append(td.text)
        notes.append(temp)
    return notes


def planning_information(): 
    options = Options()
    options.add_argument('--headless')
    options.add_argument('disable-gpu')

    driver = webdriver.Chrome(options=options) 
    driver.implicitly_wait(5)
    driver.get("https://myges.fr/student/home")

    xpath_username = "/html/body/div/div/div[2]/b/div/div/form/div[1]/input"
    username = driver.find_element(By.XPATH, xpath_username)
    username.send_keys('YOUR_ACCOUNT')
    time.sleep(0.05)

    xpath_password = "/html/body/div/div/div[2]/b/div/div/form/div[2]/input"
    password = driver.find_element(By.XPATH, xpath_password)
    password.send_keys('YOUR_PASSWORD')
    time.sleep(0.05)

    xpath_login = "/html/body/div/div/div[2]/b/div/div/form/div[3]/input[4]"
    driver.find_element(By.XPATH, xpath_login).submit()
    time.sleep(1)

    xpath_planning = "/html/body/div[3]/div[1]/div/div[2]/div/ul/li[3]/a"
    driver.find_element(By.XPATH, xpath_planning).click()
    time.sleep(0.5)
    
    planning = []
    coors = []
    events = driver.find_elements(By.CSS_SELECTOR,".fc-event.reservation-NANTES")
    if len(events) == 0 : 
        driver.find_element(By.XPATH,"/html/body/div[3]/div[2]/div[3]/div/form[2]/div/div/table/tbody/tr/td[1]/button").click()
        time.sleep(0.5)
        # driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div[3]/div/form[2]/div/div/table/tbody/tr/td[2]/button")
        # time.sleep(1)
    for i in driver.find_elements(By.CSS_SELECTOR,".fc-event.reservation-NANTES"):
        coors.append(i.location)
        i.find_element(By.CLASS_NAME, "fc-event-inner").click()
        time.sleep(0.05)
        choose = driver.find_element(By.CSS_SELECTOR, ".ui-dialog.ui-overlay-visible")
        for tr in choose.find_elements(By.XPATH, "./div[2]/table/tbody/tr"):  
            tds = tr.find_elements(By.TAG_NAME,'td')
            temp = [] 
            for td in tds:
                if len(td.text) != 0: 
                   temp.append(td.text)
            if len(temp) != 0: 
               planning.append(temp)
        driver.find_element(By.CSS_SELECTOR, ".ui-dialog-titlebar-icon.ui-corner-all").click()
        time.sleep(0.05) 
 
    cols = [] 
    dates = []
    xpath_content = driver.find_element(By.CSS_SELECTOR, ".fc-view.fc-agenda")
    for tr in xpath_content.find_elements(By.XPATH, "./table/thead/tr"): 
        for th in tr.find_elements(By.TAG_NAME, 'th'): 
            cols.append(th.location)
            dates.append(th.text)
    dates = dates[1:-1]
    cols = cols[1: -1]
    n_coors = len(coors)
    for i in range(0, 7):
        print("---",dates[i], "---")
        for j in range(n_coors): 
            if abs(coors[j]['x'] - cols[i]['x']) <= 5:
                for k in range(j*6, j*6 + 5):
                   print(planning[k])
                print('\n')
    return "Hope you have a nice week"

if __name__ == "__main__": 
    print(planning_information())
    print(note_information())
