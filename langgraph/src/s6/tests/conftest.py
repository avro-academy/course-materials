import os
import sys
import tempfile

# Let the tests import the app's files from the folder above, and keep their databases out of it
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_tmp = tempfile.mkdtemp()
os.environ["BOOKINGS_DB"] = os.path.join(_tmp, "bookings.db")
os.environ["MEMORY_DB"] = os.path.join(_tmp, "memory.db")
