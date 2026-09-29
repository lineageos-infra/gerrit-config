from lib import Gerrit, send_message, Config

gerrit = Gerrit()

GROUP_IDS = {
    "Administrators": "fcd2c6ad3dbe38e9fb63fff3655480b7d92e802e",
    "Committers": "15d3cfcb12b259633d120a1be73d343e7b4a4cda",
    "Head Developers": "a03fd3a0506d32837ea4b70a15186b53ce96137f",
    "Legacy Branch Reviewers": "34a2eb872aadd8905512c46420feabb292e47f9e",
    "Translation Robots": "168d27c07332e48452375fc99f78d69e4ed3e66e",
}

PERMISSIONS_READ = {
    "read": {
        "rules": {
            "global:Registered-Users": {"action": "ALLOW", "force": False},
            "global:Anonymous-Users": {"action": "ALLOW", "force": False},
        },
    },
}
PERMISSIONS_ALIVE = PERMISSIONS_READ | {
    "create": {
        "rules": {
            GROUP_IDS["Committers"]: {"action": "ALLOW", "force": False},
            GROUP_IDS["Head Developers"]: {"action": "ALLOW", "force": False},
        },
    },
    "push": {
        "rules": {
            GROUP_IDS["Administrators"]: {"action": "ALLOW", "force": True},
            "global:Registered-Users": {"action": "BLOCK", "force": True},
        },
    },
    "read": {
        "rules": {
            "global:Registered-Users": {"action": "ALLOW", "force": False},
            "global:Anonymous-Users": {"action": "ALLOW", "force": False},
        },
    },
}
PERMISSIONS_ALIVE_LEGACY = PERMISSIONS_ALIVE | {
    "abandon": {
        "rules": {
            GROUP_IDS["Legacy Branch Reviewers"]: {"action": "ALLOW", "force": False},
        },
    },
    "label-Code-Review": {
        "label": "Code-Review",
        "rules": {
            GROUP_IDS["Legacy Branch Reviewers"]: {"action": "ALLOW", "force": False, "min": -2, "max": 2},
        },
    },
    "label-Verified": {
        "label": "Verified",
        "rules": {
            GROUP_IDS["Legacy Branch Reviewers"]: {"action": "ALLOW", "force": False, "min": -1, "max": 1},
        },
    },
    "push": {
        "rules": {
            GROUP_IDS["Legacy Branch Reviewers"]: {"action": "ALLOW", "force": False},
        },
    },
    "submit": {
        "rules": {
            GROUP_IDS["Legacy Branch Reviewers"]: {"action": "ALLOW", "force": False},
        },
    },
}
PERMISSIONS_DEAD = {
    "pushMerge": {
        "rules": {
            "global:Registered-Users": {"action": "BLOCK", "force": False},
        },
    },
    "addPatchSet": {
        "exclusive": True,
        "rules": {
            "global:Registered-Users": {"action": "BLOCK", "force": False},
        },
    },
    "push": {
        "rules": {
            "global:Registered-Users": {"action": "BLOCK", "force": False},
        },
    },
}

