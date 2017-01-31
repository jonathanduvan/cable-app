from selenium import webdriver
from selenium.common.exceptions import InvalidElementStateException
import time
import re

street_address = "7705 Nw 73rd Terrace"
zip_code = 33321

webpage = "http://www.xfinity.com/?Shop=1" # edit me

phantom = True
driver = None

if phantom:
    driver = webdriver.PhantomJS() #headless
else:
    driver = webdriver.Chrome('./chromedriver') #Opens Chrome browser, useful for testing

driver.get(webpage)

try:
    address = driver.find_element_by_id("contentplaceholder_2__streetNameTxt")

except InvalidElementStateException as ex:
            enter_address = driver.find_element_by_id("enter_address")
            enter_address.click()

enter_address = driver.find_element_by_id("enter_address")
enter_address.click()
time.sleep(2)
address = driver.find_element_by_id("contentplaceholder_2__streetNameTxt")
address.send_keys(street_address)

zip_box = driver.find_element_by_id("contentplaceholder_2__zipCodeTxt")
zip_box.send_keys(zip_code)

submit = driver.find_element_by_id("contentplaceholder_2__submitIbtn")

submit.click()

time.sleep(10)

links = driver.find_elements_by_xpath("//*[contains(text(), 'new Comcast customer')]")

for link in links:
    link.click()
    break

time.sleep(10)

deals = driver.find_elements_by_xpath("//*[contains(text(), 'View Deals')]")

for deal in deals:
     onclick_text2 = deal.get_attribute('class')

     if onclick_text2 and re.search("tmmbtn vd", onclick_text2):
        deal.click()
        break

#Selecting/Deselecting Xfinity package options
time.sleep(10)

internet_check = driver.find_element_by_id("_internetLobHtmlInputCheckBox")

if internet_check.is_selected():
    for internet_span in driver.find_elements_by_xpath('.//span[@class = "checkbox contentplaceholder_0$middle_1$_offerFinderControl$ctl01$_internetLobHtmlInputCheckBox selected"]'):
        internet_span.click()
        break

phone_check = driver.find_element_by_id("_voiceLobHtmlInputCheckBox")

if phone_check.is_selected():
    for phone_span in driver.find_elements_by_xpath('.//span[@class = "checkbox contentplaceholder_0$middle_1$_offerFinderControl$ctl01$_voiceLobHtmlInputCheckBox selected"]'):
        phone_span.click()
        break

home_check = driver.find_element_by_id("_homeLobHtmlInputCheckBox")

if home_check.is_selected():

    for home_span in driver.find_elements_by_xpath('.//span[@class = "checkbox contentplaceholder_0$middle_1$_offerFinderControl$ctl01$_homeLobHtmlInputCheckBox selected"]'):
        home_span.click()
        break

tv_check = driver.find_element_by_id("_tvLobHtmlInputCheckBox")

if not (tv_check.is_selected()):
    for tv_span in driver.find_elements_by_xpath('.//span[@class = "checkbox contentplaceholder_0$middle_1$_offerFinderControl$ctl01$_tvLobHtmlInputCheckBox"]'):
        tv_span.click()
        break

see_offers = driver.find_elements_by_xpath("//*[contains(text(), 'See Offers')]")

for offer in see_offers:
    offer_text = offer.get_attribute('class')

    if offer_text and re.search("btn btn-yellow show-offers-button", offer_text):
        offer.click()
        break

time.sleep(5)

###### SCRAPING TIME ##########

#Get first row info
first_row = driver.find_element_by_css_selector(".offer_row.first_row")
first_package = first_row.find_element_by_class_name("package")


package_text = first_package.text.strip().split("\n")

first_pack_name = package_text[0] #Package name
print "first package name: " + first_pack_name

first_channels = first_row.find_element_by_class_name("channels")
first_channels_box = first_channels.find_element_by_class_name("num")

first_channels_text = first_channels_box.text.strip().split("\n")

print "first package channels: " + first_channels_text[0]

first_pricing = first_row.find_element_by_class_name("total-price")

first_pricing_text = first_pricing.text.strip().split("\n")

first_noformat_price = first_pricing_text[1]
first_price_per_month = first_noformat_price[:len(first_noformat_price)-5] + '.' + first_noformat_price[len(first_noformat_price)-5:]

if not phantom:
    print "price: " + first_price_per_month

else:
    print "price: " + first_pricing_text[0] + ".99/mo"

print "\n#######\ncash me oussah\n"
