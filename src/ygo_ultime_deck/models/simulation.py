from typing import List, Union
from pydantic import BaseModel, Field, ConfigDict

class Requirement(BaseModel):
    model_config = ConfigDict(extra='forbid')
    name: str = Field(min_length=1)
    count: Union[int, str] = Field(default=1)

class TargetCombo(BaseModel):
    model_config = ConfigDict(extra='forbid')
    name: str = Field(min_length=1)
    requirements: List[Requirement] = Field(min_length=1)

class SimulationRequest(BaseModel):
    model_config = ConfigDict(extra='forbid')
    combos: List[TargetCombo] = Field(min_length=1)

class SimulationResult(BaseModel):
    model_config = ConfigDict(extra='forbid')
    total_iterations: int = Field(ge=0)
    combo_success_rates: dict[str, int] = Field(default_factory=dict)
