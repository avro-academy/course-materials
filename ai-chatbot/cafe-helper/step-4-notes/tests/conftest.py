import os
import sys

# Let the tests import app.py and knowledge.py from the folder above
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
