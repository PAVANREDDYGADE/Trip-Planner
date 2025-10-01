from ai_client import AIClient
from planner import build_prompt

# Define some sample normalized data for prompt
normalized = {
    "destination": "Bangalore",
    "start_date": "2025-12-10",
    "duration_days": 3,
    "budget_level": "tight",
    "interests": ["nature", "food", "culture", "hiking"],
    "transport": "bus/train",
    "stay_type": "hostel",
    "currency": "INR"
}

client = AIClient()
prompt = build_prompt(normalized)
result = client.generate_itinerary(prompt)
print(result)
