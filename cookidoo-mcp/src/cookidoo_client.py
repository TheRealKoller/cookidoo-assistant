from cookidoo_api import Cookidoo
from src.logging_config import logger
import os

class CookidooConnection:
    def __init__(self):
        self._client = None
        self._email = os.getenv("COOKIDOO_EMAIL")
        self._password = os.getenv("COOKIDOO_PASSWORD")
        
        if not self._email or not self._password:
            raise ValueError("COOKIDOO_EMAIL and COOKIDOO_PASSWORD must be set")
    
    async def connect(self):
        if self._client:
            return self._client
        
        logger.info(f"Connecting to Cookidoo API with user {self._email}")
        self._client = Cookidoo()
        await self._client.login(self._email, self._password)
        logger.info("Successfully connected to Cookidoo API")
        return self._client
    
    async def disconnect(self):
        if self._client:
            logger.info("Disconnecting from Cookidoo API")
            # cookidoo_api doesn't have explicit disconnect
            self._client = None
    
    @property
    def client(self):
        if not self._client:
            raise RuntimeError("Not connected. Call connect() first")
        return self._client

cookidoo_connection = CookidooConnection()
