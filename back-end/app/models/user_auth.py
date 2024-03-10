from pydantic import BaseModel


class LoginModel(BaseModel):
    username: str
    password: str
    rememberMe: bool = False


class SignupModel(BaseModel):
    username: str
    password: str
    passwordConfirmation: str
