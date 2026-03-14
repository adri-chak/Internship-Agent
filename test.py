import json

with open('data/companies.json') as f:
    companies = json.load(f)

print(f"Loaded {len(companies)} companies!")
for company in companies:
    print(f"  - {company['name']}")