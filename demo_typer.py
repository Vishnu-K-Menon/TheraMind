import pyautogui
import time

# --- Demo Typing Script ---
print("🎬 Demo typing script started!")
print("⏳ You have 5 seconds to click the chat input box...")

for i in range(5, 0, -1):
    print(f"   {i}...")
    time.sleep(1)

print("⌨️  Typing now...")

message = "I'm having this really tight, squeezing pain in the center of my chest, and it's radiating down my left arm. I also feel a little short of breath and sweaty. What is this, and what medicine should I take?"

# Type each character individually at 0.01s interval
for char in message:
    pyautogui.write(char, interval=0)
    time.sleep(0.00005)

time.sleep(0.3)
pyautogui.press('enter')

print("✅ Typing complete! Message sent.")
