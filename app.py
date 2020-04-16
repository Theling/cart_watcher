from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import os
from selenium.webdriver.firefox.options import Options
import joblib
import pandas as pd
from selenium.webdriver.common.keys import Keys
import numpy as np
import time
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import joblib
from time import sleep
from toolkit import alarm

class Cart_watcher:
    def __init__(self, driver_path):
            options = webdriver.ChromeOptions()
            # options.add_argument("user-data-dir=selenium")
            self.driver = webdriver.Chrome(chrome_options=options, 
                                executable_path=driver_path) 
            
    def save_cookies(self, file_name = 'cookies.pkl'):
        self.driver.get('https://www.instacart.com')
        input('pause for logging in.')
        joblib.dump(self.driver.get_cookies(), file_name)

    def load_cookies(self, file_name = 'cookies.pkl'):
        return joblib.load(file_name)

    def connect(self):
        driver = self.driver
        cookies = self.load_cookies()
        driver.get('https://www.instacart.com')
        
        for cookie in cookies:
            try:
                driver.add_cookie(cookie)
            except:
                pass
        driver.get('https://www.instacart.com/store/checkout_v3')

    def watch(self, times = 100, wait_time = 30):
        driver = self.driver
        for _ in range(times):
            try:
                driver.implicitly_wait(3)
                switch_pick_btn = driver.find_element_by_class_name('ic-btn-success')
                if switch_pick_btn.text == 'Switch to Pickup':
                    print('not avaiable, check again in 30s.')
                    sleep(wait_time)
                    driver.get('https://www.instacart.com/store/checkout_v3')
                    sleep(5)
        #             driver.implicitly_wait(3)
                else:
                    alarm('Found abnormal button.')
                    print('----------check manually---------: ic-btn-success is not switch...')
            except NoSuchElementException:
                alarm('No button found, check manually')
                print('----------check manually---------: button not found')

if __name__ == "__main__":
    executable_path = './chromedriver'
    watcher = Cart_watcher(executable_path)
    if input('Regenerate cookie? (empty for NO, any key for YES)'):
        print('chose save cookie.')
        watcher.save_cookies()
    else:
        print('loading existing cookie')
        watcher.connect()
        print('starting watching')
        watcher.watch()

