# Import the packages
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import yagmail


# Set the Chrome options
chrome_options = Options()
chrome_options.add_argument("start-maximized") # Required for a maximized Viewport
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation', 'disable-popup-blocking']) # Disable pop-ups to speed up browsing
chrome_options.add_experimental_option("detach", True) # Keeps the Chrome window open after all the Selenium commands/operations are performed 
chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'}) # Operate Chrome using English as the main language
chrome_options.add_argument('--blink-settings=imagesEnabled=false') # Disable images
chrome_options.add_argument('--disable-extensions') # Disable extensions
chrome_options.add_argument("--headless=new") # Operate Selenium in headless mode
chrome_options.add_argument('--no-sandbox') # Disables the sandbox for all process types that are normally sandboxed. Meant to be used as a browser-level switch for testing purposes only
chrome_options.add_argument('--disable-gpu') # An additional Selenium setting for headless to work properly, although for newer Selenium versions, it's not needed anymore
chrome_options.add_argument("--window-size=1920x1080") # Set the Chrome window size to 1920 x 1080

# Instantiate a webdriver
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://vhsmitte.flexappoint.de/#/wizard/leistungen/1")

# Maximize the window
driver.maximize_window()

# Navigate to the page corresponding to the date of the iteration
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@name='service[3][active]']")))
driver.find_element(by=By.XPATH, value="//input[@name='service[3][active]']").click()
driver.find_element(by=By.XPATH, value="//button[@class='btn btn-primary btn-lg mx-1']").click()

# Click on the "Accept Cookies" button
driver.find_element(by=By.XPATH, value="//button[@class='btn btn-primary']").click()

# Wait for 3 seconds until the content is loaded
time.sleep(3)

# Loop over all months starting from the current month and going 6 months in the future
days = []
times1 = []
times2 = []
for iter in range(1, 7):
    month = driver.find_element(by=By.XPATH, value="//div[@class='vfc-top-date vfc-center']/span[1]").text.strip()
    year = driver.find_element(by=By.XPATH, value="//div[@class='vfc-top-date vfc-center']/span[2]").text.strip()
    month_year = month + " " + year

    # Check if there are available days
    available_days_web_element = driver.find_elements(by=By.XPATH, value="//span[@class='vfc-span-day vfc-hover']")

    # If there are available days, they will have the "//span[@class='vfc-span-day vfc-hover']" selector and it will be non-NULL
    if available_days_web_element != []:
        for i in available_days_web_element:
            # Append the available day to the "days" list
            days.append(i.text + f" in {month_year}")
            
            # Click on the day that has an appointment
            i.click()

            # Wait for 3 seconds until the content is loaded
            time.sleep(3)

            # Find the available times on that day
            times_web_element = driver.find_elements(by=By.XPATH, value="//div[@class='time-group-title']")
            for j in times_web_element:
                times1.append(j.text.strip())
            
            # Collapse the list so you can know the corresponding times to the given day 
            times2.append(', '.join(times1))
    
    # Proceed to the next month
    driver.find_element(by=By.XPATH, value="//div[@class='vfc-cursor-pointer']/div[@class='vfc-arrow-right']").click()

    # Pause for a moment to prevent the appearence of false dates
    time.sleep(2)
    
    # Wait until the date appears
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//div[@class='vfc-top-date vfc-center']/span")))

# Concatenate the days and times to form the full appointments
appointments = [i + " on day " + days[idx] for idx, i in enumerate(times2)]

# Close the driver
driver.quit()

# Send an E-mail
yag = yagmail.SMTP("omarmoataz6@gmail.com", oauth2_file=os.path.expanduser("~") + "/email_authentication.json")
if days != []:
    contents = [
        f"""
        VHS appointments exist. Check out this link --> https://vhsmitte.flexappoint.de/#/.
        The appointments are: {appointments}
        """
    ]
    yag.send(["omarmoataz6@gmail.com"], "VHS Appointments Were Found!!", contents)
else:
    contents = [
        f"No VHS appointments were found. Keep checking!!"
    ]
    yag.send(["omarmoataz6@gmail.com"], "No VHS Appointments Were Found. Keep Checking!!", contents)
