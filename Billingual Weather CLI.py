import requests
import pycountry
import sys
import os
from dotenv import load_dotenv


load_dotenv()
API_KEY  = os.getenv('OPENWEATHER_API_KEY')
if not API_KEY:
    sys.exit('ERROR: OPENWEATHER_API_KEY not found')


def main():
    city = input('Which city do you want to know the weather? ')
    display_weather(city)


def validate_city(name):
    get = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={name}&limit=1&appid={API_KEY}')
    if not get.json():
        sys.exit('Not a valid city')

    local_name = get.json()[0].get('local_names', {})
    official_name = get.json()[0]['name']
    country = get.json()[0]['country']

    return local_name, official_name, country


def get_weather(official_name, country_code, lang):
    if lang == 'pt':
        api_lang = 'pt_br'
    else:
        api_lang = 'en'

    r = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={official_name},{country_code}&lang={api_lang}&appid={API_KEY}')

    if r.status_code != 200:
        raise KeyError

    data = r.json()
    temp_K = float(data['main']['temp'])
    feels_K = float(data['main']['feels_like'])
    temp_min = float(data['main']['temp_min'])
    temp_max = float(data['main']['temp_max'])
    country = data['sys']['country']

    if lang == 'pt':
        weather = data['weather'][0]['description'].title()
    else:
        weather = data['weather'][0]['main']

    return temp_K, feels_K, weather, country, temp_min, temp_max


def convert_temperature(K):
    celsius = K - 273.15
    return celsius


def get_country_names(code):
    if len(code) == 2:
        return pycountry.countries.get(alpha_2 = code).name
    if len(code) == 3:
        return pycountry.countries.get(alpha_3 = code).name


def display_weather(city):
    try:
        local_name, official_name, country_code = validate_city(city)

        user_input = city.strip().lower()

        if not local_name:
            raise KeyError

        valid_names = [official_name.lower()]
        if 'en' in local_name:
            valid_names.append(local_name['en'].lower())
        if 'pt' in local_name:
            valid_names.append(local_name['pt'].lower())

        if user_input not in valid_names:
            raise KeyError

        if 'pt' in local_name and user_input == local_name['pt'].lower():
            lang= 'pt'
            name_exibicao = local_name['pt'].upper()
        else:
            lang = 'en'
            name_exibicao = official_name.upper()

        temp_K, feels_K, weather, country, temp_min, temp_max = get_weather(official_name, country_code, lang)

        min_C = convert_temperature(temp_min)
        max_C = convert_temperature(temp_max)
        temp_C = convert_temperature(temp_K)
        feels_C = convert_temperature(feels_K)
        country_name = get_country_names(country)

        languages = {
            'en': {
                'report': 'WEATHER REPORT FOR',
                'condition': 'Condition:',
                'temp': 'Temperature:',
                'feels': 'Feels Like:',
                'min_max': 'Min / Max Temp:'
            },
            'pt': {
                'report': 'RELATÓRIO METEOROLÓGICO PARA',
                'condition': 'Condição:',
                'temp': 'Temperatura:',
                'feels': 'Sensação Térmica:',
                'min_max': 'Temp Mín / Máx:'
            }
        }
        txt = languages[lang]

        print("-" * 55)
        print(f"{txt['report']}: {name_exibicao}, {country_name}")
        print("-" * 55)
        print(f"{txt['condition']:<18}{weather}")
        print(f"{txt['temp']:<18}{temp_C:.1f}°C ({temp_K:.1f} K)")
        print(f"{txt['feels']:<18}{feels_C:.1f}°C ({feels_K:.1f} K)")
        print(f"{txt['min_max']:<18}{min_C:.1f}°C ({temp_min:.1f} K) / {max_C:.1f}°C ({temp_max:.1f} K)")
        print("-" * 55)

    except KeyError:
        sys.exit('Input a valid city')

if __name__ == "__main__":
    main()
