import json
import os
from urllib.parse import quote_plus

import requests

class Config:
    GERRIT_USER = os.environ.get("GERRIT_USER")
    GERRIT_PASS = os.environ.get("GERRIT_PASS")

def get_projects(auth=None):
    url = "https://review.lineageos.org/a/projects/?t" if auth else "https://review.lineageos.org/projects/?t"
    resp = requests.get(url, auth=auth)
    if resp.status_code != 200:
        raise Exception(f"Error communicating with gerrit: {resp.text}")
    projects = json.loads(resp.text[5:])
    nodes = {}

    for name, project in projects.items():
        nodes[name] = []

    for name, project in projects.items():
        parent = project.get("parent")
        if parent:
            nodes[parent].append(name)
    for project in nodes.keys():
        nodes[project] = sorted(nodes[project])
    return nodes

def update_parent(child, parent, auth=None):
    child = quote_plus(child)
    url = f"https://review.lineageos.org/a/projects/{child}/parent" if auth else f"https://review.lineageos.org/projects/{child}/parent"
    print(f"Updating {child}'s parent to {parent}")
    resp = requests.put(url, json=({"parent": parent, "commit_message": "Auto update from gerrit_config"}))
    if resp.status_code != 200:
        raise Exception(f"Error communicatin gwith gerrit: {resp.text}")
