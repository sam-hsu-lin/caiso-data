from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from datetime import date, timedelta
from time import sleep
# import pandas as pd
# import numpy as np

""" there's probably some nice way to manage the download so the files all go to a neat place """
# import os
# pathOut = os.path.expanduser('~').replace("\\","/") + "/Documents/"

profile = webdriver.FirefoxProfile()

# profile.set_preference("browser.download.folderList", 2)
# profile.set_preference("browser.download.manager.showWhenStarting", False)
# profile.set_preference("browser.download.lastDir", pathOut)
# profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")

driver = webdriver.Firefox(firefox_profile=profile)
page = "https://www.caiso.com/TodaysOutlook/Pages/emissions.html" # desired page

start_date = date(2018,4,10) # earliest data is from April 10, 2018
# end_date = date(2018,4,12) # for testing
end_date = date.now() # latest data is from today
delta = end_date - start_date   # returns timedelta

driver.get(page)
section = driver.find_element_by_css_selector("#navbar-follow > li:nth-child(3) > a:nth-child(1)")
date_selector = driver.find_element_by_css_selector(".co2-breakdown-date") # css selector of desired elements
download_button = driver.find_element_by_css_selector("#dropdownMenuCO2Breakdown")
download_option = driver.find_element_by_css_selector("#downloadCO2BreakdownCSV")

section.click()

for i in range(delta.days + 1):	
	day = start_date + timedelta(days=i) # day is start_date plus i number of days (indexed from 0)
	
	date_selector.click()
	date_selector.clear()
	driver.execute_script("""
		arguments[0].dispatchEvent(new FocusEvent("blur"));
		arguments[0].dispatchEvent(new FocusEvent("focus"));
		arguments[0].dispatchEvent(new KeyboardEvent("keydown"));
		$('.form-control.date').datepicker("update", arguments[1]).datepicker("update");
		arguments[0].dispatchEvent(new Event("select"));
		arguments[0].dispatchEvent(new KeyboardEvent("keyup"));
		arguments[0].dispatchEvent(new FocusEvent("focusout"));
		arguments[0].dispatchEvent(new Event("onRender"));
		arguments[0].dispatchEvent(new Event("changeDate"));
		arguments[0].dispatchEvent(new FocusEvent("blur"));
		""", date_selector,day.strftime("%m/%d/%Y"))
	date_selector.send_keys("",Keys.ENTER)
	download_button.click()
	sleep(.1)
	download_option.click()
	sleep(.1)

sleep(3)
driver.close()
