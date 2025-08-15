# Pydantic schemas for validating OpenAI API responses
from typing import List, Literal, Annotated
from pydantic import BaseModel, Field, StringConstraints

# Valid clue categories for mystery generation
Category = Literal["timeline", "forensic", "behavioral", "financial"]

# Reusable string validators with length constraints
ShortID    = Annotated[str, StringConstraints(strip_whitespace=True, min_length=2, max_length=10)]   # IDs like "S1", "C2"
NameStr    = Annotated[str, StringConstraints(max_length=60)]    # Character names
BioStr     = Annotated[str, StringConstraints(max_length=200)]   # Character descriptions
ClueText   = Annotated[str, StringConstraints(max_length=200)]   # Clue descriptions
HerringStr = Annotated[str, StringConstraints(max_length=160)]   # Red herring text
TitleStr   = Annotated[str, StringConstraints(max_length=80)]    # Case titles
SettingStr = Annotated[str, StringConstraints(max_length=120)]   # Case locations
WhyStr     = Annotated[str, StringConstraints(max_length=200)]   # Uniqueness explanation


class SuspectOut(BaseModel):
    """Individual suspect with ID, name, and background."""
    id: ShortID            
    name: NameStr
    bio: BioStr


class ClueOut(BaseModel):
    """Evidence that implicates 1-2 suspects."""
    id: ShortID
    category: Category
    text: ClueText
    implicates: Annotated[
        List[ShortID],      # Must implicate at least 1, max 2 suspects
        Field(min_items=1, max_items=2)
    ]


class RedHerringOut(BaseModel):
    """False clue designed to mislead players."""
    id: ShortID
    text: HerringStr


class MysteryOut(BaseModel):
    """Complete mystery case from OpenAI - validates JSON structure."""
    title: TitleStr
    setting: SettingStr
    suspects: List[SuspectOut]
    culprit_id: ShortID
    clues: List[ClueOut]
    red_herrings: List[RedHerringOut]
    why_unique: WhyStr               # What makes this case special
