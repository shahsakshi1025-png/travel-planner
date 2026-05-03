from groq import Groq
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv(dotenv_path=Path(__file__).with_name('.env'))

def call_llm(prompt):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return (
            "Error: GROQ_API_KEY is not set. "
            "Please set GROQ_API_KEY in your environment or in the .env file."
        )

    try:
        client = Groq(api_key=api_key)
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model="llama-3.1-8b-instant"
        )

        return chat_completion.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"

# ---------------- BASE AGENT ---------------- #
# ---------------- BASE AGENT ---------------- #

class BaseAgent:
    def __init__(self, name, role):
        self.name = name
        self.role = role

    def think(self, task):
        prompt = f"""
        You are {self.name}, a {self.role}.

        Your job:
        {task}

        Follow instructions STRICTLY.
        Keep results realistic and within limits.
        """
        return call_llm(prompt)


# ---------------- AGENTS ---------------- #

class FlightAgent(BaseAgent):
    def __init__(self):
        super().__init__("Flight Agent", "expert in cheap flights")

    def run(self, city, budget):
        task = f"""
        Suggest ONLY 2 flight options to {city}.

        Rules:
        - TOTAL flight cost MUST be under {budget} INR
        - Include airline, price, duration
        - Keep prices realistic (Indian flights)
        - Do NOT exceed budget

        Format:
        - Airline | Price | Duration
        """
        return self.think(task)


class HotelAgent(BaseAgent):
    def __init__(self):
        super().__init__("Hotel Agent", "budget hotel expert")

    def run(self, city, budget, days):
        per_night = budget // days

        task = f"""
        Suggest 2-3 hotels in {city}.

        Rules:
        - Budget per night ≈ {per_night} INR
        - Total stay cost must be under {budget} INR
        - Include hotel name, price per night, area
        - Keep realistic pricing

        Format:
        - Hotel | Price/night | Area
        """
        return self.think(task)


class ActivityAgent(BaseAgent):
    def __init__(self):
        super().__init__("Activity Agent", "itinerary planner")

    def run(self, city, days, budget):
        task = f"""
        Create a {days}-day itinerary for {city}.

        Rules:
        - Keep activities low-cost
        - Assume total activity budget ≈ {budget} INR
        - Include food + attractions
        - Be realistic for tourists

        Format:
        Day 1: ...
        Day 2: ...
        """
        return self.think(task)


class BudgetAgent(BaseAgent):
    def __init__(self):
        super().__init__("Budget Agent", "trip cost optimizer")

    def run(self, flights, hotels, activities, total_budget):
        task = f"""
        You MUST ensure the total trip cost stays within {total_budget} INR.

        Flights:
        {flights}

        Hotels:
        {hotels}

        Activities:
        {activities}

        Rules:
        - Calculate total cost
        - Adjust plan if over budget
        - Give breakdown:
          Flights cost
          Hotel cost
          Activity cost
        - Final total MUST be ≤ {total_budget}

        Format clearly.
        """
        return self.think(task)


# ---------------- COORDINATOR ---------------- #

class TravelCoordinator:
    def __init__(self):
        self.flight_agent = FlightAgent()
        self.hotel_agent = HotelAgent()
        self.activity_agent = ActivityAgent()
        self.budget_agent = BudgetAgent()

    def execute(self, city, budget, days):

        # 🔥 SMART BUDGET SPLIT
        flight_budget = int(budget * 0.4)
        hotel_budget = int(budget * 0.4)
        activity_budget = int(budget * 0.2)

        # Step 1: agents use restricted budgets
        flights = self.flight_agent.run(city, flight_budget)
        hotels = self.hotel_agent.run(city, hotel_budget, days)
        activities = self.activity_agent.run(city, days, activity_budget)

        # Step 2: final optimizer
        final_plan = self.budget_agent.run(
            flights, hotels, activities, budget
        )

        return {
            "flights": flights,
            "hotels": hotels,
            "activities": activities,
            "final": final_plan
        }