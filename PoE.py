import os, sys, time, keyboard, selenium, requests, pytest, re, datetime, urllib3
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# CHROME DRIVER PATH
chrome_driver = webdriver.Chrome(executable_path = "/Users/Amitabh.Mishra/Documents/Mesh_530/chromedriver.exe")

def controller_login():
    chrome_driver.find_element_by_id("user").send_keys("araknis")
    chrome_driver.find_element_by_id("pass").send_keys("snapav704")
    chrome_driver.find_element(By.CSS_SELECTOR, ".btn-primary:nth-child(1)").click()

def poe_switch_login():
    chrome_driver.find_element(By.ID, "usid").click()
    chrome_driver.find_element(By.ID, "usid").send_keys("araknis")
    chrome_driver.find_element(By.ID, "psid").send_keys("mistyjungle237")
    chrome_driver.find_element(By.ID, "btnPwd").click()

def navigate_to_firmware_page():
    chrome_driver.find_element_by_id("fun_2_3").click() # Navigate to the firmware page

def navigate_to_wifi_setup_page():
    chrome_driver.find_element_by_id("fun_1_2").click() # Navigate to wifi setup page

# FIRMWARE FILES
firmware_files = ["an530i-v3.0.00.17.bin", "an530i-v3.0.00.18.bin"]

for x in range(0, 3):
    for switch in [0, 1]:
        # Login to controller 
        chrome_driver.get("http://192.168.1.136/cgi-bin/luci")
        time.sleep(2)
        controller_login()
        time.sleep(5)

        # Login to PoE switch in new window
        chrome_driver.execute_script("window.open('http://192.168.1.106/login.html', 'new_window')")
        time.sleep(10)
        chrome_driver.switch_to_window(chrome_driver.window_handles[1])
        poe_switch_login()
        time.sleep(10)

        # Go to PoE page
        chrome_driver.find_element(By.CSS_SELECTOR, ".bg-head:nth-child(2) li:nth-child(3) > .arrow-icon").click()
        time.sleep(5)

        # Go back to controller firmware page and upload firmware
        chrome_driver.switch_to_window(chrome_driver.window_handles[0])
        navigate_to_firmware_page()
        time.sleep(10)

        chrome_driver.switch_to_frame(0)
        chrome_driver.find_element_by_id("df_mesh_image").click()
        time.sleep(5)

        keyboard.write(r"C:\Users\Amitabh.Mishra\Documents\Mesh_530\{}".format(firmware_files[switch%2]))
        time.sleep(2)

        keyboard.press_and_release("return")
        time.sleep(5)

        # Upload file
        chrome_driver.find_element(By.ID, "MeshUploadButton").click()
        time.sleep(5)

        # Upgrade for all devices in mesh network
        chrome_driver.find_element(By.CSS_SELECTOR, "#hidemeshbutton > input:nth-child(1)").click()
        time.sleep(10)
        chrome_driver.find_element(By.CSS_SELECTOR, "#msg-buton > input:nth-child(1)").click()

        # Stop Poe Power
        time.sleep(2)
        chrome_driver.switch_to_window(chrome_driver.window_handles[1])
        chrome_driver.find_element(By.CSS_SELECTOR, "tr:nth-child(13) .en").click()
        time.sleep(22) # After ~ 25% (Change to 45-50 for 50% or 70-75 for 75%)
        chrome_driver.find_element(By.ID, "btnApply").click()
        time.sleep(2)

        # Restore PoE Power
        chrome_driver.find_element(By.CSS_SELECTOR, "tr:nth-child(13) .en").click() # Change port number
        time.sleep(2) 
        chrome_driver.find_element(By.ID, "btnApply").click()
        time.sleep(5)

        # Switch back to controller window
        chrome_driver.switch_to_window(chrome_driver.window_handles[0])
        time.sleep(300)
        chrome_driver.refresh()
        time.sleep(5)