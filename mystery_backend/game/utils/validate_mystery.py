from typing import Dict, Any
from mystery_backend.game.schemas import MysteryOut

def validate_mystery(mystery_data: Dict[str, Any]) -> MysteryOut:

    data = MysteryOut.model_validate(mystery_data)

    ids = {s.id for s in data.suspects}
    assert data.culprit_id in ids, "Culprit ID must be one of the suspects' IDs"

    counts = {s.id: 0 for s in data.suspects}
    for clue in data.clues:
        for sid in clue.implicates:
            assert sid in ids, f"Clue {clue.id} implicates unknown suspect {sid}"
            counts[sid] += 1

    assert counts[data.culprit_id] >= 2, "At least 2 clues must implicate the culprit"
    for sid in ids:
        if sid != data.culprit_id:
            assert counts[sid] >= 1, f"Non-culprit suspect {sid} must be implicated by at least 1 clue"

    culprit_total = counts[data.culprit_id]
    assert all(culprit_total > counts[sid] for sid in ids if sid != data.culprit_id), \
        "culprit not uniquely strongest"

    return data