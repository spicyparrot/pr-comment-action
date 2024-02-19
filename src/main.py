import os
import sys
import json
import pandas as pd
from github import Github

# Import shared modules
SCRIPT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,  os.path.abspath(f'{SCRIPT_DIRECTORY}/../src'))

#=============================================================================#
# Get Event Info
#=============================================================================#
def get_comment_tag(comment_uid):
    """
    Returns the hidden tag used to identify comment uniqueness
    """
    comment_tag = f"[comment]: <> ({comment_uid})"       # This ensures the comment is hidden
    comment_tag = comment_tag + "\n\n"
    return comment_tag


def gen_comment(comment_uid, comment, comment_file):
    """
    Creates/Edits comment on a PR 
    """
    comment_tag = get_comment_tag(comment_uid)
    new_comment = comment_tag + comment
    # Optionally get comment for a text file
    if len(comment_file) > 0:
        print("Comment file specified - " + str(comment_file))
        with open(comment_file, 'r') as file:
            data = file.read()
            new_comment = new_comment  + "\n\n" + data

    return new_comment


def get_pr_comment_id(pull_request, comment_uid):
    """
    Get the comment id for a comment on a given PR which contains our comment_uid value
    """
    comment_tag = get_comment_tag(comment_uid)
    comments = pull_request.get_issue_comments()
    comment_strings = [c.body for c in pull_request.get_issue_comments()]
    indexes = range(0, len(comment_strings))
    # Check for existing comments
    github_id = 0
    for i in indexes:
        text = comments[i].body
        if text.startswith(comment_tag):
            github_id = comments[i].id
            print("Duplicate comment found - " + str(comment_uid))

    return github_id


def get_branch_pr(event_details:dict):
    """
    Return the PR objeects associated with the branch
    """
    repo_name = event_details['repo_full_name']
    print(f"Getting associated PRs: {repo_name}")
    repo = github.get_repo(repo_name)
    prs = repo.get_pulls(state='open', sort='created', head=event_details['branch_label'])
    print(f"Associated PRs: {prs.totalCount}")
    ### Only able comment if valid pull request is available
    if prs.totalCount == 0:
        print("No PR found for branch - " + str(event_details['branch_label']))
        sys.exit()
    pr = prs[0]
    return pr


def parse_event_details(event_path):
    """
    Parse the github event file ($GITHUB_EVENT_PATH)
    """
    print(f"Parsing event file: {event_path}")
    event_file = open(event_path)
    event = json.load(event_file)
    info = {}
    info['org'] = event['organization']['login']
    # Exit early if not a branch associated/PR
    if 'ref' not in list(event.keys()):
        print("No branch found for event")
        return {}
    # Branch info
    info['branch_ref'] = event['ref']
    info['branch_name'] = info['branch_ref'].split('refs/heads/')[-1]
    info['branch_label'] = info['org'] + ':' + info['branch_name']
    info['repo_name'] = event['repository']['name']
    info['repo_full_name'] = event['repository']['full_name']
    return info


def put_comment(event_path:str, comment_uid:str, comment:str, comment_file:str = '')-> bool:
    """

    """
    event_details = parse_event_details(event_path)
    pr = get_branch_pr(event_details)
    gh_id = get_pr_comment_id(pr, comment_uid)
    new_comment = gen_comment(comment_uid, comment, comment_file)
    if gh_id==0:
        print("No existing comment found. Adding new comment")
        pr.create_issue_comment(new_comment)
    else:
        print("Editing existing comment - " + str(id))
        repo = github.get_repo(event_details['repo_full_name'])
        issue = repo.get_issue(pr.number)
        existing_comment = issue.get_comment(id)
        existing_comment.edit(new_comment)
    return True


#=============================================================================#
# Handlers
#=============================================================================#
def github_event_validation():
    """
    Ensure all required information is present, else exit gracefully
    """
    event = {}
    return event


def github_action_handler(event_path:str, comment:str, comment_uid:str = '', comment_file:str = ''):
    # TODO - validation

    # Create comment
    put_comment(event_path, comment_uid, comment, comment_file=comment_file)
    return True

#=============================================================================#
# Script entrypoint
#=============================================================================#
github = Github(os.getenv('GITHUB_TOKEN'))

if __name__ == "__main__":
    # Get inputs from envars (GitHub converts all inputs into INPUT_<UPPER CASE OF INPUT>)
    event_path = os.getenv('GITHUB_EVENT_PATH')
    comment = os.getenv("INPUT_COMMENT")
    comment_uid = os.getenv("INPUT_COMMENT_ID")
    comment_path = os.getenv("INPUT_COMMENT_PATH")
    github_action_handler(event_path, comment, comment_uid, comment_file=comment_path)
