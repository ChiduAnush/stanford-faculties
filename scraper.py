from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import csv
import time

# Function to scrape faculty data from the faculty page
def scrape_faculty_data(driver, faculty_link):
    driver.execute_script("window.open('', '_blank');")  # Open a new tab
    driver.switch_to.window(driver.window_handles[1])  # Switch to the new tab
    driver.get(faculty_link)

    # Wait for the faculty page to load (you may need to adjust the waiting time)
    time.sleep(2)

    # Extract faculty data
    faculty_data = {'Name': driver.find_element(By.XPATH, '//some_xpath_for_name').text}

    # Check if email is available
    email_element = driver.find_element(By.XPATH, '//some_xpath_for_email')
    faculty_data['Email'] = email_element.text if email_element else ''

    # Check if personal website link is available
    website_element = driver.find_element(By.XPATH, '//some_xpath_for_website')
    faculty_data['Website'] = website_element.get_attribute('href') if website_element else ''

    driver.close()  # Close the current tab
    driver.switch_to.window(driver.window_handles[0])  # Switch back to the original tab

    return faculty_data

# Set up Chrome WebDriver (replace 'path/to/chromedriver' with the actual path)
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')  # Run Chrome in headless mode (without opening a visible window)
driver = webdriver.Chrome(executable_path='path/to/chromedriver', options=chrome_options)

# URL of the page to scrape
url = 'https://med.stanford.edu/neurology/faculty/overview.html'
driver.get(url)

# Wait for the page to load (you may need to adjust the waiting time)
time.sleep(2)

# Main loop to scrape data for each faculty member
faculty_data_list = []

# Xpath pattern for faculty members
xpath_pattern = '//*[@id="mainContent"]/div/div[1]/div/div[3]/div/div[{}]/div/div/div/div[2]/p/a'

# Find the total number of faculty members (you may need to adjust the range)
total_faculty_members = 200

for i in range(1, total_faculty_members + 1):
    xpath = xpath_pattern.format(i)
    try:
        faculty_link = driver.find_element(By.XPATH, xpath).get_attribute('href')
        faculty_data = scrape_faculty_data(driver, faculty_link)
        faculty_data_list.append(faculty_data)
    except Exception as e:
        print(f"Error processing faculty #{i}: {str(e)}")



# Write data to CSV
csv_file_path = 'faculty_data.csv'
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    headers = ['Name', 'Email', 'Website']
    writer = csv.DictWriter(csv_file, fieldnames=headers)

    # Write headers
    writer.writeheader()

    # Write faculty data to the CSV file
    for faculty_data in faculty_data_list:
        writer.writerow(faculty_data)

print(f'Data successfully written to {csv_file_path}.')

# Close the WebDriver
driver.quit()
