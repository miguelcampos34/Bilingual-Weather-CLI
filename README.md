# Bilingual Weather CLI

#### Description
The Bilingual Weather CLI is a Python-based command-line application that provides real-time weather updates by consuming the OpenWeather API. It intelligently detects the language of the user's input—supporting both English and Portuguese—and dynamically adjusts the interface labels accordingly. The application emphasizes visual consistency, utilizing dynamic f-string padding to ensure that all terminal outputs remain perfectly aligned regardless of the language used, offering a polished and user-friendly experience for weather tracking.

This project was developed as a final submission for Harvard's CS50P (CS50's Introduction to Programming with Python).

### Features
* **Real-time Weather Data:** Fetches current weather conditions directly from the OpenWeather API.
* **Bilingual Support:** Automatically adapts the interface and labels for both English and Portuguese users.
* **Polished UI:** Uses dynamic f-string padding to keep terminal outputs clean and perfectly aligned, regardless of the language length differences.

### How to use

#### 1. Install dependencies
Run the following command in your terminal to install the required libraries:

pip install requests pycountry python-dotenv


#### 2. Configure your API key
You will need an OpenWeather API key to fetch the weather data.
1. Create a file named `.env` in the root directory of the project folder.
2. Inside the `.env` file, add your key on a new line:

OPENWEATHER_API_KEY=your_actual_api_key_here


#### 3. Run the application
Start the CLI application by running:
python project.py
