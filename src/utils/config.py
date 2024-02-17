from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
APP_SECRET_KEY =os.getenv('APP_SECRET_KEY')
PORT = os.getenv('PORT', 8080)