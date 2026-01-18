from datetime import datetime

# convert sleep range string into average sleep hours
def converting_sleep_range(sleep_range: str) -> float:
  
  sleep_hours = 0.0

  if sleep_range == "0-4":
    sleep_hours = 3.0
  elif sleep_range == "5-7":
    sleep_hours = 6.0
  elif sleep_range == "8-10":
    sleep_hours = 9.0
  elif sleep_range == "10+":
    sleep_hours = 10.5
  else:
    sleep_hours = 6.0 #default value
  
  return sleep_hours

# maps the mood user chose into a mood level
def mapping_mood(user_mood: str) -> int:

  user_mood = user_mood.lower()
  mood_level = 0

  if user_mood == "motivated":
    mood_level = 5
  elif user_mood == "energetic":
    mood_level = 4
  elif user_mood == "meh":
    mood_level = 3
  elif user_mood == "tired":
    mood_level = 2
  elif user_mood == "anxious":
    mood_level = 1
  else:
    mood_level = 3 # neutral
  
  return mood_level

# helper to compute cutoff level for meals eaten so far 
def compute_meals_cutoff(meals_taken: int, current_hour: int) -> float:
   
    if current_hour < 12:
        target = 1   # by noon should have had 1 or more meals
    elif current_hour < 18:
        target = 2   # by evening should have had 2 or more meals
    else:
        target = 3   # by night should have had 3 or more meals

    # target met 
    if meals_taken >= target:
        return 0.0

    # target not met
    missing_meals = target - meals_taken  
    cutoff = missing_meals / target      
    
    if cutoff > 1.0:
        cutoff = 1.0

    return cutoff


# computes the chances of burnout 
def compute_burnout_rate(
    sleep_range: str,        
    user_mood: str,         
    physical_activity: str,  
    water_intake: float,     
    caffeine_amount: float,  
    meals_taken: int 
) -> int:

  sleep_hours = converting_sleep_range(sleep_range)
  mood_level = mapping_mood(user_mood)
  

  # cut-offs for each habit should be between 0(good) and 1(bad)

  # 8 or more hours of sleep needed
  sleep_cutoff = max(0.0, 8.0 - sleep_hours) / 8.0 

  # mood levels below 4 would add to burnout
  if mood_level < 4:
    mood_cutoff = (4.0 - mood_level) / 4.0
  else:
    mood_cutoff = 0.0

  physical_activity = physical_activity.lower()
  if (physical_activity == "yes"):
    physical_activity_cutoff = 0.0
  else:
    physical_activity_cutoff = 1.0

  # 7 or more cups of water needed
  water_intake_cutoff = max(0.0, 7.0 - water_intake) / 7.0 

  # 2 cups of caffeine is acceptable
  caffeine_cutoff = max(0.0, caffeine_amount - 2.0) / 4.0
  if caffeine_cutoff > 1.0:
    caffeine_cutoff = 1.0
  
  # meals cutoff depending on what time of the day the user uses the app
  current_hour = datetime.now().hour  
  meals_cutoff = compute_meals_cutoff(meals_taken, current_hour)

  burnout_score = (
    0.30 * sleep_cutoff +
    0.25 * caffeine_cutoff +
    0.20 * mood_cutoff +
    0.10 * water_intake_cutoff +
    0.10 * meals_cutoff +
    0.05 * physical_activity_cutoff
  )

  burnout_percentage = int(burnout_score * 100)

  if burnout_percentage < 0:
    burnout_percentage = 0
  elif burnout_percentage > 100:
    burnout_percentage = 100

  return burnout_percentage

def burnout_category(burnout_percentage: int) -> str:

  if burnout_percentage <= 30:
    return "Less chances of burnout"
  elif burnout_percentage <= 60:
    return "Moderate chances of burnout"
  else:
    return "High chances of burnout"














  



  
