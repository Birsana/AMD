from bs4 import BeautifulSoup
import requests
from datetime import datetime

dates = []

url1 = "http://ir.amd.com/financial-information/sec-filings?field_nir_sec_form_group_target_id%5B%5D=496&field_nir_sec_" \
      "date_filed_value=&items_per_page=50#views-exposed-form-widget-sec-filings-table"
url2 = "http://ir.amd.com/financial-information/sec-filings?field_nir_sec_form_group_target_id%5B496%5D=496&field_" \
       "nir_sec_date_filed_value=&items_per_page=50&page=1"

def scrape(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    table = soup.findAll("td")

    getTextArray = []
    for item in table:
        text=item.get_text()
        getTextArray.append(text)


    for i in range(len(getTextArray)-1):
        if getTextArray[i+1].strip() == "10-Q":
            dates.append(getTextArray[i])

scrape(url1)
scrape(url2)

for i in range(len(dates)):
    dates[i] = dates[i].rstrip()
    dates[i] = dates[i].replace("Jan", "January")
    dates[i] = dates[i].replace("Feb", "February")
    dates[i] = dates[i].replace("Mar", "March")
    dates[i] = dates[i].replace("Apr", "April")
    dates[i] = dates[i].replace("Jul", "July")
    dates[i] = dates[i].replace("Aug", "August")
    dates[i] = dates[i].replace("Oct", "October")
    dates[i] = dates[i].replace("Nov", "November")
    dates[i] = dates[i].replace("Dec", "December")
    dateFormat = "%B %d, %Y"
    dates[i] = datetime.strptime(dates[i], dateFormat)



earningDates = dates