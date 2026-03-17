import json

with open('data/companies.json') as f:
    companies = json.load(f)

print(f"Total companies in list: {len(companies)}")
for i, company in enumerate(companies, 1):
    print(f"  {i}. {company['name']}")