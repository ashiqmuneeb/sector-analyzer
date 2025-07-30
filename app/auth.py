from fastapi import Header, HTTPException
import logging

logger = logging.getLogger(__name__)

API_KEYS = {"testkey123"}

async def authenticate_user(x_api_key: str = Header(...)):
    if x_api_key not in API_KEYS:
        logger.warning(f"Invalid API key attempt: {x_api_key}")
        raise HTTPException(status_code=403, detail="Invalid API Key")
    logger.debug(f"Authenticated request with API key: {x_api_key[:3]}...")