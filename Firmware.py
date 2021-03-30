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

####################################################################################################################################
# THINGS TO CHANGE:

# chrome_driver path -> Set Prior
# output_file_path -> Set Prior
# firmware_files -> Set Prior
# upgrade_downgrade_loops -> User Input
# login credentials -> under def login(): -> User Input
# node_1 IP -> under def node_1_default_check(): -> User Input
# node_2 IP -> under def node_2_default_check(): -> User Input
# chrome_driver.get(IP) -> IP address for controller -> User Input 
# path to firmware file location - Set Prior

####################################################################################################################################

# User Input
output_file_name = input("Enter file name to save as: ")

mesh_username = input("Enter mesh username: ")
mesh_password = input("Enter mesh password: ")

controller_IP = input("Enter controller IP address: ")
node_1_IP = input("Enter node 1 IP address: ")
node_2_IP = input("Enter node 2 IP address: ")

upgrade_downgrade_loops = input("Enter number of upgrade/downgrade loops: ")

# OUTPUT FILE PATH
# output_file_path = "/Users/Brandon/Desktop/530 U_D/{}.txt"
output_file_path = "/Users/Amitabh.Mishra/Documents/Mesh_530/{}.txt".format(output_file_name)

# FIRMWARE FILES
firmware_files = ["an530i-v3.0.00.17.bin", "an530i-v3.0.00.18.bin"]

# INITIALIZE COUNTERS
upgrade_counter = 0
downgrade_counter = 0
failed_counter = 0
default_counter = 0

user_start = input("Start test (Y/N): ")

# CHROME DRIVER PATH
# chrome_driver = webdriver.Chrome(executable_path = "/Users/Brandon/Desktop/530 U_D/chromedriver.exe")
chrome_driver = webdriver.Chrome(executable_path = "/Users/Amitabh.Mishra/Documents/Mesh_530/chromedriver.exe")

# FUNCTIONS
def default_login():
    chrome_driver.find_element_by_id("user").send_keys("araknis")
    chrome_driver.find_element_by_id("pass").send_keys("araknis")
    chrome_driver.find_element(By.CSS_SELECTOR, ".btn-primary:nth-child(1)").click()

def login():
    chrome_driver.find_element_by_id("user").send_keys(mesh_username)
    chrome_driver.find_element_by_id("pass").send_keys(mesh_password)
    chrome_driver.find_element(By.CSS_SELECTOR, ".btn-primary:nth-child(1)").click()

def navigate_to_firmware_page():
    print("Clicking on firmware page")
    chrome_driver.find_element_by_id("fun_2_3").click() 

def navigate_to_wifi_setup_page():
    print("Clicking on wifi setup page.")
    chrome_driver.find_element_by_id("fun_1_2").click() # Navigate to wifi setup page

def node_1_default_check():
    chrome_driver.execute_script("window.open('http://{}/cgi-bin/luci', 'new_window')".format(node_1_IP))
    time.sleep(10)
    chrome_driver.switch_to_window(chrome_driver.window_handles[1])
    time.sleep(10)

    # Log in with default credentials
    default_login()
    time.sleep(10)
    # If user credentials don't work, the node has been defaulted
    if chrome_driver.find_elements_by_id("fun_2_3"):
        print(currentDateTime + " -- Node 1 Defaulted.", file = outputFile)
        default_counter = default_counter + 1
    elif chrome_driver.find_element_by_id("user"):
        login()
        print("Node 1 Not Defaulted!")
 
    time.sleep(10)
 
    chrome_driver.close()
    chrome_driver.switch_to_window(chrome_driver.window_handles[0])
    time.sleep(10)

def node_2_default_check():
    chrome_driver.execute_script("window.open('http://{}/cgi-bin/luci', 'new_window')".format(node_2_IP))
    time.sleep(10)
    chrome_driver.switch_to_window(chrome_driver.window_handles[1])
    time.sleep(10)

    # Log in with default credentials
    default_login()
    time.sleep(10)

    # If user credentials don't work, the node has been defaulted
    if chrome_driver.find_elements_by_id("fun_2_3"):
        print(currentDateTime + " -- Node 2 Defaulted.", file = outputFile)
        default_counter = default_counter + 1
    elif chrome_driver.find_element_by_id("user"):
        login()
        print("Node 2 Not Defaulted!")
 
    time.sleep(10)
 
    chrome_driver.close()
    chrome_driver.switch_to_window(chrome_driver.window_handles[0])
    time.sleep(10)

