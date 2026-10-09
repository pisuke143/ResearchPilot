import sys
import platform
from pathlib import Path

print("=== ResearchPilot Environment Check ===")
print("Python version:", sys.version)
print("Python executable:", sys.executable)
print("Operating system:", platform.platform())
print("Project directory:", Path.cwd())
