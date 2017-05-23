from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import mysql.connector
import time
import re

att_service = "directv"

street_address = "7705 Nw 73rd Terrace"
zip_code = 33321

webpage = "https://www.att.com/shop/unified/availability.html" # edit me

phantom = False
driver = None


if phantom:
    driver = webdriver.PhantomJS() #headless
else:
    driver = webdriver.Chrome('./chromedriver') #Opens Chrome browser, useful for testing

driver.get(webpage)

time.sleep(3)

#Input user info
address = driver.find_element_by_id("streetaddress")
address.send_keys(street_address)

zip_box = driver.find_element_by_id("zipcode")
zip_box.send_keys(zip_code)
time.sleep(2)
submit = driver.find_element_by_css_selector("input.blueButton.lrgButton.ckavButton")
submit.click()



try:
    WebDriverWait(driver, 12).until(EC.presence_of_element_located((By.ID, "seeoffermodal.html")))
    print "Page is ready!"
except TimeoutException:
    print "Loading took too much time!"
    time.sleep(5)


skins = driver.find_elements_by_css_selector("i.skin")

#Select Packages
for check in skins:
    label = check.get_attribute("aria-label")

    if label == "Internet":
        internet_check = check
        if (internet_check.get_attribute("aria-checked") == "true"):
             internet_check.click()

    elif label == "TV":
        tv_check = check
        if not (tv_check.get_attribute("aria-checked") == "true"):
            tv_check.click()


    elif label == "Voice":
        phone_check = check
        if (phone_check.get_attribute("aria-checked") == "true"):
            phone_check.click()

time.sleep(3)

#Determine if Uverse or DirecTV
select = Select(driver.find_element_by_id('filterSelection'))
if att_service == "u-verse":
    # select by visible text
    select.select_by_visible_text('U-verse Offers')
else:
    select.select_by_visible_text('DIRECTV Offers')

time.sleep(3)

###### SCRAPING TIME ##########

#Get the rows

try:
    more_rows = driver.find_element_by_css_selector("span.ng-binding") #Check if there are more rows that are hidden
    more_rows.click()
except Exception as e:
    pass

time.sleep(2)

all_rows = driver.find_elements_by_css_selector("div.col-3.rounded.rel")

for row in all_rows:
