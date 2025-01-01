from pydantic.dataclasses import dataclass
from pydantic import Field

@dataclass
class test_api:
    user_name: str = Field(...)