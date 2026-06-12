from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict

class MetaThreat(BaseModel):
    model_config = ConfigDict(extra='forbid')
    name: str = Field(min_length=1, json_schema_extra={"strip_whitespace": True})
    category: Optional[str] = Field(default="Generic")
    count: int = Field(default=1, ge=1, le=3)

class MetaTargetsRequest(BaseModel):
    model_config = ConfigDict(extra='forbid')
    threats: List[MetaThreat] = Field(min_length=1)
