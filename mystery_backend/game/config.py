DIFFICULTY_PROFILES = {
    'easy': {
        'num_suspects': 4,
        'num_clues': 6,
        'num_red_herrings': 1
    },
    'medium': {
        'num_suspects': 5,
        'num_clues': 8,
        'num_red_herrings': 2
    },
    'hard': {
        'num_suspects': 6,
        'num_clues': 10,
        'num_red_herrings': 3
    }
}

def get_difficulty_profile(difficulty):
    difficulty = difficulty.lower()
    if difficulty in DIFFICULTY_PROFILES:
        return DIFFICULTY_PROFILES[difficulty]
    else:
        return DIFFICULTY_PROFILES['medium']