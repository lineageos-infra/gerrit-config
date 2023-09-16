from datadiff import diff

from lib import Gerrit, send_message, Config

gerrit = Gerrit()

projects = [x for x in gerrit.get_projects() if any([x.startswith("PROJECT-"), x.startswith("OEM-")])]

groups = gerrit.get_groups()
modified = []
for project in projects:
    group_data = groups.get(project, None)
    if not group_data:
        print(f"Missing group for {project} - creating")
        gerrit.create_group(project)
        continue
    group = str(group_data["id"])
    branches = [
        "refs/heads/staging/*",
        "refs/heads/backup/*",
        "refs/heads/lineage-18.1",
        "refs/heads/lineage-19.1",
        "refs/heads/lineage-20",
    ]
    new = {
        'refs/heads/*': { 'permissions': {
            'label-Code-Review': {
                'rules': { group: {
                    'action': 'ALLOW',
                    'force': False,
                    'max': 2,
                    'min': -2,
              }},
              'label': 'Code-Review'
            },
           'label-Verified': {
               'rules': { group: {
                   'action': 'ALLOW',
                   'force': False,
                   'max': 1,
                   'min': -1,
             }},
             'label': 'Verified'
           },
            'submit': {
                'rules': { group: {
                    'action': 'ALLOW',
                    'force': False
                }}
            },
            'forgeAuthor': {
                'rules': { group: {
                    'action': 'ALLOW',
                    'force': False
                }}
            },
            'push': {
                'rules': { group: {
                    'action': 'ALLOW',
                    'force': False
                }}
            },
            'forgeCommitter': {
                'rules': { group: {
                    'action': 'ALLOW',
                    'force': False
                }}
            },
            'abandon': {
                'rules': {group: {
                    'action': 'ALLOW',
                    'force': False
                }}
            },
            'editTopicName': {
                'rules': {group: {
                    'action': 'ALLOW',
                    'force': False
                }}
            },
        }},
    }
    
    if project == 'PROJECT-qcom-hardware':
        branches += [
            "^refs/heads/lineage-18.1-caf(-(msm|sdm|sm)[0-9]{3,4})?",
            "^refs/heads/lineage-19.1-caf(-(msm|sdm|sm)[0-9]{3,4})?",
            "^refs/heads/lineage-20.0-caf(-(msm|sdm|sm)[0-9]{3,4})?",
        ]
    for branch in branches:
        new[branch] = {
            'permissions': {
                'create': {
                    'rules': {group: {
                        'action': 'ALLOW',
                        'force': False
                    }}
                },
            }
        }
    updated = gerrit.replace_project_permissions(project, new)
    if updated:
         modified.append(project)

if modified:
    send_message(Config.DISCORD_WEBHOOK, f"Reset project permissions on {', '.join(modified)}")
