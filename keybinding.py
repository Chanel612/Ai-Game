# keybinding.py
import random
from collections import defaultdict

# FULL key list for exploration
ALL_KEYS = [
    'a','b','c','d','e','f','g','h','i','j','k','l','m',
    'n','o','p','q','r','s','t','u','v','w','x','y','z',
    '0','1','2','3','4','5','6','7','8','9',
    'left','right','up','down',
    'space','enter','return','tab','backspace','delete',
    'shift','ctrl','alt','command','option',
    'f1','f2','f3','f4','f5','f6','f7','f8','f9','f10','f11','f12',
    '`','-','=','[',']','\\',';',"'",',','.','/',
    'esc','escape','home','end','pgup','pgdn','insert'
]

class KeyBindingLearner:
    """
    Learns which physical key works best for each logical action.
    Now uses the FULL key list for exploration.
    """
    def __init__(self, epsilon=0.1):
        self.epsilon = epsilon
        self.stats = defaultdict(lambda: defaultdict(lambda: {"success": 0, "trials": 0}))

    def choose_key(self, logical_action: str):
        # Exploration: try a random key
        if random.random() < self.epsilon:
            return random.choice(ALL_KEYS)

        # Exploitation: use the best-known key
        best_key = None
        best_rate = -1

        for key in ALL_KEYS:
            data = self.stats[logical_action][key]
            trials = data["trials"]
            success = data["success"]

            # untested keys get neutral probability
            rate = 0.5 if trials == 0 else success / trials

            if rate > best_rate:
                best_rate = rate
                best_key = key

        return best_key

    def update(self, logical_action: str, key: str, success: bool):
        data = self.stats[logical_action][key]
        data["trials"] += 1
        if success:
            data["success"] += 1
# keybinding.py
import random
from collections import defaultdict

class KeyBindingLearner:
    """
    Learns which physical key works best for each logical action.
    Uses a simple epsilon-greedy strategy per action.
    """

    def __init__(self, action_candidates, epsilon=0.2):
        """
        action_candidates: dict like:
            {
                "JUMP": ["space", "w", "up", "j", "k", "z", "x"],
                "MOVE_LEFT": ["left", "a"],
                "MOVE_RIGHT": ["right", "d"],
            }
        epsilon: probability of exploring a random key instead of the best-known one.
        """
        self.action_candidates = action_candidates
        self.epsilon = epsilon

        # stats[action][key] = {"success": int, "trials": int}
        self.stats = defaultdict(lambda: defaultdict(lambda: {"success": 0, "trials": 0}))

    def choose_key(self, logical_action: str):
        """
        Pick which physical key to try for the given logical action.
        """
        candidates = self.action_candidates.get(logical_action)
        if not candidates:
            return None

        # Random exploration
        if random.random() < self.epsilon:
            return random.choice(candidates)

        # Exploit best success rate
        best_key = None
        best_rate = -1.0
        for key in candidates:
            data = self.stats[logical_action][key]
            if data["trials"] == 0:
                # untested keys start with neutral 0.5
                rate = 0.5
            else:
                rate = data["success"] / data["trials"]

            if rate > best_rate:
                best_rate = rate
                best_key = key

        return best_key

    def update(self, logical_action: str, key: str, success: bool):
        """
        Record whether this action-key attempt succeeded or failed.
        """
        data = self.stats[logical_action][key]
        data["trials"] += 1
        if success:
            data["success"] += 1
