"""Telegram Web App authentication and authorization."""
import hashlib
import hmac
import logging
from typing import Optional
from urllib.parse import parse_qs

from fastapi import HTTPException, Header

from api.config import config

logger = logging.getLogger(__name__)


def validate_telegram_web_app_data(init_data: str) -> dict:
    """
    Validate Telegram Web App initData.
    
    Args:
        init_data: The initData string from Telegram Web App
        
    Returns:
        dict: Parsed user data if valid
        
    Raises:
        HTTPException: If validation fails
    """
    try:
        # Parse the init data
        parsed_data = parse_qs(init_data)
        
        # Extract hash and other data
        received_hash = parsed_data.get("hash", [None])[0]
        if not received_hash:
            raise HTTPException(status_code=401, detail="Missing hash in initData")
        
        # Remove hash from data for verification
        data_check_string_parts = []
        for key, values in sorted(parsed_data.items()):
            if key != "hash":
                for value in values:
                    data_check_string_parts.append(f"{key}={value}")
        
        data_check_string = "\n".join(data_check_string_parts)
        
        # Create secret key
        secret_key = hmac.new(
            key=b"WebAppData",
            msg=config.bot_token.encode(),
            digestmod=hashlib.sha256
        ).digest()
        
        # Calculate hash
        calculated_hash = hmac.new(
            key=secret_key,
            msg=data_check_string.encode(),
            digestmod=hashlib.sha256
        ).hexdigest()
        
        # Verify hash
        if calculated_hash != received_hash:
            raise HTTPException(status_code=401, detail="Invalid initData hash")
        
        # Parse user data
        user_data = {}
        if "user" in parsed_data:
            import json
            user_json = parsed_data["user"][0]
            user_data = json.loads(user_json)
        
        return user_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error validating initData: {e}", exc_info=True)
        raise HTTPException(status_code=401, detail="Invalid initData")


async def get_current_user(
    authorization: Optional[str] = Header(None)
) -> dict:
    """
    Dependency to get current user from Telegram Web App initData.
    
    Args:
        authorization: Authorization header containing initData
        
    Returns:
        dict: User data
        
    Raises:
        HTTPException: If authentication fails
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    
    # The authorization header should contain the raw initData
    init_data = authorization
    user_data = validate_telegram_web_app_data(init_data)
    
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid user data")
    
    return user_data
