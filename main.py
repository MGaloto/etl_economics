from time import sleep
import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup as BS
import random
from unidecode import unidecode
from datetime import datetime
import pytz
import os
import time




class Main:
    def __init__(self) -> None:
        self.DATE = self.getDate()
        self.URL ="https://tradingeconomics.com/matrix"


    def getDate(self) -> str:
        argentina_timezone = pytz.timezone('America/Argentina/Buenos_Aires')
        utc_now = datetime.utcnow()
        argentina_now = utc_now.replace(tzinfo=pytz.utc).astimezone(argentina_timezone)
        formatted_date = argentina_now.strftime('%Y-%m-%d')
        return formatted_date
    
    
    def parseToFloatOrInt(self, data) -> any:
        if data != '' and '.' in data:
            return float(data)
        elif data != '' and '.' not in data:
            return int(data)
        else:
            return None

    def getSoup(self, url):
        user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.37",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Version/15.0.1 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36 Edg/89.0.774.57",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
        ]


        headers = {
            "User-Agent": random.choice(user_agents),
            "Accept-Language": "en-US,en;q=0.9",
        }

        sleep(random.randint(1, 2))
        response = self.getRequests(url, headers)
        soup = BS(response.content, 'html.parser')
        return soup

    def getRequests(self, url, headers):
        delay = 2
        retry = 0
        limit = 5
        while retry < limit:
            try:
                res = requests.get(url,headers=headers)
                if res.status_code == 200:
                    return res
                else:
                    print("Error: la request fue: " + str(res.status_code)+ " se sigue reintentando..")
                    time.sleep(delay * retry)
            except ConnectionError:
                print("No se puedo conectar")
                retry += 1
                continue
            break
        if retry==limit:
            raise(f"status code {str(res.status_code)}")


    def run(self):
        soup = self.getSoup(self.URL)
        table = soup.find('table', {'id': 'matrix'})

        countries = []
        gdp_values = []
        gdp_growth_values = []
        interest_rate_values = []
        inflation_rate_values = []
        jobless_rate_values = []
        gov_budget_values = []
        debt_to_gdp_values = []
        current_account_values = []
        population_values = []

        for row in table.find_all('tr')[1:]:
            columns = row.find_all('td')
            
            countries.append(columns[0].text.strip())
            gdp_values.append(self.parseToFloatOrInt(columns[1].text.strip()))
            gdp_growth_values.append(self.parseToFloatOrInt(columns[2].text.strip()))
            interest_rate_values.append(self.parseToFloatOrInt(columns[3].text.strip()))
            inflation_rate_values.append(self.parseToFloatOrInt(columns[4].text.strip()))
            jobless_rate_values.append(self.parseToFloatOrInt(columns[5].text.strip()))
            gov_budget_values.append(self.parseToFloatOrInt(columns[6].text.strip()))
            debt_to_gdp_values.append(self.parseToFloatOrInt(columns[7].text.strip()))
            current_account_values.append(self.parseToFloatOrInt(columns[8].text.strip()))
            population_values.append(self.parseToFloatOrInt(columns[9].text.strip()))

        data = {
            'country': countries,
            'gdp': gdp_values,
            'gdp_growth': gdp_growth_values,
            'interest_rate': interest_rate_values,
            'inflation_rate': inflation_rate_values,
            'jobless_rate': jobless_rate_values,
            'gov_budget': gov_budget_values,
            'debt_gdp': debt_to_gdp_values,
            'current_account': current_account_values,
            'population': population_values,
            'date' : self.DATE
        }

        df = pd.DataFrame(data)

        file_name_country_df = os.path.join('data_country_all', "paises.csv")
        if os.path.exists(file_name_country_df):
            existing_df = pd.read_csv(file_name_country_df)
            validation = self.DATE in existing_df['date'].values
            if validation == False:
                existing_df = pd.concat([existing_df, df], ignore_index=True)
                existing_df = existing_df.drop_duplicates()
                existing_df.to_csv(file_name_country_df, index=False)
        else:
            df.to_csv(file_name_country_df, index=False)

        

if __name__ == "__main__":
    app = Main()
    app.run()
    print("Fin")
