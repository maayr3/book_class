#!python3

import pickle
import time
import random
import yaml
import configparser

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from chromedriver_py import binary_path

config = configparser.ConfigParser()
config.read('config.ini')
config = config['DEFAULT']

schedule = {}
with open('schedule.yaml', 'r') as stream:
    try:
        schedule = yaml.safe_load(stream)
    except:
        print('Unable to load schedule.yaml')
        exit(1)

options = webdriver.ChromeOptions() 
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(executable_path=binary_path, options=options)
driver.implicitly_wait(30)
print('')

driver.get("https://thefitnessplayground.com.au/timetables/")


driver.find_element_by_class_name('bw-widget__cart_button')
print('found classes table')

select = Select(driver.find_element_by_class_name('location_alias'))
select.select_by_visible_text('Surry Hills Fitness Playground')

third_day = driver.find_elements_by_class_name('bw-widget__day')[3]
date_text = third_day.find_element_by_class_name('bw-widget__date').text
weekday = date_text.split(',')[0]

if weekday not in schedule.keys():
    print('No class to book today: {}'.format(weekday))
    exit(0)

class_to_book = schedule[weekday]
print('Trying to book: {} {} {}'.format(weekday, class_to_book['time'], class_to_book['name']))
classes = third_day.find_elements_by_class_name('bw-session')
class_found = None
for _class in classes:
    if class_to_book['time'] in _class.text and class_to_book['name'] in _class.text:
        print('found matching class')
        class_found = _class.find_element_by_class_name('bw-widget__cart_button')
        break

if class_found == None:
    print('couldnt find class')
    time.sleep(10)
    driver.close()
    exit(1)

if 'Sign Up' not in class_found.text:
    print('class unavailable')
    driver.close()
    exit(1)

class_found.click()
driver.switch_to.window(driver.window_handles[-1])

username = driver.find_element_by_id('su1UserName')
print('logging in..')
username.send_keys(config['username'])
password = driver.find_element_by_id('su1Password')
password.send_keys(config['password'])

time.sleep(1)
driver.find_element_by_class_name("loginButton").click()

driver.find_element_by_id('SubmitEnroll2').click()
print('class booked')

time.sleep(5)
driver.close()
driver.close()
exit(0)