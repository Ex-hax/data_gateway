from pydantic.dataclasses import dataclass
from pydantic import Field

# TODO to recheck validate_headers
@dataclass
class AuthHeaders:
    content_type: str = Field(..., alias="Content-Type", pattern="^application/json$")
    authorization: str = Field(..., alias="Authorization", description="Bearer token for authentication")