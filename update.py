import yaml
import requests

from github import Github

from lib import Gerrit, Config


gerrit = Gerrit()
github = Github(Config.GITHUB_TOKEN)


with open("structure.yml", "r") as f:
    wanted = yaml.load(f.read(), Loader=yaml.BaseLoader)

with open("gha_enabled_repos.yml", "r") as f:
    gha_enabled_repos = yaml.load(f.read(), Loader=yaml.BaseLoader)

live = gerrit.get_projects()


print("Creating gerrit repos...")
missing = set()

for parent, children in wanted.items():
    if parent not in live.keys():
        missing.add(parent)
    for child in children:
        if child not in live.keys():
            missing.add(child)

if missing:
    print(f"Missing projects: {missing}")
    for project in missing:
        print(f"Creating {project} on gerrit...")
        gerrit.create_project(project)


live = gerrit.get_projects()

print("Creating github repos...")


github_org = github.get_organization("LineageOS")
github_projects = {x.id: x.full_name for x in github_org.get_repos()}
gerrit_projects = set()

for parent, children in wanted.items():
    gerrit_projects.add(parent)
    [gerrit_projects.add(x) for x in children]

missing = gerrit_projects - set(github_projects.values())

for repo in missing:
    if not repo.startswith("LineageOS/"):
        continue
    print(f"Creating {repo} on github...")
    github_org.create_repo(repo.replace("LineageOS/",""), has_wiki=False, has_downloads=False, has_projects=False, has_issues=False, private=False)
    github_org.get_repo(repo.replace("LineageOS/","")).edit(has_pull_requests=False)

print("Updating gerrit permissions...")

for parent, children in wanted.items():
    for child in children:
        if live.get(child, {}).get("parent") != parent:
            print(f"Setting parent of {child} to {parent}")
            gerrit.update_parent(child, parent)

gerrit_groups = gerrit.get_groups()
for group in [x for x in wanted.keys() if x.startswith("PROJECT-") or x.startswith("OEM-")]:
    if group not in gerrit_groups:
        print(f"adding {group}")
        gerrit.create_group(group)

print("Updating GHA allowed repos...")

gha_enabled_repos_ids = [k for k, v in github_projects.items() if v in gha_enabled_repos]
github._requester.requestJsonAndCheck("PUT", f"{github_org.url}/actions/permissions/repositories",
                                      input={"selected_repository_ids": gha_enabled_repos_ids})

print("Done!")
