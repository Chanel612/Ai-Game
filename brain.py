# brain.py
import numpy as np

class Brain:
    """
    For now: dumb brain that picks random actions.
    Later: replace with real neural network / RL.
    """
    def __init__(self):
        # Logical actions, not keys
        self.actions = ["NONE", "JUMP", "MOVE_LEFT", "MOVE_RIGHT"]
        print("Brain ready with actions:", self.actions)

    def decide(self, state: np.ndarray) -> str:
        """
        state: np.ndarray of shape (stack_size, H, W)
        returns: one of the logical actions as a string.
        """
        # You could inspect state here; for now, random:
        return np.random.choice(self.actions)
