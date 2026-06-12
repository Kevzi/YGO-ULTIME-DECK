from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional
from enum import Enum

class CardAttribute(str, Enum):
    DARK = "DARK"
    EARTH = "EARTH"
    FIRE = "FIRE"
    LIGHT = "LIGHT"
    WATER = "WATER"
    WIND = "WIND"
    DIVINE = "DIVINE"

class CardRace(str, Enum):
    AQUA = "Aqua"
    BEAST = "Beast"
    BEAST_WARRIOR = "Beast-Warrior"
    CREATOR_GOD = "Creator-God"
    CYBERSE = "Cyberse"
    DINOSAUR = "Dinosaur"
    DIVINE_BEAST = "Divine-Beast"
    DRAGON = "Dragon"
    FAIRY = "Fairy"
    FIEND = "Fiend"
    FISH = "Fish"
    INSECT = "Insect"
    ILLUSION = "Illusion"
    MACHINE = "Machine"
    PLANT = "Plant"
    PSYCHIC = "Psychic"
    PYRO = "Pyro"
    REPTILE = "Reptile"
    ROCK = "Rock"
    SEA_SERPENT = "Sea Serpent"
    SPELLCASTER = "Spellcaster"
    THUNDER = "Thunder"
    WARRIOR = "Warrior"
    WINGED_BEAST = "Winged Beast"
    WYRM = "Wyrm"
    ZOMBIE = "Zombie"
    # Spell/Trap races
    NORMAL = "Normal"
    FIELD = "Field"
    EQUIP = "Equip"
    CONTINUOUS = "Continuous"
    QUICK_PLAY = "Quick-Play"
    RITUAL = "Ritual"
    COUNTER = "Counter"

class CardModel(BaseModel):
    """Pydantic model representing a YGOJSON card."""
    
    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore"
    )
    
    id: str
    name: str
    card_type: str = Field(alias="type")
    desc: str
    
    # Optional attributes
    race: Optional[CardRace] = None
    atk: Optional[int] = Field(default=None, ge=-1)
    def_: Optional[int] = Field(default=None, alias="def", ge=-1)
    level: Optional[int] = Field(default=None, ge=0, le=13)
    attribute: Optional[CardAttribute] = None
    series: Optional[str] = None
    
    # Additional common optional attributes based on YGOJSON schema
    archetype: Optional[str] = None
    scale: Optional[int] = Field(default=None, ge=0, le=13)
    linkval: Optional[int] = Field(default=None, ge=1, le=8)
    linkmarkers: Optional[list[str]] = None

    @field_validator("atk", "def_", mode="before")
    @classmethod
    def handle_question_mark_stats(cls, v):
        if isinstance(v, str) and v.strip() == "?":
            return -1
        return v

class TaggedCardModel(CardModel):
    """A CardModel that has been enriched with semantic tags."""
    tags: list[str] = Field(default_factory=list)
