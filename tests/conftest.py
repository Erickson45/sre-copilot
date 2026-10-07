import os
import sys

# Permite importar os módulos de src/ como no container (python src/main.py)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
