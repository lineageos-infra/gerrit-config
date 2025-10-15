import yaml

with open("structure.yml", "r") as f:
    wanted = yaml.load(f.read(), Loader=yaml.BaseLoader)

parents = {item: None for item in wanted}

for parent, children in wanted.items():
    for child in children:
        if child in parents:
            parents[child] = parent

for item, parent in parents.items():
    assert item == "All-Projects" or parent, f"{item} has no parent"
