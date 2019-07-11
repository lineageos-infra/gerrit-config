from lib import Gerrit

projects = Gerrit.get_projects()

print("---")
for node in sorted(projects.keys()):
    children = sorted(projects[node])
    if children:
        print(f"{node}:")
        for child in projects[node]:
            print(f"  - {child}")

