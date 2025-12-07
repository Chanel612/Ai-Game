# actions.py
import time
import pyautogui
from keybinding import KeyBindingLearner

class ActionExecutor:
    def __init__(self, dry_run=True):
        self.dry_run = dry_run
        self.learner = KeyBindingLearner(epsilon=0.2)

    def set_dry_run(self, value):
        self.dry_run = value

    def execute(self, logical_action: str):
        key = self.learner.choose_key(logical_action)

        if key is None:
            print(f"[EXECUTOR] Action={logical_action} has no key")
            return None

        if self.dry_run:
            print(f"[EXECUTOR] Would press '{key}' for '{logical_action}'")
            return key

        print(f"[EXECUTOR] Pressing '{key}' for '{logical_action}'")
        pyautogui.keyDown(key)
        time.sleep(0.03)
        pyautogui.keyUp(key)

        return key

    def report_success(self, logical_action: str, key: str, success: bool):
        self.learner.update(logical_action, key, success)
