from dotenv import load_dotenv
import os
import logging

load_dotenv()
# Set up logging
log_file_path = 'logs/app.log'
logger = logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filename=log_file_path, filemode='a')

