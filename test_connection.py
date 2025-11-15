from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable, AuthError
from dotenv import load_dotenv
import os
import logging

# Load environment variables from .env file
load_dotenv()

# Neo4j configuration
uri = os.getenv('NEO4J_URI')
username = os.getenv('NEO4J_USERNAME')
password = os.getenv('NEO4J_PASSWORD')

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Print environment variables to check if they are loaded correctly
logger.info(f"URI: {uri}")
logger.info(f"Username: {username}")

# Initialize Neo4j driver with correct settings
def get_driver():
    try:
        driver = GraphDatabase.driver(uri, auth=(username, password))
        return driver
    except Exception as e:
        logger.error("Error initializing driver: %s", e)
        return None

driver = get_driver()

def test_connection():
    if driver is None:
        logger.error("Failed to initialize driver")
        return
    
    try:
        with driver.session() as session:
            result = session.run("RETURN 1")
            for record in result:
                logger.info(record)
    except ServiceUnavailable as e:
        logger.error("Service unavailable: %s", e)
    except AuthError as e:
        logger.error("Authentication error: %s", e)
    except Exception as e:
        logger.error("An error occurred: %s", e)
    finally:
        driver.close()

if __name__ == "__main__":
    test_connection()
