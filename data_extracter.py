from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException
import time

driver = webdriver.Chrome()
driver.get("https://inputsurvey.da.gov.in/districttables.aspx")

wait = WebDriverWait(driver, 15)

wait.until(EC.presence_of_element_located((By.NAME, "_ctl0:ContentPlaceHolder2:ddlYear")))

category = driver.find_element(By.NAME, "_ctl0:ContentPlaceHolder2:ddlYear")
all_options = category.find_elements(By.TAG_NAME, "option")

# Flags to resume scraping
resume_state = False
resume_district = False

for year_index in range(2, len(all_options)):
    category = driver.find_element(By.NAME, "_ctl0:ContentPlaceHolder2:ddlYear")
    all_options = category.find_elements(By.TAG_NAME, "option")
    all_options[year_index].click()

    wait.until(EC.presence_of_element_located((By.NAME, "_ctl0:ContentPlaceHolder2:ddlStates")))
    subcat = driver.find_element(By.NAME, "_ctl0:ContentPlaceHolder2:ddlStates")
    all_option_subcat = subcat.find_elements(By.TAG_NAME, "option")

    for state_index in range(len(all_option_subcat)):
        subcat = driver.find_element(By.NAME, "_ctl0:ContentPlaceHolder2:ddlStates")
        all_option_subcat = subcat.find_elements(By.TAG_NAME, "option")
        state_name = all_option_subcat[state_index].text.strip()

        # Resume from "Arunachal Pradesh"
        if not resume_state:
            if state_name == "WEST BENGAL":
                resume_state = True
            else:
                continue  # Skip earlier states

        try:
            all_option_subcat[state_index].click()
            wait.until(EC.presence_of_element_located((By.NAME, "_ctl0:ContentPlaceHolder2:ddldistrict")))
        except UnexpectedAlertPresentException:
            continue

        district = driver.find_element(By.NAME, "_ctl0:ContentPlaceHolder2:ddldistrict")
        district_options = district.find_elements(By.TAG_NAME, "option")

        for district_index in range(len(district_options)):
            district = driver.find_element(By.NAME, "_ctl0:ContentPlaceHolder2:ddldistrict")
            district_options = district.find_elements(By.TAG_NAME, "option")
            district_name = district_options[district_index].text.strip()

            # Resume after "Changlang"
            if not resume_district:
                if state_name == "WEST BENGAL" and district_name == "HOWRAH":
                    resume_district = True
                continue  # skip until we reach Changlang

            district_options[district_index].click()

            wait.until(EC.presence_of_element_located((By.NAME, "_ctl0:ContentPlaceHolder2:ddlTables")))

            table = driver.find_element(By.NAME, "_ctl0:ContentPlaceHolder2:ddlTables")
            table.click()
            extract_table_8 = table.find_element(By.XPATH, "//option[@value='33']")
            extract_table_8.click()

            button = driver.find_element(By.NAME, "_ctl0:ContentPlaceHolder2:cmdSubmit")
            button.click()

            time.sleep(7)

            try:
                export_button = driver.find_element(By.CLASS_NAME, "ExportLink")
                export_button.click()

                wait.until(EC.presence_of_element_located((By.XPATH, "//div//a[@title='CSV (comma delimited)']")))

                csv_file = driver.find_element(By.XPATH, "//div//a[@title='CSV (comma delimited)']")
                csv_file.click()

                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "btnBack")))

                back_button = driver.find_element(By.NAME, "btnBack")
                back_button.click()

                wait.until(EC.presence_of_element_located((By.NAME, "_ctl0:ContentPlaceHolder2:ddlYear")))
            except:
                print(f"⚠️ Download failed for {state_name} - {district_name}")
                driver.back()
                wait.until(EC.presence_of_element_located((By.NAME, "_ctl0:ContentPlaceHolder2:ddlYear")))

driver.close()

#Uttar Pradesh 9C
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException,
    UnexpectedAlertPresentException
)
import time

