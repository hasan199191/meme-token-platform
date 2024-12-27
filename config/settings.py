from dotenv import load_dotenv
import os

load_dotenv()

# Algorand testnet settings
ALGORAND_ALGOD_ADDRESS = "https://testnet-api.algonode.cloud"
ALGORAND_ALGOD_TOKEN = ""
ALGORAND_INDEXER_ADDRESS = "https://testnet-idx.algonode.cloud"
ALGORAND_INDEXER_TOKEN = ""

# Move sensitive data to .env file
DEBUG = os.getenv("DEBUG", "True").lower() == "true"