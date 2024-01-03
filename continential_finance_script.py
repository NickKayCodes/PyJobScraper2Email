from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
from mail_me import send_email
from config import gmail_password, gmail_user, recipient_email

driver = webdriver.Chrome()
driver.get("https://contfinco.bamboohr.com/careers")

time.sleep(5)
assert "BambooHR" in driver.title

elements = driver.find_elements(By.XPATH, '//li//a[@class="jss-f65"]')

if elements:
    listing_info = []
    for e in elements:
        text = e.text
        href = e.get_attribute('href')

        listing_info.append({'title': text, 'link': href})

    print("Job listing title and link:\n")
    for i in listing_info:
        print(f"Title: {i['title']}, Link: {i['link']}")

    print("------------------------------------------------------------------------------")
    pattern = re.compile(r".*Quality Assurance.*", re.IGNORECASE)

    parsed_listings = []
    for job in listing_info:
        if pattern.match(job["title"]):
            parsed_listings.append(job)
    body = "\n".join([f"Title: {job['title']}, Link: {job['link']}" for job in parsed_listings])
    send_email("Continential Finance Job Listings", body, recipient_email, gmail_user, gmail_password)
else:
    print("no elements found")

driver.quit()