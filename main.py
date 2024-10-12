import time
from playwright.sync_api import sync_playwright
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
import os
import shutil
import pandas as pd
import csv

# i want to get the County,Acres (min),Acres (max) from csv in a list mean all county will be in county list and Acres (min) in acresmin list and Acres (max) will be in acresmax list



# CSV file ka path
file_path = 'readfin-market-analysis.csv'  # Isse apne CSV file ke path se badalna na bhoolen

# CSV file ko pandas DataFrame mein load karna
df = pd.read_csv(file_path)

# County, Acres (min), aur Acres (max) ko lists mein extract karna
county_list = df['County'].tolist()
acres_min_list = df['Acres (min)'].tolist()
acres_max_list = df['Acres (max)'].tolist()
State_list = df['State'].tolist()


# Lists ko print karna
print("County List:", county_list)
print("Acres (Min) List:", acres_min_list)
print("Acres (Max) List:", acres_max_list)
print("State List:", State_list)



with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir=r'C:\Users\ULC\PycharmProjects\Keepa-WebScraper-bot\data_dir',
        headless=False,
        accept_downloads=True
    )
    page = browser.new_page()

    for county, acres_min, acres_max, state in zip(county_list, acres_min_list, acres_max_list, State_list):
        print("County:", county)
        print("Acres (Min):", acres_min)
        print("Acres (Max):", acres_max)
        page.goto("https://www.redfin.com/")

        # Zoom out the browser for better visibility
        page.evaluate("document.body.style.zoom = '0.75'")

        page.fill("//input[@type='search']", f"{county} County", timeout=0)
        page.click(f"//a[@title='{county} County']", timeout=0)
        time.sleep(12)
        current_url = page.url
        print("Current URL:", current_url)

        solds_url = f"{current_url}/filter/property-type=land,min-lot-size={acres_min}-acre,max-lot-size={acres_max}-acre"
        print(solds_url)

        page.goto(solds_url, timeout=0)

        solds_xpath = page.text_content('//div[@data-rf-test-id="homes-description"]')

        # Extract the first part (before 'of')
        sold_number = solds_xpath.split(" ")[0]  # Splitting and getting the first part
        print("First number:", sold_number)

        current_url2 = page.url
        print("Current URL:", current_url2)
        pending_url = f"{current_url2},status=contingent+pending"
        print(pending_url)

        page.goto(pending_url)

        pendinghomes = page.text_content('//div[@data-rf-test-id="homes-description"]')

        # Extract the first part (before 'of')
        pendinghomes_number = pendinghomes.split(" ")[0]  # Splitting and getting the first part
        print("Pending Homes:", pendinghomes_number)

        one_month_url = f"{solds_url},include=sold-1mo"
        print(one_month_url)

        page.goto(one_month_url, timeout=0)

        onemonthhomes = page.text_content('//div[@data-rf-test-id="homes-description"]')

        # Extract the first part (before 'of')
        onemonthhomes_number = onemonthhomes.split(" ")[0]  # Splitting and getting the first part
        print("one month number:", onemonthhomes_number)

        three_months_url = f"{solds_url},include=sold-3mo"
        print(three_months_url)

        page.goto(three_months_url, timeout=0)

        threemonthshomes = page.text_content('//div[@data-rf-test-id="homes-description"]')

        # Extract the first part (before 'of')
        threemonthshomes_number = threemonthshomes.split(" ")[0]  # Splitting and getting the first part
        print("three months number:", threemonthshomes_number)

        six_months = f"{solds_url},include=sold-6mo"
        print(six_months)

        page.goto(six_months, timeout=0)

        sixmonthshomes = page.text_content('//div[@data-rf-test-id="homes-description"]')

        # Extract the first part (before 'of')
        sixmonthshomes_number = sixmonthshomes.split(" ")[0]  # Splitting and getting the first part
        print("Six Number:", sixmonthshomes_number)

        oneyear = f"{solds_url},include=sold-1yr"
        print(oneyear)

        page.goto(oneyear, timeout=0)

        oneyearhomes = page.text_content('//div[@data-rf-test-id="homes-description"]')

        # Extract the first part (before 'of')
        oneyearhomes_number = oneyearhomes.split(" ")[0]  # Splitting and getting the first part
        print("one year number:", oneyearhomes_number)

        # now i want to save everythng in a csv with csv a+ mode

        header = ["county", "state", "min-acer", "max-acer", "Sold", "Pending", "1 Month", "3 Months", "6 Months", "1 Year", "sold_url", "pending_url", "one_month_url", "three_months_url", "six_months", "oneyear"]
        with open('redfin1.csv', 'a+', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            if file.tell() == 0:  # Check if file is empty
                writer.writerow(header)
            writer.writerow([county, state, acres_min, acres_max, sold_number, pendinghomes_number, onemonthhomes_number, threemonthshomes_number, sixmonthshomes_number, oneyearhomes_number, solds_url, pending_url, one_month_url, three_months_url, six_months, oneyear])



