from lib import Gerrit, send_message, Config

gerrit = Gerrit()

projects = gerrit.get_projects()
groups = gerrit.get_groups()
filtered_groups = [x for x in groups.keys() if any([x.startswith("OEM"), x.startswith("PROJECT")])]

parent_id = groups['Head Developers']['id']

modified = []
for group in filtered_groups:
    _id = groups[group]['id']
    if groups[group]['owner'] != 'Head Developers':
        print(f'{group} isn\'t owned by Head Developers, fixing')
        gerrit.set_group_owner(group, parent_id)
        modified.append(group)
    if not groups[group]["options"].get("visible_to_all", False):
        gerrit.set_group_visible(group, True)

if modified:
    send_message(Config.DISCORD_WEBHOOK, f"Reset group settings on {', '.join(modified)}")
