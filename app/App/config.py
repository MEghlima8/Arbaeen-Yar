import os
from dotenv import load_dotenv
load_dotenv()

configs = {
    
    'SYSTEM_NAME' : os.getenv('SYSTEM_NAME') , 
    'DOMAIN_ADDRESS' : os.getenv('DOMAIN_ADDRESS') ,
    
    'TARGET_API_URL' : os.getenv('TARGET_API_URL') ,

    'HOST' : os.getenv('HOST') , 
    'PORT' : os.getenv('PORT') , 
    'SECRET_KEY' : os.getenv('SECRET_KEY') ,
    'SEND_FILE_MAX_AGE_DEFAULT' : os.getenv('SEND_FILE_MAX_AGE_DEFAULT') ,

    # API Info
    'API_USERNAME' : os.getenv('API_USERNAME') ,
    'API_PASSWORD' : os.getenv('API_PASSWORD') ,
    
    # Database 
    'DB_NAME' : os.getenv('DB_NAME') ,
    'DB_HOST' : os.getenv('DB_HOST') ,
    'DB_USER' : os.getenv('DB_USER') ,
    'DB_PASSWORD' : os.getenv('DB_PASSWORD') ,
    'DB_PORT' : os.getenv('DB_PORT') ,
            
    # Users files
    'UPLOAD_USER_FILE' : os.getenv('UPLOAD_USER_FILE') ,
        
    # Docker Compose
    'RABBITMQ_SERVICE_NAME': os.getenv('RABBITMQ_SERVICE_NAME') , 
    
    # Bot
    'BOT_TOKEN': os.getenv('BOT_TOKEN') ,
    'BASE_URL': os.getenv('BASE_URL') ,
    'BASE_FILE_URL': os.getenv('BASE_FILE_URL') ,
    
    # Help the user how to send to the file. the file format is gif
    'HELP_USER_SEND_FILE': os.getenv('HELP_USER_SEND_FILE'),
}