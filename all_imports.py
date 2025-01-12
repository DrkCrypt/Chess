# Core modules
import os
import re
import sys
import time
import zipfile
import subprocess
from datetime import date
from shutil import move, copymode, make_archive
import pandas as pd

# Selenium modules
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from webdriver_manager.chrome import ChromeDriverManager

# ChromeDriver setup
def setup_driver():
    opt = Options()
    opt.add_experimental_option("debuggerAddress", "localhost:8989")
    opt.add_argument('--disable-gpu')

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), 
        options=opt
    )

    driver.implicitly_wait(5)
    return driver

# Utility functions
def tab(n, driver):
    tn = driver.window_handles[n]
    driver.switch_to.window(tn)

def wait_for_clickable(xpth, driver):
    return WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpth)))

def find_element(xpath, driver):
    try:
        return driver.find_element(by=By.XPATH, value=xpath)
    except Exception:
        return None

def wrreplace(cpth, search_text, replace_text):
    with open(cpth, 'r+') as f:
        file = f.read()
        file = re.sub(search_text, replace_text, file, 1)
        f.seek(0)
        f.write(file)
        f.truncate()

def write(cont):
    with open('extract.csv', 'a', encoding='utf-8') as f:
        try:
            f.write(cont)
        except:
            pass

def wait_for_presence(xpth, driver):
    return WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpth)))

def scroll(driver):
    driver.execute_script("window.scrollBy(0, 500);")  # Scroll down by 500 pixels
