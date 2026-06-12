import re
import logging
from pathlib import Path
from ygo_ultime_deck.models.card import CardModel, TaggedCardModel

logger = logging.getLogger(__name__)

class RegexTagger:
    """Categorizes cards using pre-compiled regular expressions."""
    
    def __init__(self, rules: dict[str, str]):
        """
        Initialize the tagger with a dictionary of rules.
        
        Args:
            rules: A dictionary where keys are tag names and values are regex patterns.
        """
        self.compiled_rules: dict[str, re.Pattern] = {}
        for tag, pattern in rules.items():
            try:
                # Removed re.IGNORECASE to allow case-sensitive rules.
                # Added re.DOTALL to allow .* to match across newlines in PSCT.
                self.compiled_rules[tag] = re.compile(pattern, re.DOTALL)
            except (re.error, TypeError) as e:
                logger.error("Failed to compile regex for tag '%s': %s", tag, e)

    @classmethod
    def from_config(cls, filepath: str | Path | None = None) -> "RegexTagger":
        """
        Create a RegexTagger from a YAML configuration file.
        
        Args:
            filepath: Optional path to the YAML file. Defaults to config/tags_rules.yaml.
            
        Returns:
            An instance of RegexTagger configured with the loaded rules.
        """
        from ygo_ultime_deck.rules.config import load_tags_rules
        
        if filepath is None:
            current_dir = Path(__file__).resolve().parent
            while current_dir.parent != current_dir and not (current_dir / "config" / "tags_rules.yaml").exists():
                current_dir = current_dir.parent
            filepath = current_dir / "config" / "tags_rules.yaml"
            
        rules = load_tags_rules(filepath)
        return cls(rules)

            
    def tag_card(self, card: CardModel) -> TaggedCardModel:
        """
        Evaluate a card's description against the compiled regex rules and return a new TaggedCardModel.
        
        Args:
            card: The original CardModel.
            
        Returns:
            A new TaggedCardModel with the matched tags appended.
        """
        matched_tags = []
        
        # Structurally ignore non-effect normal monsters to avoid false positives on flavor text
        is_normal_monster = "Normal" in card.card_type and "Monster" in card.card_type and "Pendulum" not in card.card_type
        
        if not is_normal_monster:
            desc = card.desc
            if desc:
                for tag, compiled_pattern in self.compiled_rules.items():
                    if compiled_pattern.search(desc):
                        matched_tags.append(tag)
                
        card_data = card.model_dump(by_alias=True)
        card_data.pop("tags", None) # Prevent key collision
        
        # Use model_construct to bypass Pydantic validation for massive performance gain
        return TaggedCardModel.model_construct(**card_data, tags=matched_tags)
