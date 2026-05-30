import csv
import json
import time
from llm import ask

results = []

with open("claims.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:

        prompt = f"""
Analyze the insurance claim below.

Return ONLY valid JSON.

Claim:
{row['description']}

Format:
{{
    "claim_type": "motor/property/liability/other",
    "tone": "calm/frustrated/urgent",
    "legal_action": "yes/no"
}}
"""

        response = ask([
            {
                "role": "system",
                "content": "You are an insurance claim classifier."
            },
            {
                "role": "user",
                "content": prompt
            }
        ])

        content = response.choices[0].message.content

        # Remove markdown code fences if present
        content = content.replace("```json", "")
        content = content.replace("```", "")
        content = content.strip()

        classification = json.loads(content)

        results.append({
            "claim_id": row["claim_id"],
            "description": row["description"],
            **classification
        })

        # Avoid Gemini free-tier rate limit
        time.sleep(12)

with open("results.json", "w", encoding="utf-8") as outfile:
    json.dump(results, outfile, indent=4)

print("Results saved to results.json")

# Ambiguous Claim Example:
# Claim ID 10: "There was damage during the incident, but I am not sure
# whether it was caused by the delivery truck or by the storm."
#
# This claim is ambiguous because the damage could be classified as:
# - Property: if the storm caused the damage.
# - Liability: if the delivery truck caused the damage.
#
# The model classified the claim as "property" with a "calm" tone and
# "no" legal action. This suggests the model focused more on the damage
# to property than on determining responsibility for the incident.