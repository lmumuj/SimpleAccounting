import subprocess
import os

os.chdir(r"c:\Users\Admins\Documents\记账")

# Git add
result = subprocess.run(["git", "add", "."], capture_output=True, text=True)
print("git add:", result.stdout, result.stderr)

# Git commit
result = subprocess.run(["git", "commit", "-m", "Initial commit"], capture_output=True, text=True)
print("git commit:", result.stdout, result.stderr)

# Check status
result = subprocess.run(["git", "log", "--oneline"], capture_output=True, text=True)
print("git log:", result.stdout, result.stderr)

result = subprocess.run(["git", "status"], capture_output=True, text=True)
print("git status:", result.stdout, result.stderr)
