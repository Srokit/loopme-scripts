"Download the first sample after searching on splice and then play it"

from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.action_chains import ActionChains

# Using Selenium web driver to navigate site

DRIVER_LOCATION = "/Users/srok/Dev/selenium/chromedriver_mac64/chromedriver"
SPLICE_BASE = "https://splice.com"

# WARNING: Do Not COmmit this info into a repo
USERNAME = 'srok35@gmail.com'
PASSWORD = 'mud1PQP.vdc2uzb!dph'

driver = webdriver.Chrome(DRIVER_LOCATION)

driver.get(SPLICE_BASE)
driver.find_element(By.XPATH, '//a[text()="Login"]').click()

# Wait for login page to show
sleep(7)

# On Login Page
usernameEle = driver.find_element(By.ID, 'username')
passEle = driver.find_element(By.ID, 'password')

usernameEle.send_keys('srok35@gmail.com')
passEle.send_keys('mud1PQP.vdc2uzb!dph')

driver.find_element(By.XPATH, '//button[text()="Continue"]').click()

# After login on home page

# Wait for sounds button to be available
sleep(3)

driver.find_element(By.XPATH, '//a[@data-qa="navbar-sounds"]').click()

sleep(2)

# Follow Genres -> Hip Hop
driver.find_element(By.XPATH, '//a[text()="Genres"]').click()
sleep(2)
driver.find_element(By.XPATH, '//a[contains(text(), "Hip Hop")]').click()

# Wait for search area to load
sleep(3)

# Click synth tag to filter by synths
driver.find_element(By.XPATH, '//a[contains(text(), "synth")]').click()

# Click Type to select loop type
driver.find_element(By.XPATH, '//button[span[contains(text(), "Type")]]').click()
sleep(3)
radioButton = driver.find_element(By.XPATH, '//span[input[@id="radio-0"]]')
radioButton.click()

# Click away from loop type so that it goes away
ActionChains(driver).move_to_element(radioButton).move_by_offset(-150, 0).click().perform()

# driver.find_element(By.ID, 'radio-0').click()
sleep(5)

NUM_PAGES = 5

for _ in range(NUM_PAGES):
    # While there is plus icons to click keep clicking the next one
    while len(driver.find_elements(By.XPATH, '//button[@iconname="plus"]')) > 0:
        # Now we're at a good selection of loops
        dlButton = driver.find_element(By.XPATH, '//button[@iconname="plus"]')
        ActionChains(driver).move_to_element(dlButton).pause(2).click().perform()
        sleep(1)

    # Click next page button
    driver.find_element(By.XPATH, '//button[@iconname="arrow-right"]').click()

    sleep(3)
