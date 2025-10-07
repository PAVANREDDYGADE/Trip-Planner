from config import Config

def validate_inputs(data):
    destination = (data.get("destination") or "").strip()
    start_date = (data.get("start_date") or "").strip()
    duration_days = int(data.get("duration_days") or 0)
    budget_level = (data.get("budget_level") or "tight").strip().lower()
    interests = [i.strip().lower() for i in (data.get("interests") or "").split(",") if i.strip()]
    transport = (data.get("transport") or "bus/train").strip().lower()
    stay_type = (data.get("stay_type") or "hostel").strip().lower()
    currency = Config.DEFAULT_CURRENCY

    if not destination:
        return False, "Destination is required.", None
    if duration_days < Config.MIN_DAYS or duration_days > Config.MAX_DAYS:
        return False, f"Duration must be between {Config.MIN_DAYS} and {Config.MAX_DAYS}.", None

    return True, "", {
        "destination": destination,
        "start_date": start_date,
        "duration_days": duration_days,
        "budget_level": budget_level,
        "interests": interests,
        "transport": transport,
        "stay_type": stay_type,
        "currency": currency
    }

def build_prompt(params):
    destination = params["destination"]
    duration = params["duration_days"]
    budget = params["budget_level"]
    interests = ", ".join(params["interests"]) if params["interests"] else "general sightseeing"
    transport = params["transport"]
    stay = params["stay_type"]
    currency = params["currency"]

    prompt = f"""
You are a travel itinerary designer.

Create a {duration}-day budget-friendly travel itinerary for {destination}.
Preferences:
- Budget: {budget}
- Interests: {interests}
- Transport: {transport}
- Stay: {stay}
- Currency: {currency}

Format for each day:
Day X:
9:00 AM - 10:00 AM: Breakfast at [cafe name] (Menu: [sample item], Cost: [cost in {currency}])
10:00 AM - 12:00 PM: [Activity] at [place] (Cost: [cost])
12:00 PM - 1:00 PM: Lunch at [place] (Menu: [item], Cost: [cost])
1:00 PM - 4:00 PM: [Activity] at [place] (Cost: [cost])
... (one per line, no extra blank lines!)

End each day with: Total estimated daily cost: [amount] {currency}

Do NOT use bullet points, lists, tables, or code blocks.
One line for each time slot/activity, serial schedule format—NO extra lines.
Respond ONLY with the schedule in this style.
"""
    return prompt
