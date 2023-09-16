import os
from dotenv import load_dotenv
load_dotenv()

configs = {
    'SYSTEM_NAME' : os.getenv('SYSTEM_NAME') , 
    'CLIENT_SERVICE_NAME' : os.getenv('CLIENT_SERVICE_NAME') ,
    'DOMAIN_ADDRESS' : os.getenv('DOMAIN_ADDRESS') ,

    'HOST' : os.getenv('HOST') , 
    'PORT' : os.getenv('PORT') , 
    'SECRET_KEY' : os.getenv('SECRET_KEY') ,
    'SEND_FILE_MAX_AGE_DEFAULT' : os.getenv('SEND_FILE_MAX_AGE_DEFAULT') ,
    
    # Database 
    'DB_NAME' : os.getenv('DB_NAME') ,
    'DB_HOST' : os.getenv('DB_HOST') ,
    'DB_USER' : os.getenv('DB_USER') ,
    'DB_PASSWORD' : os.getenv('DB_PASSWORD') ,
    'DB_PORT' : os.getenv('DB_PORT') ,
    
    'RABBITMQ_SERVICE_NAME': os.getenv('RABBITMQ_SERVICE_NAME') ,
    
    # Bot
    'BOT_TOKEN': os.getenv('BOT_TOKEN') ,
    'BASE_URL': os.getenv('BASE_URL') ,
    'BASE_FILE_URL': os.getenv('BASE_FILE_URL') ,
    
    'UPLOAD_USER_FILE': os.getenv('UPLOAD_USER_FILE'),
    'UPLOAD_TEMP_FILE': os.getenv('UPLOAD_TEMP_FILE'),
}