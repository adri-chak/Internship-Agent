import json

with open("data/hashes.json") as f:
    hashes = json.load(f)

print(f"Agent is tracking {len(hashes)} companies:")
for company, fingerprint in hashes.items():
    print(f"  {company}: {fingerprint}")