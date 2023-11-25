import os
import sys
import json
import pandas as pd
from github import Github

### Get Event Info - https://pygithub.readthedocs.io/en/latest/github_objects/PullRequest.html
event_file = open(os.getenv('GITHUB_EVENT_PATH'))
event = json.load(event_file)
org = event['organization']['login']

# Exit early if not a branch associated/PR
if 'ref' not in list(event.keys()):
    print("No branch found for event")
    sys.exit()

branch_ref = event['ref']
branch_name = branch_ref.split('refs/heads/')[-1]
branch_label = org + ':' + branch_name
repo_name = os.environ["GITHUB_REPOSITORY"]

### Setup GitHub Class
token = os.getenv('GITHUB_TOKEN')
if token is None:
    token = os.getenv('ACTIONS_RUNTIME_TOKEN')
    
gh = Github(token)
repo = gh.get_repo(repo_name)
prs = repo.get_pulls(state='open', sort='created', head=branch_label)

### Only able comment if valid pull request is available
if prs.totalCount == 0:
    print("No PR found for branch - " + str(branch_label))
    sys.exit()

### Go through all existing issue comments
pr = prs[0]
comment_id = os.environ["INPUT_COMMENT_ID"]
comment_tag = f"[comment]: <> ({comment_id})"
comment_tag = comment_tag + "\n\n"   #This ensures the comment is hidden
comments = pr.get_issue_comments()
comment_strings = [c.body for c in pr.get_issue_comments()]
indexes = range(0, len(comment_strings))

comment_id = 0
for i in indexes:
    text = comments[i].body
    if text.startswith(comment_tag):
        comment_id = comments[i].id
        print("Duplicate comment found - " + str(comment_id))

# Get inputs from envars (GitHub converts all inputs into INPUT_<UPPER CASE OF INPUT>)
comment = os.environ["INPUT_COMMENT"]
new_comment = comment_tag + comment

comment_file = os.environ["INPUT_COMMENT_PATH"]
if len(comment_file) > 0:
    print("Comment file specified - " + str(comment_file))
    with open(comment_file, 'r') as file:
        data = file.read()
        new_comment = new_comment  + "\n\n" + data

if comment_id==0:
    print("No existing comment found. Adding new comment")
    pr.create_issue_comment(new_comment)
else:
    print("Editing existing comment - " + str(comment_id))
    issue = repo.get_issue(pr.number)
    existing_comment = issue.get_comment(comment_id)
    existing_comment.edit(new_comment)