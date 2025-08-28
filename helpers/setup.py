import sys
import os
import logging

# Add the root directory to sys.path
root = os.path.abspath("..")
sys.path.append(root)

# Optional: suppress FastF1 info logs globally
logging.getLogger('fastf1').setLevel(logging.INFO)

