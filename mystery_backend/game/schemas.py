# game/schemas.py
from typing import List, Literal, Annotated
from pydantic import BaseModel, Field, StringConstraints

Category = Literal["timeline", "forensic", "behavioral", "financial"]

# Reusable helpers
ShortID    = Annotated[str, StringConstraints(strip_whitespace=True, min_length=2, max_length=10)]
NameStr    = Annotated[str, StringConstraints(max_length=60)]
BioStr     = Annotated[str, StringConstraints(max_length=200)]
ClueText   = Annotated[str, StringConstraints(max_length=200)]
HerringStr = Annotated[str, StringConstraints(max_length=160)]
TitleStr   = Annotated[str, StringConstraints(max_length=80)]
SettingStr = Annotated[str, StringConstraints(max_length=120)]
WhyStr     = Annotated[str, StringConstraints(max_length=200)]

class SuspectOut(BaseModel):
    id: ShortID            
    name: NameStr
    bio: BioStr

class ClueOut(BaseModel):
    id: ShortID
    category: Category
    text: ClueText
    implicates: Annotated[
        List[ShortID],      
        Field(min_items=1, max_items=2)
    ]

class RedHerringOut(BaseModel):
    id: ShortID
    text: HerringStr

class MysteryOut(BaseModel):
    title: TitleStr
    setting: SettingStr
    suspects: List[SuspectOut]
    culprit_id: ShortID
    clues: List[ClueOut]
    red_herrings: List[RedHerringOut]
    why_unique: WhyStr
