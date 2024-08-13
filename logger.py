import logging

# Set up the logger
logger = logging.getLogger('AppLogger')
logger.setLevel(logging.DEBUG)

# Create a file handler to store logs
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)

# Create a console handler for output to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Set the log format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)