# Launch browser
driver = webdriver.Chrome()
driver.get("https://inputsurvey.da.gov.in/districttables.aspx")

wait = WebDriverWait(driver, 15)

# Wait for year dropdown and select latest year
wait.until(EC.presence_of_element_located((By.NAME, "_ctl0:ContentPlaceHolder2:ddlYear")))
category = driver.find_element(By.NAME, "_ctl0:ContentPlaceHolder2:ddlYear")
all_years = category.find_elements(By.TAG_NAME, "option")
all_years[-1].click()  # Select most recent year

# Wait for state dropdown
wait.until(EC.presence_of_element_located((By.NAME, "_ctl0:ContentPlaceHolder2:ddlStates")))
subcat = driver.find_element(By.NAME, "_ctl0:ContentPlaceHolder2:ddlStates")
all_states = subcat.find_elements(By.TAG_NAME, "option")

# Select only "Uttar Pradesh"
for state_option in all_states:
    if "Uttar Pradesh" in state_option.text:
        state_option.click()
        break

wait.until(EC.presence_of_element_located((By.NAME, "_ctl0:ContentPlaceHolder2:ddldistrict")))
district_dropdown = driver.find_element(By.NAME, "_ctl0:ContentPlaceHolder2:ddldistrict")
district_options = district_dropdown.find_elements(By.TAG_NAME, "option")

for district_index in range(len(district_options)):
    district_dropdown = driver.find_element(By.NAME, "_ctl0:ContentPlaceHolder2:ddldistrict")
    district_options = district_dropdown.find_elements(By.TAG_NAME, "option")
    district_options[district_index].click()

    # Wait for table dropdown
    wait.until(EC.presence_of_element_located((By.NAME, "_ctl0:ContentPlaceHolder2:ddlTables")))
    table_dropdown = driver.find_element(By.NAME, "_ctl0:ContentPlaceHolder2:ddlTables")
    table_dropdown.click()
    table_options = table_dropdown.find_elements(By.TAG_NAME, "option")

    # Select Table 9C by visible text
    for table_option in table_options:
        if "Table 9C" in table_option.text:
            table_option.click()
            break

    # Click Submit button
    button = driver.find_element(By.NAME, "_ctl0:ContentPlaceHolder2:cmdSubmit")
    button.click()

    time.sleep(6)  # Wait for table to load
    try:
        export_button = driver.find_element(By.CLASS_NAME, "ExportLink")
        export_button.click()

        # Wait for CSV download option
        wait.until(EC.presence_of_element_located((By.XPATH, "//div//a[@title='CSV (comma delimited)']")))
        csv_link = driver.find_element(By.XPATH, "//div//a[@title='CSV (comma delimited)']")
        csv_link.click()

        time.sleep(2)  # Small pause to ensure download

        # Go back to district selection
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "btnBack")))
        back_button = driver.find_element(By.NAME, "btnBack")
        back_button.click()
        wait.until(EC.presence_of_element_located((By.NAME, "_ctl0:ContentPlaceHolder2:ddldistrict")))
    except Exception as e:
        print(f"Error in district {district_options[district_index].text}: {e}")
        continue

driver.quit()

import pandas as pd
import os

# Use raw strings (prefix with r)
input_folder = r"C:\Users\yevag\OneDrive\Desktop\YEVA\IITK\Digitization In Agriculture\Table 9C 2006-2007"
output_folder = r"C:\Users\yevag\OneDrive\Desktop\YEVA\IITK\Digitization In Agriculture\csv"

# Loop through all Excel files in the folder
for file in os.listdir(input_folder):
    if file.endswith(".xlsx") or file.endswith(".xls"):
        file_path = os.path.join(input_folder, file)
        
        # Read Excel file
        excel_data = pd.read_excel(file_path)
        
        # Generate output CSV file path
        output_file = os.path.splitext(file)[0] + ".csv"
        output_path = os.path.join(output_folder, output_file)
        
        # Save as CSV
        excel_data.to_csv(output_path, index=False)
        print(f"Converted: {file} → {output_file}")
