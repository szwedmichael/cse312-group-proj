from pydantic import BaseModel


class LoginModel(BaseModel):
    username: str
    password: str


class SignupModel(BaseModel):
    username: str
    password: str
    passwordConfirmation: str
