import yaml
import requests

from lib import get_projects, update_parent, Config

if Config.GERRIT_USER and Config.GERRIT_PASS:
    auth = requests.auth.HTTPBasicAuth(Config.GERRIT_USER, Config.GERRIT_PASS)
else:
    auth = None

with open("structure.yaml", "r") as f:
    desired_projects = yaml.load(f.read())

live_projects = get_projects(auth)

changes = {}

for parent, children in desired_projects.items():
    if parent in live_projects:
        if set(live_projects[parent]) == set(desired_projects[parent]):
            continue
        else:
            changes[parent] = list(set(desired_projects[parent]) - set(live_projects[parent]))
            if not changes[parent]:
                del changes[parent]
    else:
        changes[parent] = children

if changes:
    for parent, children in changes.items():
        for child in children:
            update_parent(child, parent, auth)

print("Done!")
