import requests
from urllib.parse import urlencode

# Keycloak 서버 설정
keycloak_url = "http://localhost:8080"
realm_name = "myrealm"
client_id = "myclient"
client_secret = "mysecret"
redirect_uri = "http://localhost:8000/callback"

# 사용자 인증을 위한 URL 생성
auth_url = f"{keycloak_url}/realms/{realm_name}/protocol/openid-connect/auth"
params = {
    "response_type": "code",
    "client_id": client_id,
    "redirect_uri": redirect_uri,
    "scope": "openid"
}
auth_request_url = f"{auth_url}?{urlencode(params)}"

print(f"Please go to the following URL and authorize the application: {auth_request_url}")

# 사용자가 인증 후 리디렉션된 URL에서 'code' 파라미터를 추출하여 입력
authorization_code = input("Enter the authorization code: ")

# 토큰 요청
token_url = f"{keycloak_url}/realms/{realm_name}/protocol/openid-connect/token"
data = {
    "grant_type": "authorization_code",
    "code": authorization_code,
    "redirect_uri": redirect_uri,
    "client_id": client_id,
    "client_secret": client_secret
}

response = requests.post(token_url, data=data)
tokens = response.json()

# JWT 토큰 출력
access_token = tokens.get('access_token')
print(f"Access Token: {access_token}")