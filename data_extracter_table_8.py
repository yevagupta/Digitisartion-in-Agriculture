from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException, UnexpectedAlertPresentException
import time

driver = webdriver.Chrome()
driver.get("https://inputsurvey.da.gov.in/districttables.aspx")

wait = WebDriverWait(driver, 15)  # wait up to 15 seconds

# Wait for year dropdown to load
wait.until(EC.presence_of_element_located((By.NAME, "_ctl0:ContentPlaceHolder2:ddlYear")))

category = driver.find_element(By.NAME, "_ctl0:ContentPlaceHolder2:ddlYear")
all_options = category.find_elements(By.TAG_NAME, "option")

for year_index in range(4,len(all_options)):
    category = driver.find_element(By.NAME, "_ctl0:ContentPlaceHolder2:ddlYear")
    all_options = category.find_elements(By.TAG_NAME, "option")
    all_options[year_index].click()

    table = driver.find_element(By.NAME, "_ctl0:ContentPlaceHolder2:ddlTables")
    table.click()
    extract_table_8 = table.find_element(By.XPATH, "//option[@value='30']")
    extract_table_8.click()

    wait.until(EC.presence_of_element_located((By.NAME, "_ctl0:ContentPlaceHolder2:ddlStates")))

    subcat = driver.find_element(By.NAME, "_ctl0:ContentPlaceHolder2:ddlStates")
    all_option_subcat = subcat.find_elements(By.TAG_NAME, "option")

    for state_index in range(33,len(all_option_subcat)):

        try:
            subcat = driver.find_element(By.NAME, "_ctl0:ContentPlaceHolder2:ddlStates")
            all_option_subcat = subcat.find_elements(By.TAG_NAME, "option")
            all_option_subcat[state_index].click()
            wait.until(EC.presence_of_element_located((By.NAME, "_ctl0:ContentPlaceHolder2:ddldistrict")))
        except UnexpectedAlertPresentException:
            continue

        district = driver.find_element(By.NAME, "_ctl0:ContentPlaceHolder2:ddldistrict")
        district_options = district.find_elements(By.TAG_NAME, "option")

        for district_index in range(len(district_options)):
            district = driver.find_element(By.NAME, "_ctl0:ContentPlaceHolder2:ddldistrict")
            district_options = district.find_elements(By.TAG_NAME, "option")
            district_options[district_index].click()

            wait.until(EC.presence_of_element_located((By.NAME, "_ctl0:ContentPlaceHolder2:ddlTables")))

            # table = driver.find_element(By.NAME, "_ctl0:ContentPlaceHolder2:ddlTables")
            # table.click()
            # extract_table_8 = table.find_element(By.XPATH, "//option[@value='30']")
            # extract_table_8.click()

            button = driver.find_element(By.NAME, "_ctl0:ContentPlaceHolder2:cmdSubmit")
            button.click()

            # wait.until(EC.presence_of_element_located((By.CLASS_NAME, "DisabledLink")))
            time.sleep(7)

            export_button = driver.find_element(By.CLASS_NAME, "ExportLink")
            export_button.click()

            wait.until(EC.presence_of_element_located((By.XPATH, "//div//a[@title='CSV (comma delimited)']")))

            csv_file = driver.find_element(By.XPATH, "//div//a[@title='CSV (comma delimited)']")
            csv_file.click()

            # Wait a bit for download to initiate
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "btnBack")))

            back_button = driver.find_element(By.NAME, "btnBack")
            back_button.click()

            wait.until(EC.presence_of_element_located((By.NAME, "_ctl0:ContentPlaceHolder2:ddlYear")))

driver.close()