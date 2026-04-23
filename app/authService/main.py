from fastapi import FastAPI
from loginService.loginHandler import login as handle_login
from logoutService.logoutHandler import logout as handle_logout
from models import (
    LoginRequest, 
    RefreshTokenRequest,
    LogoutRequest,
)
from refreshAccessTokenService.refreshHandler import (
    refresh_access_token as handle_refresh_access_token,
)

app = FastAPI()


@app.get("/")
def root() -> dict[str, str]:
    return {"hello": "world"}


@app.post("/login")
async def login(payload: LoginRequest) -> dict:
    return await handle_login(payload)

@app.post("/refresh")
async def refresh_access_token(payload: RefreshTokenRequest) -> dict:
    return await handle_refresh_access_token(payload)

@app.post("/logout")
async def logout(payload: LogoutRequest) -> dict:
    print("logout")
    return await handle_logout(payload)