PERMISSIONS = {
    "refs/heads/*": {
        "permissions": {
            "label-Code-Review": {
                "label": "Code-Review",
                "rules": {
                    GROUP_IDS["Translation Robots"]: {"action": "ALLOW", "force": False, "min": -2, "max": 2},
                    "global:Change-Owner": {"action": "BLOCK", "force": False, "min": -2, "max": 2},
                },
            },
        },
    },

    "refs/for/refs/heads/cm-11.0": {"permissions": PERMISSIONS_DEAD},
    "refs/for/refs/heads/cm-13.0": {"permissions": PERMISSIONS_DEAD},
    "refs/for/refs/heads/cm-14.0": {"permissions": PERMISSIONS_DEAD},
    "refs/for/refs/heads/cm-14.0": {"permissions": PERMISSIONS_DEAD},
    "refs/for/refs/heads/lineage-15.0": {"permissions": PERMISSIONS_DEAD},
    "refs/for/refs/heads/lineage-17.0": {"permissions": PERMISSIONS_DEAD},
    "refs/for/refs/heads/lineage-18.0": {"permissions": PERMISSIONS_DEAD},
    "refs/for/refs/heads/lineage-19.0": {"permissions": PERMISSIONS_DEAD},
    "refs/for/refs/heads/lineage-22.0": {"permissions": PERMISSIONS_DEAD},
    "refs/for/refs/heads/lineage-22.1": {"permissions": PERMISSIONS_DEAD},
    "refs/for/refs/heads/lineage-23.0": {"permissions": PERMISSIONS_DEAD},
    "refs/for/refs/heads/lineage-23.1": {"permissions": PERMISSIONS_DEAD},

    "^refs/heads/cm-11.0": {"permissions": PERMISSIONS_READ},
    "^refs/heads/cm-13.0": {"permissions": PERMISSIONS_READ},
    "^refs/heads/cm-13.0-caf(-[0-9]{3,4})?": {"permissions": PERMISSIONS_READ},
    "refs/heads/lineage-15.0": {"permissions": PERMISSIONS_READ},
    "^refs/heads/lineage-15.0-caf(-[0-9]{3,4})?": {"permissions": PERMISSIONS_READ},
    "refs/heads/lineage-17.0": {"permissions": PERMISSIONS_READ},
    "^refs/heads/lineage-17.0-(pn5xx|sn100x)": {"permissions": PERMISSIONS_READ},
    "^refs/heads/lineage-17.0-caf(-(apq|msm|sdm|sm)?[0-9]{3,4})?": {"permissions": PERMISSIONS_READ},
    "refs/heads/lineage-18.0": {"permissions": PERMISSIONS_READ},
    "^refs/heads/lineage-18.0-(pn5xx|sn100x)": {"permissions": PERMISSIONS_READ},
    "^refs/heads/lineage-18.0-caf(-(apq|msm|sdm|sm)?[0-9]{3,4})?": {"permissions": PERMISSIONS_READ},
    "refs/heads/lineage-19.0": {"permissions": PERMISSIONS_READ},
    "refs/heads/lineage-22.0": {"permissions": PERMISSIONS_READ},
    "refs/heads/lineage-22.1": {"permissions": PERMISSIONS_READ},
    "refs/heads/lineage-23.1": {"permissions": PERMISSIONS_READ},

    "refs/heads/cm-14.1": {"permissions": PERMISSIONS_ALIVE_LEGACY},
    "^refs/heads/cm-14.1-caf(-[0-9]{3,4})?": {"permissions": PERMISSIONS_ALIVE_LEGACY},
    "refs/heads/lineage-15.1": {"permissions": PERMISSIONS_ALIVE_LEGACY},
    "^refs/heads/lineage-15.1-caf(-[0-9]{3,4})?": {"permissions": PERMISSIONS_ALIVE_LEGACY},
    "refs/heads/lineage-16.0": {"permissions": PERMISSIONS_ALIVE_LEGACY},
    "^refs/heads/lineage-16.0-caf(-[0-9]{3,4})?": {"permissions": PERMISSIONS_ALIVE_LEGACY},
    "refs/heads/lineage-17.1": {"permissions": PERMISSIONS_ALIVE_LEGACY},
    "^refs/heads/lineage-17.1-(pn5xx|sn100x)": {"permissions": PERMISSIONS_ALIVE_LEGACY},
    "^refs/heads/lineage-17.1-caf(-(apq|msm|sdm|sm)?[0-9]{3,4})?": {"permissions": PERMISSIONS_ALIVE_LEGACY},
    "refs/heads/lineage-18.1": {"permissions": PERMISSIONS_ALIVE_LEGACY},
    "refs/heads/lineage-19.1": {"permissions": PERMISSIONS_ALIVE_LEGACY},
    "refs/heads/lineage-20.0": {"permissions": PERMISSIONS_ALIVE_LEGACY},
    "refs/heads/lineage-21.0": {"permissions": PERMISSIONS_ALIVE_LEGACY},

    "refs/heads/lineage-22.2": {"permissions": PERMISSIONS_ALIVE},
    "refs/heads/lineage-23.2": {"permissions": PERMISSIONS_ALIVE},
    "refs/heads/lineage-24.0": {"permissions": PERMISSIONS_ALIVE},
}

if gerrit.replace_project_permissions("Lineage-Platform-Projects", PERMISSIONS):
    send_message(Config.DISCORD_WEBHOOK, "Reset project permissions on Lineage-Platform-Projects")
