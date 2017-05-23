from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import mysql.connector
import time
import re



cnx = mysql.connector.connect(user='cordstreamjon', password='temp44$$',
                              host='127.0.0.1',
                              database='employees')
cnx.close()

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

time.sleep(3)
enter_address = driver.find_element_by_id("enter_address")
enter_address.click()
time.sleep(5)
address = driver.find_element_by_id("contentplaceholder_2__streetNameTxt")
address.send_keys(street_address)

zip_box = driver.find_element_by_id("contentplaceholder_2__zipCodeTxt")
zip_box.send_keys(zip_code)

submit = driver.find_element_by_id("contentplaceholder_2__submitIbtn")

submit.click()


time.sleep(10)

if (driver.current_url == 'https://www.xfinity.com/localize/activeaccount.aspx'):
    print "Made it to new customer"
    try:
        link = driver.find_element_by_link_text('new Comcast customer')
        link.click()


    except Exception as e:
        pass
else:
    print "errorrrrrr"
    error_page = driver.find_element_by_class_name('icon-house-cross')
    error_message = None
    try:
        error_message = error_page.text
        driver.close()
        print "NOT PROVIDED AT THIS ADDRESS"
        #return "NOT PROVIDED AT THIS ADDRESS"

    except Exception as e:
        print e
        drivr.close()
        print "UNKNOWN URL"
        #return "UNKNOWN URL"

try:
    deal_test = driver.find_element_by_css_selector("a.tmmbtn.vd")
    deal_test.click()

except Exception as e:
    pass


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

#Get the rows

try:
    more_rows = driver.find_element_by_css_selector("a.sprite") #Check if there are more rows that are hidden
    more_rows.click()
except Exception as e:
    pass


other_rows = driver.find_elements_by_id("_tvOfferRow")

print "########################################"

i = 1
for row in other_rows:

    #Get package info
    pack = row.find_element_by_css_selector("th.package")
    pack_list = pack.text.strip().split("\n")

    if (len(pack_list) == 1):
        continue

    print "\nPackage Number " + str(i) + " Name: " + pack_list[0]

    #get channel info

    channels = row.find_element_by_css_selector("td.channels")
    channels_box = channels.find_element_by_css_selector("div.num")

    channels_text = channels_box.text.strip().split("\n")

    print "Package Number " + str(i) + " Channels: " + str(channels_text[0])

    #get pricing info
    pricing = row.find_element_by_css_selector("div.total-price")


    if phantom:
        inner_text = driver.execute_script("return arguments[0].innerText;", pricing)
        pricing_text = inner_text.strip().split("\n")
    else:
        pricing_text = pricing.text.strip().split("\n")

    if (len(pricing_text[0]) > 10):
        noformat_price = pricing_text[1]
    else:
        noformat_price = pricing_text[0]
    pricing_per_month = noformat_price[:len(noformat_price)-5] + '.' + noformat_price[len(noformat_price)-5:]

    print "Package Number " + str(i) + " Price: " + str(pricing_per_month) + "\n"

    #Get the next row
    i+=1
driver.close()
