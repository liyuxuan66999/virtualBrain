from fastapi import FastAPI
from loginHandler import login as handle_login
from models import LoginRequest, RefreshTokenRequest
from refreshHandler import refresh_access_token as handle_refresh_access_token

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
