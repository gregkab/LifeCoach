# api/utils/helpers.py

import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )

logger = logging.getLogger(__name__)

# Initialize logging when the module is imported
setup_logging()