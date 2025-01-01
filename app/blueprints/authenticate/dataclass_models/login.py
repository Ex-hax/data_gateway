from pydantic.dataclasses import dataclass
from pydantic import Field

@dataclass
class api_login_user:
    user_name: str = Field(...)
    password: str = Field(...)
