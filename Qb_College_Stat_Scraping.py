
import pandas as pd
from playwright.sync_api import sync_playwright

nfl_qbs = pd.read_csv('C:/Users/james/OneDrive/Desktop/nfl_combine_qbs.csv')

baselink = 'https://www.sports-reference.com/cfb/players/{name}-1.html'

nfl_qbs['Name'] = nfl_qbs['Name'].str.lower()

def insert_dash(text):
    return '-'.join(text.split())

nfl_qbs['Name'] = nfl_qbs['Name'].apply(insert_dash)

nfl_qbs['Name'] = nfl_qbs['Name'].str.replace('.','', regex=False)

nfl_qbs['Name'] = nfl_qbs['Name'].str.replace("'", '', regex=False)



names = nfl_qbs['Name'].tolist()


qb_urls = []

for name in names:
    url = baselink.format(name=name)
    #print(url)
    qb_urls.append(url)

#URL clean up to get the proper links for qbs

qb_urls[15] = 'https://www.sports-reference.com/cfb/players/kerwin-bell-2.html' 

qb_urls[8] = 'https://www.sports-reference.com/cfb/players/bill-ransdell-2.html' 

qb_urls[78] = 'https://www.sports-reference.com/cfb/players/greg-jones-7.html'  

qb_urls[621] = 'https://www.sports-reference.com/cfb/players/josh-allen-7.html'  

qb_urls[652] = 'https://www.sports-reference.com/cfb/players/mike-white-6.html'  

qb_urls[726] = 'https://www.sports-reference.com/cfb/players/zach-wilson-3.html'  

qb_urls[768] = 'https://www.sports-reference.com/cfb/players/caleb-williams-3.html'  

qb_urls[7] = 'https://www.sports-reference.com/cfb/players/chris-miller-4.html'

qb_urls[750] = 'https://www.sports-reference.com/cfb/players/anthony-richardson-2.html'  

qb_urls[340] = 'https://www.sports-reference.com/cfb/players/alex-smith-3.html'  

qb_urls[97] = 'https://www.sports-reference.com/cfb/players/brad-johnson-2.html'

qb_urls[762] = 'https://www.sports-reference.com/cfb/players/michael-penix-jr-1.html'  

qb_urls[763] = 'https://www.sports-reference.com/cfb/players/jacob-eason-1.html'  

qb_urls[616] = 'https://www.sports-reference.com/cfb/players/mitch-trubisky-1.html' 

qb_urls[571] = 'https://www.sports-reference.com/cfb/players/jacoby-brissett-2.html'

qb_urls[25] = 'https://www.sports-reference.com/cfb/players/mike-perez-2.html'

#Additional url fixes upon futher inspection:

#https://www.sports-reference.com/cfb/players/mike-johnson-6.html
#https://www.sports-reference.com/cfb/players/jeff-blake-2.html
#https://www.sports-reference.com/cfb/players/eric-hunter-3.html
#https://www.sports-reference.com/cfb/players/steve-smith-15.html
#https://www.sports-reference.com/cfb/players/kevin-mason-2.html
#https://www.sports-reference.com/cfb/players/john-walsh-2.html
#https://www.sports-reference.com/cfb/players/dan-white-2.html
#https://www.sports-reference.com/cfb/players/jason-martin-4.html
#https://www.sports-reference.com/cfb/players/chris-mccoy-3.html
#https://www.sports-reference.com/cfb/players/anthony-wright-4.html
#https://www.sports-reference.com/cfb/players/doug-johnson-3.html
#https://www.sports-reference.com/cfb/players/paul-smith-2.html
#https://www.sports-reference.com/cfb/players/john-parker-wilson-1.html  listed as john wilson at combine
#https://www.sports-reference.com/cfb/players/thaddeus-lewis-2.html
#https://www.sports-reference.com/cfb/players/robert-griffin-iii-1.html
#https://www.sports-reference.com/cfb/players/ryan-griffin-2.html
#https://www.sports-reference.com/cfb/players/blake-sims-2.html
#https://www.sports-reference.com/cfb/players/austin-reed-2.html
#https://www.sports-reference.com/cfb/players/ryan-williams-7.html
#https://www.sports-reference.com/cfb/players/brandon-allen-2.html
#https://www.sports-reference.com/cfb/players/travis-wilson-4.html
#https://www.sports-reference.com/cfb/players/brandon-silvers-2.html
#https://www.sports-reference.com/cfb/players/nick-fitzgerald-2.html
#https://www.sports-reference.com/cfb/players/michael-penix-jr-1.html
#https://www.sports-reference.com/cfb/players/anthony-gordon-2.html
#https://www.sports-reference.com/cfb/players/jordan-love-2.html
#https://www.sports-reference.com/cfb/players/justin-fields-2.html
#https://www.sports-reference.com/cfb/players/zac-thomas-2.html
#https://www.sports-reference.com/cfb/players/zach-smith-6.html


#Scraping Code

def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.set_default_timeout(60000)

    qb_college_stats = []

    for qb in qb_urls:
        try:
            response = page.goto(qb)
            if response.status == 404:
                print(f"Page not found for URL: {qb}")
                continue

            rows = page.locator('tfoot tr').all()
            for row in rows:
                if row.get_attribute('id') != 'passing_standard.Career':
                    continue
                row_data = []
                cells = row.locator('td.right').all()

                for cell in cells:
                    data = cell.inner_text()
                    row_data.append(data)
            
            qbs_names = page.locator('h1 span').all()
            if len(qbs_names) > 0: 
                qb_name = qbs_names[0].inner_text()
                row_data.insert(0, qb_name) 
             
                qb_college_stats.append(row_data)
        except Exception as e:
            print(f"Error processing {qb}: {e}")
            continue
                            
               
    browser.close()


    return qb_college_stats

with sync_playwright() as playwright:
    qb_college_stats = run(playwright)

print(qb_college_stats)

# Create a DataFrame

nfl_qb_college_stats_df = pd.DataFrame(qb_college_stats, columns=['Name','G', 'Cmp', 'Att', 'Cmp%', 'Yds', 'TD', 'TD%', 'Int', 'Int%', 'Y/A', 'AY/A', 'Y/C', 'Y/G', 'Rate', 'Extra1', 'Extra2'])

nfl_qb_college_stats_df.to_csv('nfl_qb_college_stats.csv', index=False)

