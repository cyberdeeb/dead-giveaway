import os, json
from typing import Dict, Any
from openai import OpenAI
from ..config import get_difficulty_profile

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_mystery_plot(*, difficulty: str) -> Dict[str, Any]:
    profile = get_difficulty_profile(difficulty)

    num_suspects = profile['num_suspects']
    num_clues = profile['num_clues']
    num_red_herrings = profile['num_red_herrings']

    system = 'You produce murder mysteries as strict JSON.'
    user = f"""
    Difficulty: {difficulty}.
    Use EXACTLY {num_suspects} suspects with ids S1..S{num_suspects}.
    Create EXACTLY {num_clues} clues with ids C1..C{num_clues}, and EXACTLY {num_red_herrings} red herrings R1..R{num_red_herrings}.
    Rules:
    - culprit_id MUST be one of the suspects' ids.
    - Each clue's 'implicates' must list 1–2 suspect ids from the suspects list.
    - At least 2 clues must implicate the culprit.
    - Each non-culprit must be implicated by at least 1 clue.
    - Keep all text concise: bios ≤200 chars, clues ≤200 chars. PG-13, no real people, no gore.
    Return JSON with keys: title, setting, suspects, culprit_id, clues, red_herrings, why_unique.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # This model supports JSON mode
        messages=[{"role":"system","content":system},{"role":"user","content":user}],
        response_format={"type":"json_object"}  # ask for a JSON object
        )
    
    content = response.choices[0].message.content

    return json.loads(content)