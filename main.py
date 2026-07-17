from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from auth import create_token, verify_token

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Temporary storage for users
users_db = {}

# This defines what a user registration looks like
class User(BaseModel):
    username: str
    password: str

@app.get("/")
def read_root():
    return {"message": "API is running"}

@app.post("/register")
def register(user: User):
    if user.username in users_db:
        return {"error": "User already exists"}
    users_db[user.username] = user.password
    return {"message": f"User {user.username} registered successfully"}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
    if username not in users_db:
        return {"error": "User not found"}
    if users_db[username] != password:
        return {"error": "Wrong password"}
    token = create_token(username)
    return {"access_token": token, "token_type": "bearer"}

@app.get("/protected")
def protected(token: str = Depends(oauth2_scheme)):
    username = verify_token(token)
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return {"message": f"Hello {username}, you accessed a protected route!"}
