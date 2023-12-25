from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import csv
import time


driver = webdriver.Chrome()

url = "https://med.stanford.edu/neurology/faculty/overview.html"
driver.get(url)

time.sleep(2)


# modified_xpath_pattern = '//*[@id="mainContent"]/div/div[1]/div/div[{}]/div/div[{}]/div/div/div/div[2]/p/text()[1]'

modified_xpath = '//*[@id="mainContent"]/div/div[1]/div/div[30]/div/div[2]/div/div/div/div[2]/p'

faculty_name = driver.find_element(By.XPATH, modified_xpath + '/.').text

print(faculty_name)
