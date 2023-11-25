import os
import sys
import json
import pandas as pd
from github import Github


#=============================================================================#
# Get Event Info
#=============================================================================#
def get_event_info(event_path):
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
    info['repo_name'] = 
    return info


def get_branch_pr(repo_name,token):
    """
    Return the PR objeects associated with the branch
    """
    print(f"Getting associated PRs: {repo_name}")
    gh = Github(token)
    repo = gh.get_repo(repo_name)
    prs = repo.get_pulls(state='open', sort='created', head=branch_label)
    pr = prs[0]
    print(f"Associated PR: {len(prs)}")
    return pr

### Only able comment if valid pull request is available
if prs.totalCount == 0:
    print("No PR found for branch - " + str(branch_label))
    sys.exit()

### Go through all existing issue comments (TODO - get the latest PR only)
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


if __name__ == "__main__":
    event_path = os.getenv('GITHUB_EVENT_PATH')
    repo = os.getenv["GITHUB_REPOSITORY"]
    token = os.getenv('GITHUB_TOKEN')
    comment_id = os.getenv["INPUT_COMMENT_ID"]
    
    pr_comment(event_path)