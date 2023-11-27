#=============================================================================#
# Test Commenting
#=============================================================================#
import os
import sys
import pandas as pd
import pytest
import random
import uuid
from github import Github

# Import shared modules
SCRIPT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,  os.path.abspath(f'{SCRIPT_DIRECTORY}/../src'))
print(f"Loading module '{SCRIPT_DIRECTORY}'")

import main

#=============================================================================#
# Test files
#=============================================================================#
EVENT_PATH_VALID=f"{SCRIPT_DIRECTORY}/data/pr_event.json"
EVENT_PATH_INVALID=f"{SCRIPT_DIRECTORY}/data/non_pr_event.json"

#TODO - create test PR from test branch

def test_me():
    assert 1==1