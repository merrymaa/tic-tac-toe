from pydantic import BaseModel, Field

class SignUpRequest(BaseModel):
    """"Pydantic-модель для запроса"""

    login: str = Field(..., min_length=3, max_length=40)
    password: str = Field(..., min_length=6)
