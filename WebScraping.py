from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 
import pandas as pd
print('Starting the browser')
#Initalisee selenium with chromedriver
driver = webdriver.Chrome()
#Navigate to the provide url
url = 'https://www.apec.fr/candidat/recherche-emploi.html/emploi?lieux=711&typesConvention=143684&typesConvention=143685&typesConvention=143686&typesConvention=143687&page=0'
driver.get(url)
#Wait for the page to load
wait = WebDriverWait(driver, 10)
job_count = 1
page = 1
jobs_post = list()
#compteur de nmbre de poste scrapinf
previous_num_post = 0
while True:
    try:
        #wait until button  suiv appears clicking
        button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "Suiv.")]'))
        )
        button.click()
        #give some time for new content to load
        time.sleep(10)
        print(f'Button click {page} times')
        page +=1
    except Exception as e:
        print(f'Error encountered: {e}')
#parse the page content with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    print('Scraping started...')
    #Loop through html source based on specifiedmdiv element
    for card in soup.find_all('div', class_='card-offer__text'):
        company = card.find('p',class_='card-offer__company').text.strip()
        titre = card.find('h2', class_='card-title').text.strip()
        description = card.find('p',class_='card-offer__description').text.strip()
        #recup les <ul> chhacun avec ses <li>
        details = card.find_all('ul', class_='details-offer')
        salary = details[0].find('img', alt='Salaire texte').parent.text.strip() if len(details)>1 else 'N/A'
        contact_type = details[1].find('img', alt='type de contrat').parent.text.strip() if len(details)>1 else 'N/A'
        location = details[1].find('img', alt='localisation').parent.text.strip() if len(details)>1 else 'N/A'
        Date = details[1].find('img', alt='date de publication').parent.text.strip() if len(details)>1 else 'N/A'
        url = card.find_parent('a')['href']
        print(f'Page {page}')
        print(f'Company:{company}\nTitle:{titre}\nContract Type:{contact_type}\nSalary:{salary}\nLocation:{location}\nDate:{Date}\nURL:{url}')

        jobs_post.append(
            {
              'Company'  : company,
              'Title' : titre,
              'Description': description,
              'Salary' : salary,
              'Contract Type' : contact_type,
              'Location' : location,
              'Date de publication' : Date,
              'URL' : url
            }
        )

        job_count+=1
    if len(jobs_post) == previous_num_post:
        print('No new posts found. Exiting loop')
        break
    previous_num_post = len(jobs_post)
    page +=1

#Convert the job_post list of dictionaries to a dataframe
df = pd.DataFrame(jobs_post)
print(f'Heads rows\n{df.head()}')
print(f'Tail rows\n{df.tail()}')
print('Saving data...')
df.to_csv('Apec.csv', index=False)
#close the browser
driver.quit()

