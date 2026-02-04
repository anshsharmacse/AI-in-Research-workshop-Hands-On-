# Section 07: Forecast probabilities till Friday (or next week if today is Friday),
# plus what-if curves and an improvement trajectory.

def next_weekday(day):
    i = WEEKDAYS.index(day)
    return WEEKDAYS[(i + 1) % 5]

def remaining_weekdays_from(today):
    i = WEEKDAYS.index(today)
    return WEEKDAYS[i:]

def make_forecast_days(yesterday_day):
    today = next_weekday(yesterday_day)
    if today == "Fri":
        return today, ["Mon", "Tue", "Wed", "Thu", "Fri"], "Next week"
    return today, remaining_weekdays_from(today), "This week"

def predict_prob(feat_dict):
    x = pd.DataFrame([feat_dict], columns=FEATURES)
    return float(mlp_model.predict_proba(x)[0, 1]) * 100

def apply_daily_improvement(feat, frac):
    out = feat.copy()
    out["wake_time_min"] = int(round(out["wake_time_min"] - 20 * frac))
    out["screen_after_wake_min"] = float(max(0, out["screen_after_wake_min"] - 25 * frac))
    out["prep_min"] = float(max(6, out["prep_min"] - 10 * frac))
    out["sleep_start_min"] = int(round((out["sleep_start_min"] - 15 * frac) % (24 * 60)))
    return out

def small_variation(feat, rng_local, scale=1.0):
    out = feat.copy()
    out["wake_time_min"] = int(round(clamp(out["wake_time_min"] + rng_local.normal(0, 5 * scale), 4*60+30, 9*60+30)))
    out["sleep_start_min"] = int(round((out["sleep_start_min"] + rng_local.normal(0, 10 * scale)) % (24 * 60)))
    out["screen_after_wake_min"] = float(clamp(out["screen_after_wake_min"] + rng_local.normal(0, 4 * scale), 0, 240))
    out["prep_min"] = float(clamp(out["prep_min"] + rng_local.normal(0, 2 * scale), 6, 90))
    out["commute_min"] = float(clamp(out["commute_min"] + rng_local.normal(0, 2 * scale), 0, 120))
    return out

today_inferred, forecast_days, period_label = make_forecast_days(yesterday_day)
print("Inferred today:", today_inferred)
print("Forecast:", period_label, forecast_days)

# Baseline path (store day features for fair what-if comparisons)
rng_base = np.random.default_rng(SEED + 999)
baseline_feat_list = []
feat_base = yesterday_features.copy()

for d in forecast_days:
    feat_base = small_variation(feat_base, rng_base, scale=1.0)
    baseline_feat_list.append(feat_base.copy())

baseline_probs = [predict_prob(f) for f in baseline_feat_list]

baseline_df = pd.DataFrame({
    "period": period_label,
    "day": forecast_days,
    "wake": [min_to_hhmm(f["wake_time_min"]) for f in baseline_feat_list],
    "sleep_start": [min_to_hhmm(f["sleep_start_min"]) for f in baseline_feat_list],
    "screen_min": [round(f["screen_after_wake_min"], 1) for f in baseline_feat_list],
    "prep_min": [round(f["prep_min"], 1) for f in baseline_feat_list],
    "commute_min": [round(f["commute_min"], 1) for f in baseline_feat_list],
    "late_probability_pct": np.round(baseline_probs, 1),
    "prediction": ["Late" if p >= 50 else "On time" for p in baseline_probs]
})

display(baseline_df)

# Improvement trajectory (gradual improvements toward last forecast day)
rng_imp = np.random.default_rng(SEED + 2025)
feat_imp = yesterday_features.copy()
n_days = len(forecast_days)

improve_probs = []
for i, d in enumerate(forecast_days):
    frac = 0.0 if n_days == 1 else (i / (n_days - 1))
    feat_imp = small_variation(feat_imp, rng_imp, scale=0.8)
    feat_imp = apply_daily_improvement(feat_imp, frac)
    improve_probs.append(predict_prob(feat_imp))

improve_df = pd.DataFrame({
    "period": period_label,
    "day": forecast_days,
    "late_probability_pct": np.round(improve_probs, 1),
    "prediction": ["Late" if p >= 50 else "On time" for p in improve_probs]
})
display(improve_df)

# What-if curves (starting from baseline daily features)
whatif_screen = []
whatif_prep = []

for f in baseline_feat_list:
    f1 = f.copy()
    f1["screen_after_wake_min"] = max(0.0, f1["screen_after_wake_min"] - 15)
    whatif_screen.append(predict_prob(f1))

    f2 = f.copy()
    f2["prep_min"] = max(6.0, f2["prep_min"] - 10)
    whatif_prep.append(predict_prob(f2))

whatif_df = pd.DataFrame({
    "day": forecast_days,
    "baseline_pct": np.round(baseline_probs, 1),
    "screen_minus_15_pct": np.round(whatif_screen, 1),
    "prep_minus_10_pct": np.round(whatif_prep, 1),
})
display(whatif_df)

plt.figure(figsize=(10, 4))
plt.bar(whatif_df["day"], whatif_df["baseline_pct"])
plt.title("Late Probability Forecast - Baseline")
plt.xlabel("Day")
plt.ylabel("Late probability (%)")
plt.ylim(0, 100)
plt.show()

plt.figure(figsize=(10, 4))
plt.plot(whatif_df["day"], whatif_df["baseline_pct"], marker="o", label="Baseline")
plt.plot(whatif_df["day"], whatif_df["screen_minus_15_pct"], marker="o", label="Screen -15 min")
plt.plot(whatif_df["day"], whatif_df["prep_minus_10_pct"], marker="o", label="Prep -10 min")
plt.title("What-If Curves (controllable changes)")
plt.xlabel("Day")
plt.ylabel("Late probability (%)")
plt.ylim(0, 100)
plt.legend()
plt.show()

plt.figure(figsize=(10, 4))
plt.bar(improve_df["day"], improve_df["late_probability_pct"])
plt.title("Late Probability Forecast - Gradual Improvements")
plt.xlabel("Day")
plt.ylabel("Late probability (%)")
plt.ylim(0, 100)
plt.show()

top_feature = importance.index[0]
print("Most influential feature:", top_feature)
print("Try waking earlier, reducing screen time after waking, and streamlining prep.")
