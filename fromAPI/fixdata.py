import json
with open('xy.json') as f:
    data = json.load(f)
    new = {k[:2]: v for k, v in data.items()}
    with open('xyp.json', 'w') as f2:
        json.dump(new, f2, indent=4)
        