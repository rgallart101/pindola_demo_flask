#!/usr/bin/env python
import subprocess
import sys

result = subprocess.run([
    sys.executable, "-m", "babel.messages.frontend", "compile",
    "-d", "app/translations"
], cwd="/Users/ramonmariagallartescola/Documents/Projects/pindola_demo_flask")

sys.exit(result.returncode)
