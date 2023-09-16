import json
import os
from urllib.parse import quote_plus

import requests

class Config:
    GERRIT_USER = os.environ.get("GERRIT_USER")
    GERRIT_PASS = os.environ.get("GERRIT_PASS")

    GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

class Gerrit:
    def __init__(self):
        self.auth = requests.auth.HTTPBasicAuth(Config.GERRIT_USER, Config.GERRIT_PASS)

    def get_projects(self):
        url = "https://review.lineageos.org/a/projects/?t"
        resp = requests.get(url, auth=self.auth)

        if resp.status_code != 200:
            raise Exception(f"Error communicating with gerrit: {resp.text}")

        projects = json.loads(resp.text[5:])
        return projects

    def update_parent(self, child, parent, auth=None):
        child = quote_plus(child)
        url = f"https://review.lineageos.org/a/projects/{child}/parent"
        print(f"Updating {child}'s parent to {parent}")
        resp = requests.put(url, json=({"parent": parent, "commit_message": "Auto update from gerrit_config"}), auth=self.auth)
        if resp.status_code != 200:
            raise Exception(f"Error communicating with gerrit: {resp.text}")

    def create_project(self, name):
        url = f"https://review.lineageos.org/a/projects/{name.replace('/', '%2f')}"
        resp = requests.put(url, auth=self.auth)
        if resp.status_code != 201:
            raise Exception(f"Error communicating with gerrit: {resp.text}")

    def get_groups(self):
        url = "https://review.lineageos.org/a/groups/"
        resp = requests.get(url, auth=self.auth)

        if resp.status_code != 200:
            raise Exception(f"Error communicating with gerrit: {resp.text}")
        groups = json.loads(resp.text[5:])
        return groups

    def create_group(self, name):
        url = f"https://review.lineageos.org/a/groups/{name}"
        data = {
                "visible_to_all": True,
                "owner_id": "a03fd3a0506d32837ea4b70a15186b53ce96137f"
        }
        resp = requests.put(url, auth=self.auth, json=data)
        if resp.status_code != 201:
            raise Exception(f"Error communicating with gerrit: {resp.text}")
