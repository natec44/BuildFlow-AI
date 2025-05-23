from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import requests
from jose import jwt
from functools import lru_cache

app = FastAPI()
bearer_scheme = HTTPBearer()

AUTH0_DOMAIN = "dev-7d8ppk5jqirxkzaf.us.auth0.com"
API_AUDIENCE = "YOUR_AUDIENCE"
ALGORITHMS = ["RS256"]

@lru_cache
def get_jwks():
    jwks_url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
    return requests.get(jwks_url).json()

def verify_jwt(token: str):
    jwks = get_jwks()["keys"]
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    for key in jwks:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
            }
    if not rsa_key:
        raise HTTPException(status_code=401, detail="Invalid header")
    try:
        payload = jwt.decode(token, rsa_key, algorithms=ALGORITHMS, audience=API_AUDIENCE, issuer=f"https://{AUTH0_DOMAIN}/")
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="Token is invalid or expired")

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    return verify_jwt(credentials.credentials)

@app.get("/api/protected")
def protected_route(user=Depends(get_current_user)):
    return {"msg": "You are authenticated!", "user": user}
