import os, hashlib, hmac, secrets, time
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from .db import get_db
from .models import User
SECRET=os.getenv("JWT_SECRET","dev-only-change-this-secret-before-deploy")
ALGORITHM="HS256"
security=HTTPBearer(auto_error=False)
def hash_password(password:str)->str:
    salt=secrets.token_bytes(16)
    digest=hashlib.pbkdf2_hmac("sha256",password.encode(),salt,310000)
    return salt.hex()+":"+digest.hex()
def verify_password(password:str,stored:str)->bool:
    try:
        salt_hex,digest_hex=stored.split(":")
        actual=hashlib.pbkdf2_hmac("sha256",password.encode(),bytes.fromhex(salt_hex),310000)
        return hmac.compare_digest(actual,bytes.fromhex(digest_hex))
    except Exception: return False
def create_token(user:User)->str:
    return jwt.encode({"sub":str(user.id),"email":user.email,"exp":int(time.time())+86400},SECRET,algorithm=ALGORITHM)
def get_current_user(credentials:HTTPAuthorizationCredentials=Depends(security),db:Session=Depends(get_db)):
    if os.getenv("AUTH_ENABLED","false").lower()!="true": return None
    if not credentials: raise HTTPException(401,"Bearer token required")
    try:
        payload=jwt.decode(credentials.credentials,SECRET,algorithms=[ALGORITHM])
        user=db.get(User,int(payload["sub"]))
        if not user: raise ValueError("unknown user")
        return user
    except Exception: raise HTTPException(401,"Invalid or expired token")
def require_auth(user=Depends(get_current_user)):
    if os.getenv("AUTH_ENABLED","false").lower()=="true" and user is None:
        raise HTTPException(401,"Authentication required")
    return user