# STORE MESH RESULTS
outputFile = open(output_file_path, "a+")

currentDateTime = str(datetime.datetime.now().strftime("%m/%d/%Y | %H:%M:%S"))

# Print header to terminal
print("****************************************************************************************************")
print("Firmware Upgrade/Downgrade Test | "  + currentDateTime)
print("****************************************************************************************************\n")

# Print header to file
print("****************************************************************************************************", file = outputFile)
print("Firmware Upgrade/Downgrade Test | "  + currentDateTime, file = outputFile)
print("****************************************************************************************************\n", file = outputFile)

chrome_driver.get("http://{}/cgi-bin/luci".format(controller_IP))

if (user_start == "Y" or user_start == "y"):
    for x in range(0, int(upgrade_downgrade_loops)):
        for switch in [0, 1]:
            outputFile = open(output_file_path, "a+")



            default_login()
            time.sleep(5)
            if chrome_driver.find_element(By.ID, "fun_2_3"):
                print("Controller is defaulted.")
            elif chrome_driver.find_element(By.ID, "user") or chrome_driver.find_element(By.ID, "pass"):
                login()
                print("Logged in with user credentials.")
                time.sleep(5)

            currentDateTime = str(datetime.datetime.now().strftime("%m/%d/%Y | %H:%M:%S"))

            # If the change_login element is found, change password 
            # if chrome_driver.find_elements_by_id("fun_2_3"): 
            #     print(currentDateTime + " -- Controller Defaulted")
            #     print(currentDateTime + " -- Controller Defaulted", file = outputFile)
            #     # default_counter = default_counter + 1
            # elif chrome_driver.find_element_by_id("user"):
            #     login()
            #     print(currentDateTime + " Controller Not Defaulted")
            #     print(currentDateTime + " Controller Not Defaulted", file = outputFile)

            # Navigate to wifi page to check firmware version and online status
            navigate_to_wifi_setup_page()
            time.sleep(15)
            chrome_driver.switch_to.frame(0)
            
            # controller_firmware = chrome_driver.find_element(By.ID, "mesh_fwversion_0").text
            # node_1_firmware = chrome_driver.find_element(By.ID, "mesh_fwversion_2").text           
            # node_2_firmware = chrome_driver.find_element(By.ID, "mesh_fwversion_1").text

            if chrome_driver.find_elements(By.CSS_SELECTOR, "#mesh_status_0 strong"):
                controller_status = chrome_driver.find_element(By.CSS_SELECTOR, "#mesh_status_0 strong").text
            else:
                controller_status = "Offline"
            
            if chrome_driver.find_elements(By.CSS_SELECTOR, "#mesh_status_2 strong"):
                node_1_status = chrome_driver.find_element(By.CSS_SELECTOR, "#mesh_status_2 strong").text
            else:
                node_1_status = "Offline"

            if chrome_driver.find_elements(By.CSS_SELECTOR, "#mesh_status_1 strong"):
                node_2_status = chrome_driver.find_element(By.CSS_SELECTOR, "#mesh_status_1 strong").text
            else:
                node_2_status = "Offline"

            time.sleep(10)

            # Navigate to firmware page to upload firmware
            chrome_driver.refresh()
            time.sleep(5)
            navigate_to_firmware_page()
            time.sleep(10)

            # Choose firmware file
            chrome_driver.switch_to_frame(0)
            chrome_driver.find_element_by_id("df_mesh_image").click()
            time.sleep(5)

            # Write path for firmware files
            keyboard.write(r"C:\Users\Amitabh.Mishra\Documents\Mesh_530\{}".format(firmware_files[switch%2]))
            time.sleep(2)

            keyboard.press_and_release("return")
            time.sleep(5)

            # Cick uppload firmware file button
            chrome_driver.find_element(By.ID, "MeshUploadButton").click()
            time.sleep(15)

            # Get current firmware versions
            if chrome_driver.find_elements(By.CSS_SELECTOR, ".tbl-striped-even:nth-child(2) > .undefined:nth-child(7)"):
                controller_firmware =  chrome_driver.find_element(By.CSS_SELECTOR, ".tbl-striped-even:nth-child(2) > .undefined:nth-child(7)").text
            else:
                controller_firmware = "Controller Firmware N/A"

            if chrome_driver.find_elements(By.CSS_SELECTOR, ".tbl-striped-even:nth-child(4) > .undefined:nth-child(7)"):
                node_1_firmware = chrome_driver.find_element(By.CSS_SELECTOR, ".tbl-striped-even:nth-child(4) > .undefined:nth-child(7)").text
            else:
                node_1_firmware = "Node 1 Firmware N/A"
            
            if chrome_driver.find_elements(By.CSS_SELECTOR, ".tbl-striped-odd > .undefined:nth-child(7)"):
                node_2_firmware = chrome_driver.find_element(By.CSS_SELECTOR, ".tbl-striped-odd > .undefined:nth-child(7)").text
            else:
                node_2_firmware = "Node 2 Firmware N/A"

            currentDateTime = str(datetime.datetime.now().strftime("%m/%d/%Y | %H:%M:%S"))

            # Check uploaded firmware version
            uploaded_firmware_version = chrome_driver.find_element(By.CSS_SELECTOR, "#tbl_meshImageInfo .tbl-value:nth-child(1)").text
            print(currentDateTime + " -- Selected Firmware Version: " + uploaded_firmware_version[8:-4])
            print(currentDateTime + " -- Selected Firmware Version: " + uploaded_firmware_version[8:-4], file = outputFile)

            # Print mesh device firmware versions to terminal
            print("Current Firmware Versions: ")
            print("Controller firmware: " + controller_firmware + " | Controller status: " + controller_status)
            print("Node 1 firmware: " + node_1_firmware + " | Node 1 status: " + node_1_status)
            print("Node 2 firmware: " + node_2_firmware + " | Node 2 status: " + node_2_status)

            currentDateTime = str(datetime.datetime.now().strftime("%m/%d/%Y | %H:%M:%S"))

            # Print mesh device firmware versions to file
            print(currentDateTime + " -- Current Firmware Versions:", file = outputFile)
            print("                 Controller firmware: " + controller_firmware + " | Controller status: " + controller_status, file = outputFile)
            print("                 Node 1 firmware: " + node_1_firmware + " | Node 1 status: " + node_1_status, file = outputFile)
            print("                 Node 2 firmware: " + node_2_firmware + " | Node 2 status: " + node_2_status, file = outputFile)

            time.sleep(10)

            # Change values to strings
            controller_firmware = str(controller_firmware)
            node_1_firmware = str(node_1_firmware)
            node_2_firmware = str(node_2_firmware)
            uploaded_firmware_version = str(uploaded_firmware_version)

            currentDateTime = str(datetime.datetime.now().strftime("%m/%d/%Y | %H:%M:%S"))

            if ((controller_firmware == uploaded_firmware_version) and (node_1_firmware == uploaded_firmware_version) and (node_2_firmware == uploaded_firmware_version)) or ((controller_firmware != uploaded_firmware_version) and (node_1_firmware != uploaded_firmware_version) and (node_2_firmware != uploaded_firmware_version)):
                print(currentDateTime + " -- Updating all...")
                print(currentDateTime + " -- Updating all...", file = outputFile)
                chrome_driver.find_element(By.CSS_SELECTOR, "#hidemeshbutton > input:nth-child(1)").click()
                time.sleep(5)
                chrome_driver.find_element(By.CSS_SELECTOR, "#msg-buton > input:nth-child(1)").click() # Upgrade all 
                # time.sleep(420)

                # # Click here when AP is ready
                # chrome_driver.switch_to_frame(0)
                # chrome_driver.find_element(By.CSS_SELECTOR, "a > font").click()
                # time.sleep(10)

            # # Select to upgrade Controller
            # if controller_firmware != uploaded_firmware_version:
            #     chrome_driver.find_element(By.CSS_SELECTOR, "#df_en_0 .onoffswitch-switch").click()
            #     currentDateTime = str(datetime.datetime.now().strftime("%m/%d/%Y | %H:%M:%S"))
            #     print(currentDateTime + " -- Controller updating...")
            #     time.sleep(5)
                
            # # Select to upgrade Node 1
            # if node_1_firmware != uploaded_firmware_version:
            #     chrome_driver.find_element(By.CSS_SELECTOR, "#df_en_2 .onoffswitch-switch").click()
            #     currentDateTime = str(datetime.datetime.now().strftime("%m/%d/%Y | %H:%M:%S"))
            #     print(currentDateTime + " -- Node 1 updating...")
            #     time.sleep(5)
            
            # # Select to upgrade Node 2
            # if node_2_firmware != uploaded_firmware_version:
            #     chrome_driver.find_element(By.CSS_SELECTOR, "#df_en_1 .onoffswitch-switch").click()
            #     currentDateTime = str(datetime.datetime.now().strftime("%m/%d/%Y | %H:%M:%S"))
            #     print(currentDateTime + " -- Node 2 updating...")
            #     time.sleep(5)
            
            # # Click upgrade button
            # chrome_driver.find_element(By.CSS_SELECTOR, "input:nth-child(4)").click() 

            currentDateTime = str(datetime.datetime.now().strftime("%m/%d/%Y | %H:%M:%S"))

            print(currentDateTime + " -- Update in progress...")
            print(currentDateTime + " -- Update in progress... ", file = outputFile)

            time.sleep(360)

            currentDateTime = str(datetime.datetime.now().strftime("%m/%d/%Y | %H:%M:%S"))

            print(currentDateTime + " -- Update from " + controller_firmware + " to " + uploaded_firmware_version + " Successful!\n")
            print(currentDateTime + " -- Update from " + controller_firmware + " to " + uploaded_firmware_version + " Successful!\n", file = outputFile)

            # Click here when AP is ready
            chrome_driver.switch_to_frame(0)
            chrome_driver.find_element(By.CSS_SELECTOR, "a > font").click()
            time.sleep(10)

            # Refresh the page 
            chrome_driver.refresh()
            time.sleep(5)

            print("RE-LOGGING IN\n")

            chrome_driver.execute_script("window.open('http://{}/cgi-bin/luci', 'new_window')".format(controller_IP))
            time.sleep(10)
            chrome_driver.switch_to_window(chrome_driver.window_handles[1])
            time.sleep(10)
            
            default_login()
            time.sleep(5)

            currentDateTime = str(datetime.datetime.now().strftime("%m/%d/%Y | %H:%M:%S"))

            # If the change_login element is found, change password 
            if chrome_driver.find_elements_by_id("fun_2_3"): 
                print(currentDateTime + " -- Controller Defaulted")
                print(currentDateTime + " -- Controller Defaulted", file = outputFile)
                default_counter = default_counter + 1
            elif chrome_driver.find_elements_by_id("user"):
                login()
                print(currentDateTime + " Controller Not Defaulted")
                print(currentDateTime + " Controller Not Defaulted", file = outputFile)

            # Get node status after update
            navigate_to_wifi_setup_page()
            time.sleep(15)
            chrome_driver.switch_to.frame(0)

            if chrome_driver.find_elements(By.CSS_SELECTOR, "#mesh_status_0 strong"):
                controller_status_au = chrome_driver.find_element(By.CSS_SELECTOR, "#mesh_status_0 strong").text
            else:
                controller_status_au = "Offline"
            
            if chrome_driver.find_elements(By.CSS_SELECTOR, "#mesh_status_2 strong"):
                node_1_status_au = chrome_driver.find_element(By.CSS_SELECTOR, "#mesh_status_2 strong").text
            else:
                node_1_status_au = "Offline"

            if chrome_driver.find_elements(By.CSS_SELECTOR, "#mesh_status_1 strong"):
                node_2_status_au = chrome_driver.find_element(By.CSS_SELECTOR, "#mesh_status_1 strong").text
            else:
                node_2_status_au = "Offline"

            # Print mesh device status after update to terminal
            print(currentDateTime + " -- Status update after update:")
            print("         Controller status: " + controller_status_au)
            print("         Node 1 status: " + node_1_status_au)
            print("         Node 2 status: " + node_2_status_au + "\n")

            # Print mesh device status after update to file
            print(currentDateTime + " -- Status update after update:", file = outputFile)
            print("         Controller status: " + controller_status_au, file = outputFile)
            print("         Node 1 status: " + node_1_status_au, file = outputFile)
            print("         Node 2 status: " + node_2_status_au + "\n", file = outputFile)

            time.sleep(10)

            # Close second controller window
            chrome_driver.close()
            chrome_driver.switch_to_window(chrome_driver.window_handles[0])
            time.sleep(10)

            currentDateTime = str(datetime.datetime.now().strftime("%m/%d/%Y | %H:%M:%S"))

            print(currentDateTime + " - Node 1 status after update: " + node_1_status_au + "...")
            print(currentDateTime + " - Node 2 status after update: " + node_2_status_au + "...\n")
            print(currentDateTime + " - Node 1 status after update: " + node_1_status_au + "...", file = outputFile)
            print(currentDateTime + " - Node 2 status after update: " + node_2_status_au + "...\n", file = outputFile)

            node_1_status_au = str(node_1_status_au)
            node_2_status_au = str(node_2_status_au)

            # Check controller/node status before going through node check
            if node_1_status_au == "Online" and node_2_status_au == "Online":
                print("Node 1 and Node 2 are online.")
                node_1_default_check()
                node_2_default_check()            
            elif node_1_status_au == "Offline" and node_2_status_au == "Online":
                print("Node 1 is offline. Node 2 is online.")
                node_2_default_check()
            elif node_2_status_au == "Offline" and node_1_status_au == "Online:":
                print("node 2 is offline. Node 1 is online.")
                node_1_default_check()

            chrome_driver.refresh()

            # Counter for successful upgrade / downgrade
            upgrade_counter = upgrade_counter + 1
            downgrade_counter = downgrade_counter + 1

            total_loops = (upgrade_counter + downgrade_counter) / 2

            currentDateTime = str(datetime.datetime.now().strftime("%m/%d/%Y | %H:%M:%S"))

            print("Loop Ended: " + currentDateTime)
            print("Loop Ended: " + currentDateTime + "\n", file = outputFile)

            print("Successful upgrades: " + str(upgrade_counter))
            print("Successful upgrades: " + str(upgrade_counter), file = outputFile)
            print("successful downgrades: " + str(downgrade_counter))
            print("Successful downgrades: " + str(downgrade_counter), file = outputFile)

            print("Defaults: " + str(default_counter))
            print("Defaults: " + str(default_counter), file = outputFile)
            print("Failed: " + str(failed_counter))
            print("Failed: " + str(failed_counter), file = outputFile)

            outputFile.close()

total_loops = (upgrade_counter + downgrade_counter) / 2

# Change int for counters to strings
upgrade_downgrade_loops = str(upgrade_downgrade_loops)
upgrade_counter = str(upgrade_counter)
downgrade_counter = str(downgrade_counter)
failed_counter = str(failed_counter)
default_counter = str(default_counter)
total_loops = str(total_loops)

currentDateTime = str(datetime.datetime.now().strftime("%m/%d/%Y | %H:%M:%S"))

# Print test results
outputFile = open(output_file_path, "a+")

print("****************************************************************************************************", file = outputFile)
print("TEST RESULTS:", file = outputFile)
print("****************************************************************************************************\n", file = outputFile)

print("Test Ended: " + currentDateTime + "\n", file = outputFile)

print("Successful Upgrades: " + upgrade_counter + "/" + upgrade_counter, file = outputFile)
print("Successful Downgrades: " + downgrade_counter + "/" + downgrade_counter, file = outputFile)

print("Failed Upgrades: " + failed_counter + "/" + total_loops, file = outputFile)

print("Upgrade Defaults: " + default_counter + "/" + total_loops, file = outputFile)

print("", file = outputFile)

# Close the file 
print("Test Ended!")
outputFile.close()
