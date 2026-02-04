from fastapi import Security, HTTPException
from fastapi.security.api_key import APIKeyHeader
import os

api_key_scheme = APIKeyHeader(name="x-api-key")

def verify_api_key(api_key: str = Security(api_key_scheme)):
    if api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=401)
