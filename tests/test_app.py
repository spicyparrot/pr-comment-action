#=============================================================================#
# Test Commenting
#=============================================================================#
import os
import sys
import pandas as pd
import random
import uuid
from github import Github

# Import shared modules
SCRIPT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,  os.path.abspath(f'{SCRIPT_DIRECTORY}/../src'))
print(f"Loading module '{SCRIPT_DIRECTORY}'")

from main import parse_event_details, get_comment_tag, gen_comment, put_comment

#=============================================================================#
# Test files
#=============================================================================#
EVENT_LOCAL_PATH_VALID=f"{SCRIPT_DIRECTORY}/data/pr_event.json"
EVENT_PATH_INVALID=f"{SCRIPT_DIRECTORY}/data/non_pr_event.json"
COMMENT_FILE = f"{SCRIPT_DIRECTORY}/data/comment.md"
COMMENT = 'Well. Hello there'
COMMENT_ID = random.randint(0, 10000)

#=============================================================================#
# Component Tests
#=============================================================================#
def test_parse_event_details():
    info = parse_event_details(EVENT_LOCAL_PATH_VALID)
    good_type = isinstance(info,dict)
    kays_expected = ['org', 'branch_ref', 'branch_name', 'branch_label', 'repo_name', 'repo_full_name']
    good_keys = kays_expected == list(info.keys())
    values_expected = ['spicyparrot', 'refs/heads/unit-testing-brnahc', 'unit-testing-brnahc', 'spicyparrot:unit-testing-brnahc', 'pr-comment-action', 'spicyparrot/pr-comment-action']
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


#=============================================================================#
# Full end to end (TODO - create test PR from test branch)
#=============================================================================#
github = Github(os.getenv('GITHUB_TOKEN'))

# Local vs Branch (with PR) vs Trunk testing
TEST_REF = os.getenv('GITHUB_BASE_REF','')
TEST_BRANCH = TEST_REF.split('/')[-1]
TEST_EVENT_PATH = EVENT_LOCAL_PATH_VALID if TEST_BRANCH in ['', 'trunk'] else os.environ['GITHUB_EVENT_PATH']


def test_put_comment_new_text_only():
    event_path = TEST_EVENT_PATH
    comment_uid = str(uuid.uuid4())
    comment1 = 'Well; hello there'
    comment2 = 'Well. Hello there!'
    comment_file = ''
    # Create new comment
    result1 = put_comment(event_path, comment_uid, comment1, comment_file)
    # Update existing comment
    result2 = put_comment(event_path, comment_uid, comment2, comment_file)
    assert result1 is True       ,"Comment not added"
    assert result2 is True       ,"Comment not updated"