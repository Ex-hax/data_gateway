from pydantic.dataclasses import dataclass

@dataclass
class api_login_user:
    user_name: str
    password: str

# @dataclass
# class api_login_header:
#     Authorization: str
#     "Content-type": str