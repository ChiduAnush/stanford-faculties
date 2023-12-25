from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import csv
import time
from selenium.webdriver.chrome.options import Options


def scrape_faculty_data(driver, faculty_link):
    print("enter function")
    driver.execute_script("window.open('', '_blank');")  # Open a new tab
    driver.switch_to.window(driver.window_handles[1])  # Switch to the new tab

    print("switched tab")
    driver.get(faculty_link)

    time.sleep(2)

    try:
        print("enter inner try")
        faculty_email = driver.find_element(
            By.XPATH, '//*[@id="main_tabs_content_bio"]/div/div[2]/div[1]/div[1]/a'
        ).text

    except:
        print("enter inner except")
        print("ERROR WITH EMAIL")
        faculty_email = "N/A"
        print("")

    print("closed tab")
    driver.close()  # Close the current tab
    driver.switch_to.window(driver.window_handles[0])  # Switch back to the original tab

    return faculty_email


# -----------------------------------------------------------------------------


chrome_options = Options()
chrome_options.add_argument('--headless')  # Run Chrome in headless mode

# Create the WebDriver with Chrome options
driver = webdriver.Chrome(options=chrome_options)

url = "https://med.stanford.edu/neurology/faculty/overview.html"
driver.get(url)

time.sleep(2)

faculty_data_list = []

xpath_pattern = (
    '//*[@id="mainContent"]/div/div[1]/div/div[{}]/div/div[{}]/div/div/div/div[2]/p/a'
)
modified_xpath_pattern = (
    '//*[@id="mainContent"]/div/div[1]/div/div[{}]/div/div[{}]/div/div/div/div[2]/p'
)


csv_file_path = 'faculty_data.csv'
headers = ['Name', 'Education', 'Link', 'Email']

with open(csv_file_path, 'a', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=headers)
    # writer.writeheader()


    for i in range(72, 74):
        for j in range(1, 4):
            # for irregular endings in trio.
            if i == 49 and j == 3:
                continue
            if i == 53 and j == 3:
                continue
            if i == 63 and (j == 2 or j == 3):
                continue
            if i == 70 and (j == 2 or j == 3):
                continue
            if i == 73 and (j == 2 or j == 3):
                continue

            # for headings
            if i == 50 or i == 54 or i == 64 or i == 71:
                continue

            xpath = xpath_pattern.format(i, j)
            print(i, j)
            print("")

            try:
                print("enter outer try")
                faculty_name_edu = driver.find_element(By.XPATH, xpath).text

                if "," in faculty_name_edu:
                    faculty_name, faculty_edu = map(str.strip, faculty_name_edu.split(',', 1))
                else:
                    faculty_name = faculty_name_edu
                    faculty_edu = "N/A"
                faculty_link = driver.find_element(By.XPATH, xpath).get_attribute("href")
                # faculty_data_list.append(faculty_link)
                # print(faculty_name)
                # print(faculty_link)
                # print(xpath)

                # print("")

                faculty_email = scrape_faculty_data(driver, faculty_link)

                # try:
                #     print("enter inner try")
                #     faculty_email = scrape_faculty_data(driver, faculty_link)
                # except:
                #     print("enter inner except")
                #     print("")
                #     print("ERROR WITH EMAIL")
                #     faculty_email = "N/A"
                #     print("")
                #     continue

            except Exception as e:
                print("enter outer except")
                modified_xpath = modified_xpath_pattern.format(i, j)
                print(modified_xpath)
                faculty_name_edu = driver.find_element(By.XPATH, modified_xpath).text
                if "," in faculty_name_edu:
                    faculty_name, faculty_edu = map(str.strip, faculty_name_edu.split(',', 1))
                else:
                    faculty_name = faculty_name_edu
                    faculty_edu = "N/A"
                faculty_link = "N/A"
                faculty_email = "N/A"
                print(faculty_name)

            print("Good work bro")
            faculty_data = {}

            faculty_data["Name"] = faculty_name
            faculty_data["Education"] = faculty_edu
            faculty_data["Link"] = faculty_link
            faculty_data["Email"] = faculty_email

            # faculty_data_list.append(faculty_data)

            writer.writerow(faculty_data)
            print(faculty_data)


for item in faculty_data_list:
    print(item)


# 49, 2
# # secondary faculty
# //*[@id="mainContent"]/div/div[1]/div/div[50]
# //*[@id="mainContent"]/div/div[1]/div/div[50]/hgroup/h2


# 53, 2
# #instructors
# //*[@id="mainContent"]/div/div[1]/div/div[54]
# //*[@id="mainContent"]/div/div[1]/div/div[54]/hgroup/h2


# 63, 1
# #courtesy faculty
# //*[@id="mainContent"]/div/div[1]/div/div[64]
# //*[@id="mainContent"]/div/div[1]/div/div[64]/hgroup/h2


# 70,1
# #active adjunct faculty
# //*[@id="mainContent"]/div/div[1]/div/div[71]
# //*[@id="mainContent"]/div/div[1]/div/div[71]/hgroup/h2


# 73, 1
# ---


# for email:
# //*[@id="main_tabs_content_bio"]/div/div[2]/div[1]/div[1]/a

# for personal website?:
# //*[@id="main_tabs_content_bio"]/div/div[2]/div[2]/ul/li[2]/a



# csv_file_path = 'faculty_data.csv'
# headers = faculty_data_list[0].keys()

# with open(csv_file_path, 'w', newline='') as csv_file:
#     writer = csv.DictWriter(csv_file, fieldnames=headers)

#     # Write the header
#     writer.writeheader()

#     # Write the data
#     for row in faculty_data_list:
#         writer.writerow(row)
