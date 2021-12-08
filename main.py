import os
import sys
import datetime
from termcolor import colored, cprint # Impor termcolor modules
from dotenv import load_dotenv as LoadDotEnv # Impor env modules
LoadDotEnv() # Load env data
import app.home as home # Impor home file

# Deklarasi variabel dari env
APP_BRAND_NAME = os.getenv('APP_BRAND_NAME')
APP_BRAND_ADDRESS = os.getenv('APP_BRAND_ADDRESS')
APP_BRAND_EMAIL = os.getenv('APP_BRAND_EMAIL')
APP_BRAND_PHONE_NUMBER = os.getenv('APP_BRAND_PHONE_NUMBER')

# Load main menu

os.system('cls')
home.MenuMain()