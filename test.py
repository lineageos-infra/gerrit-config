import yaml

with open("structure.yml", "r") as f:
    wanted = yaml.load(f.read(), Loader=yaml.BaseLoader)

parents = {}

for parent, children in wanted.items():
    for child in children:
        assert child not in parents, f"{child} has multiple parents"
        parents[child] = parent

for item in wanted:
    assert item == "All-Projects" or item in parents, f"{item} has no parent"
