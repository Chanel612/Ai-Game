# main.py
import time
from screen import capture_frame
from state_builder import StateBuilder
from brain import Brain

def main():
    print("GameBot starting (thinking only, no key presses yet)...")
    time.sleep(1)

    state_builder = StateBuilder(stack_size=4, height=84, width=84)
    brain = Brain()

    step = 0

    while True:
        frame = capture_frame()
        state = state_builder.update(frame)

        # Wait until we have enough frames stacked
        if state is None:
            continue

        action = brain.decide(state)
        step += 1

        if step % 10 == 0:
            print(f"[step {step}] Brain decided action: {action}")

        # small sleep so we don't peg CPU
        time.sleep(0.02)

if __name__ == "__main__":
    main()
