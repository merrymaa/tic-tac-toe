from pydantic import BaseModel


class JwtRequest(BaseModel):
    login: str
    password: str


class JwtResponse(BaseModel):
    type: str = "Bearer"
    accessToken: str
    refreshToken: str


class RefreshJwtRequest:
    refreshToken: str
