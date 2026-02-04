from passlib.context import CryptContext
from passlib.handlers.bcrypt import bcrypt

# Reset bcrypt backend to avoid cached errors
bcrypt._force_backend = True

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

password = "admin123"
hashed = pwd_context.hash(password)

print(hashed)
