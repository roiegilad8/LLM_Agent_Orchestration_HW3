import google.generativeai as genai
import os

# --- קריאת המפתח ממשתנה הסביבה GEMINI_API_KEY ---
api_key = os.getenv("GEMINI_API_KEY") 

if not api_key:
    print("שגיאה: משתנה הסביבה GEMINI_API_KEY אינו מוגדר.")
    print("וודא שביצעת את שלב 2 מהמדריך הקודם ושמרת את השינויים ב-~/.bashrc.")
    exit()

# הגדרת ה-API באמצעות המפתח שנשלף
genai.configure(api_key=api_key)

# --- לוגיקת הצ'אט ---
# שימוש במודל gemini-1.5-flash כי הוא מהיר ומתאים לשכבה החינמית
model = genai.GenerativeModel('gemini-1.5-flash')

print("--- Gemini CLI מוכן (הקלד 'exit' ליציאה) ---")

# התחלת צ'אט שזוכר את ההקשר
chat = model.start_chat(history=[])

while True:
    user_input = input("\n> ")
    if user_input.lower() in ['exit', 'quit']:
        print("להתראות! זכור להריץ 'deactivate' כשתסיים.")
        break
    
    try:
        response = chat.send_message(user_input)
        print(f"Gemini: {response.text}")
    except Exception as e:
        print(f"אירעה שגיאה: {e}")

