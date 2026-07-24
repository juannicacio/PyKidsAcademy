from app.auth.jwt import create_access_token, decode_access_token

token = create_access_token(
    {
        "sub": "parent1@example.com",
        "role": "parent",
    }
)

print("TOKEN:")
print(token)

print("\nPAYLOAD:")
print(decode_access_token(token))
