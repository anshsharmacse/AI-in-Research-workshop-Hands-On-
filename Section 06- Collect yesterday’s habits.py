# Section 06: Collect yesterday’s habits and infer today (Mon–Fri)

def ask_day():
    while True:
        s = input("Yesterday was which day? (Mon/Tue/Wed/Thu/Fri): ").strip().title()
        if s in WEEKDAYS:
            return s
        print("Enter one of: Mon Tue Wed Thu Fri")

def ask_time(prompt, default):
    while True:
        s = input(f"{prompt} [default={default}]: ").strip()
        if s == "":
            s = default
        try:
            return hhmm_to_min(s)
        except:
            print("Use HH:MM (24h), e.g., 06:50")

def ask_float(prompt, lo, hi, default):
    while True:
        s = input(f"{prompt} [default={default}]: ").strip()
        if s == "":
            return float(default)
        try:
            v = float(s)
        except:
            print("Enter a number.")
            continue
        if v < lo or v > hi:
            print(f"Must be between {lo} and {hi}.")
            continue
        return float(v)

yesterday_day = ask_day()
print("You need to attend 8 Am class- fill accordingly")

y_wake = ask_time("Yesterday wake-up time (HH:MM)", "06:50")
y_sleep = ask_time("Yesterday sleep start time (HH:MM)", "23:30")
y_screen = ask_float("Yesterday screen time after waking (minutes)", 0, 240, 20)
y_prep = ask_float("Yesterday prep minutes", 6, 90, 25)
y_commute = ask_float("Yesterday commute minutes", 0, 120, 25)

yesterday_features = {
    "wake_time_min": y_wake,
    "sleep_start_min": y_sleep,
    "screen_after_wake_min": y_screen,
    "prep_min": y_prep,
    "commute_min": y_commute
}

print({
    "day": yesterday_day,
    "wake": min_to_hhmm(y_wake),
    "sleep_start": min_to_hhmm(y_sleep),
    "screen_min": y_screen,
    "prep_min": y_prep,
    "commute_min": y_commute
})
