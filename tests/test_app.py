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

from main import get_event_info, get_comment_tag, gen_comment

#=============================================================================#
# Test files
#=============================================================================#
EVENT_PATH_VALID=f"{SCRIPT_DIRECTORY}/data/pr_event.json"
EVENT_PATH_INVALID=f"{SCRIPT_DIRECTORY}/data/non_pr_event.json"
COMMENT_FILE = f"{SCRIPT_DIRECTORY}/data/comment.md"
COMMENT = 'Well. Hello there'
COMMENT_ID = random.randint(0, 10000)


# TODO - create test PR from test branch



#=============================================================================#
# Tests
#=============================================================================#
def test_get_event_info():
    info = get_event_info(EVENT_PATH_VALID)
    good_type = isinstance(info,dict)
    kays_expected = ['org', 'branch_ref', 'branch_name', 'branch_label', 'repo_name', 'repo_full_name']
    good_keys = kays_expected == list(info.keys())
    values_expected = ['spicyparrot', 'refs/heads/testing-setup', 'testing-setup', 'spicyparrot:testing-setup', 'pr-comment', 'spicyparrot/pr-comment']
    good_values = values_expected == list(info.values())
    assert all([good_type,good_keys,good_values]), "Invalid dictionary parsed from event"


def test_get_comment_tag():
    tag = get_comment_tag(COMMENT_ID)
    hidden = tag.startswith('[comment]:')
    assert hidden, "Invalid comment tag generated"


def test_parse_comment_text_only():
    comment = gen_comment(COMMENT_ID, COMMENT, '')
    hidden = comment.startswith('[comment]:')
    text_present = comment.endswith(COMMENT)
    assert all([hidden,text_present]), "Invalid comment generated"


def test_parse_comment_text_and_file():
    comment = gen_comment(COMMENT_ID, COMMENT, COMMENT_FILE)
    hidden = comment.startswith('[comment]:')
    text_present = COMMENT in comment
    file_parsed = comment.endswith('|')
    assert all([hidden,text_present,file_parsed]), "Invalid comment generated"