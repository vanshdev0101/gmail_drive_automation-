from google.oauth2.credentials import Credentials

creds = Credentials.from_authorized_user_file("token.json")

print("SCOPES IN TOKEN:")
for s in creds.scopes:
    print("-", s)
