"""Spelling error injection for experiments."""
import random
import logging

logger = logging.getLogger(__name__)

# Keyboard neighbor mapping (QWERTY layout)
KEYBOARD_NEIGHBORS = {
    'a': ['q', 's', 'z'], 'b': ['v', 'g', 'h', 'n'],
    'c': ['x', 'd', 'f', 'v'], 'd': ['s', 'e', 'f', 'c', 'x'],
    'e': ['w', 'r', 'd', 's'], 'f': ['d', 'r', 't', 'g', 'v', 'c'],
    'g': ['f', 't', 'y', 'h', 'b', 'v'], 'h': ['g', 'y', 'u', 'j', 'n', 'b'],
    'i': ['u', 'o', 'k', 'j'], 'j': ['h', 'u', 'i', 'k', 'n', 'm'],
    'k': ['j', 'i', 'o', 'l', 'm'], 'l': ['k', 'o', 'p'],
    'm': ['n', 'j', 'k'], 'n': ['b', 'h', 'j', 'm'],
    'o': ['i', 'p', 'l', 'k'], 'p': ['o', 'l'],
    'q': ['w', 'a'], 'r': ['e', 't', 'f', 'd'],
    's': ['a', 'w', 'd', 'x', 'z'], 't': ['r', 'y', 'g', 'f'],
    'u': ['y', 'i', 'j', 'h'], 'v': ['c', 'f', 'g', 'b'],
    'w': ['q', 'e', 's', 'a'], 'x': ['z', 's', 'd', 'c'],
    'y': ['t', 'u', 'h', 'g'], 'z': ['a', 's', 'x']
}


def inject_typo(word: str) -> str:
    """Inject a single typo into a word by replacing one character."""
    if len(word) < 4:
        return word
    
    pos = random.randint(1, len(word) - 2)
    char = word[pos].lower()
    
    if char in KEYBOARD_NEIGHBORS and KEYBOARD_NEIGHBORS[char]:
        replacement = random.choice(KEYBOARD_NEIGHBORS[char])
        return word[:pos] + replacement + word[pos+1:]
    
    return word


def inject_errors(text: str, error_rate: float, seed: int = 42) -> str:
    """Inject spelling errors into text at specified rate."""
    random.seed(seed)
    
    words = text.split()
    num_errors = int(len(words) * error_rate)
    
    logger.info(f"Injecting {num_errors} errors into {len(words)} words ({error_rate:.0%})")
    
    error_indices = random.sample(range(len(words)), min(num_errors, len(words)))
    
    for idx in error_indices:
        original = words[idx]
        words[idx] = inject_typo(words[idx])
    
    return ' '.join(words)