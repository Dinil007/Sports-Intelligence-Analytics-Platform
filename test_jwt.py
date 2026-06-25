from auth.security import create_access_token

token = create_access_token(
    {"sub": "admin", "role": "coach"}
)

print(token)