from jose import jwt, JWTError
import datetime

# This is a secret key used to sign tokens (in a real app, keep it hidden!)
SECRET_KEY = "my-secret-key-change-this-later"
ALGORITHM = "HS256"

def create_token(username):
    # The token will expire in 30 minutes
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    data = {"sub": username, "exp": expire}
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]  # returns the username if valid
    except JWTError:
        return None  # token is invalid or expired