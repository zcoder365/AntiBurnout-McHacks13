from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("API_KEY"))

def build_prompt(user_data: dict, burnout_percentage: int) -> str:
  sleep_range = user_data["sleep_range"]
  user_mood = user_data["user_mood"]
  physical_activity = user_data["physical_activity"]
  water_intake = user_data["water_intake"]
  caffeine_amount = user_data["caffeine_amount"]
  meals_taken = user_data["meals_taken"]


  return f"""
You are a supportive assistant helping McGill students manage burnout in a safe, non-medical way to help them stay on track.
Never diagnose. Never mention mental illness. Never give medical instructions.

STUDENT DATA:
- Sleep: {sleep_range}
- Mood: {user_mood}
- Physical Activity: {physical_activity}
- Water Intake: {water_intake} cups
- Caffeine: {caffeine_amount} cups
- Meals so far today: {meals_taken}

STUDENT BURNOUT CHANCES: {burnout_percentage}%
Print out the burnout percenatge as well.

For the purpose of this student wellness tool:
- 7+ cups water is considered well hydrated.
- 1–2 cups caffeine is considered acceptable.
- 7+ hours sleep is considered well rested.
- Physical activity yes is good. 
- Motivated and Energetic moods are good.


Instructions:
  1. Start with one sentence validating how their week may have felt.
  2. Give EXACTLY three bullet points of gentle, practical suggestions personalized to their result above and adhering to the rules. 
  3. Include McGill campus-specific resources if appropriate:
    - Wellness Hub (Drop-ins + Appointments, dog therapy)
    - Workshops & Peer Support
    - McGill Recreation (gym, intramurals, yoga)
  4. End with an encouraging one-liner.

Ranges:
  - If <30% it would be in low chances range: maintenance + social balance.
  - If 30-60% it would be in moderate chances range: time balance + hydration + wellness workshops.
  - If >60% very high chances range: more advice, rest + support systems + Wellness Hub info.

  Tone: short, friendly, campus-oriented, max 100 words.
  """

def generate_feedback(data, burnout_percentage):
    prompt = build_prompt(data, burnout_percentage)
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


