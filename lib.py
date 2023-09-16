import json
import os
from urllib.parse import quote_plus

import requests
from requests import auth as rauth

class Config:
    GERRIT_USER = os.environ.get("GERRIT_USER", "")
    GERRIT_PASS = os.environ.get("GERRIT_PASS", "")

    GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

    DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK", "")


class Gerrit:
    def __init__(self):
        self.auth = rauth.HTTPBasicAuth(Config.GERRIT_USER, Config.GERRIT_PASS)
    
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

    def replace_project_permissions(self, project: str, permissions: dict) -> bool:
        '''Replaces project permissions with new permission set
           Note: this does nothing if the new permission set matches the old one
           returns: bool, true if changes made
        '''
        url = f"https://review.lineageos.org/a/projects/{project}/access"
        resp = requests.get(url, auth=self.auth)

        if resp.status_code != 200:
            raise Exception(f"Error fetching permissions from gerrit: code {resp.status_code}, response: {resp.text}")
        
        perms = self._decode_raw(resp.text).get("local", {})

        if perms != permissions:
            print("no match")
            return False
            remove = {
                "remove": {"refs/heads/*": {}}
            }
            if perms:
                resp = requests.post(f"/projects/{project}/access", auth=self.auth, json={'remove': perms})
                if resp.status_code != 200:
                    raise Exception(f"Error removing gerrit permissions: {resp.text}")
            resp = requests.post(f"/projects/{project}/access", auth=self.auth, json={"add": permissions})
            if resp.status_code != 00:
                raise Exception(f"Error setting gerrit permissions: {resp.text}")
            return True
        return False

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

    def set_group_owner(self, group: str, owner: str) -> None:
        url = f"https://review.lineageos.org/a/groups/{group}/owner"
        resp =  requests.put(url, {'owner': owner})
        if resp.status_code != 200:
            raise Exception(f"Error communicating with gerrit: {resp.text}")


    def set_group_visible(self, group: str, visible: bool) -> None:
        url = f"https://review.lineageos.org/a/groups/{group}/options"
        resp = requests.put(url, {"visible_to_all": visible})
        if resp.status_code != 200:
            raise Exception(f"Error communicating with gerrit: {resp.text}")
        
    def _decode_raw(self, input: str):
        return json.loads(input[5:])


def send_message(webhook: str, message: str) -> None:

    requests.post(webhook, json={
        "username": "Github Actions",
        "icon_url": "https://avatars1.githubusercontent.com/u/44036562?s=280&v=4",
        "text": message
    })
