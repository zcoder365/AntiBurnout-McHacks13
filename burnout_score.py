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

  





  



  
