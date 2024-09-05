from dotenv import load_dotenv
import os
import logging

load_dotenv()

# Set up logging
# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Go up one level to the 'src' directory
src_dir = os.path.dirname(current_dir)
# Create the logs directory if it doesn't exist
logs_dir = os.path.join(src_dir, 'logs')
os.makedirs(logs_dir, exist_ok=True)
# Set the log file path
log_file_path = os.path.join(logs_dir, 'app.log')

# Set up the logger
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                    filename=log_file_path, 
                    filemode='a')

# Create a logger object
logger = logging.getLogger(__name__)

