import requests

class NBPTools:
    @staticmethod
    def get_exchange_rates(table, code = ''):   
        url = f"http://api.nbp.pl/api/exchangerates/tables/{table}/"
        if code != '':
            url = f"http://api.nbp.pl/api/exchangerates/rates/{table}/{code}"
            
        print(url)
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print('Error while retrieving data from NBP API')
            print(response.text)
            print(response.status_code)
            return None
