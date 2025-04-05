
from playwright.sync_api import sync_playwright
import pandas as pd
from datetime import datetime

#To avoid the potential of a timeout error, we will get the data in chunks of 10 years by
#changing the years in the range in the for loop below.

current_year = datetime.now().year

url_list = []
for year in range(2018, current_year):
    # Get the URL
    url = f'https://nflcombineresults.com/nflcombinedata.php?year={year}&pos=&college='
    #print(url)
    url_list.append(url)


def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.set_default_timeout(30000)

    nfl_combine_data = []

    # Get the data
    for url in url_list:
        page.goto(url)


        rows = page.locator('tbody tr').all()
        for row in rows:
            row_data = []
            cells = row.locator('td div').all()

            for cell in cells:
                data = cell.inner_text()
                row_data.append(data)
                
             
            nfl_combine_data.append(row_data)

                            
               
    browser.close()

    return nfl_combine_data

with sync_playwright() as playwright:
    nfl_combine_data = run(playwright)

# Create a DataFrame
nfl_combine_df_1 = pd.DataFrame(nfl_combine_data, columns=['Year', 'Name', 'College', 'Position', 'Height (in)', 'Weight (lbs)', 'Wonderlic', '40YD', 'Bench', 'Vertical', 'Broad Jump', 'Shuttle', '3Cone'])

nfl_combine_df_1.to_csv('nfl_combine_data_2018_2024.csv', index=False)
