import requests

class RestCountriesTools:
    @staticmethod
    def get_country_info(name):
        url = f"https://restcountries.com/v3.1/name/{name}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print('Error while retrieving data from RestCountries API')
            return None
