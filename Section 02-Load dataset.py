# Section 02: Load dataset and visualize distributions + label balance

if not DATASET_PATH.exists():
    raise FileNotFoundError(
        f"CSV not found at {DATASET_PATH}. Put the file in the same folder, or update DATASET_PATH."
    )

df = pd.read_csv(DATASET_PATH)

print("Shape:", df.shape)
display(df.head(10))

print("Late rate (%):", round(df[LABEL].mean() * 100, 2))

assert set(WEEKDAYS).issuperset(set(df["day"].unique())), "Dataset contains non-weekday data."
assert all(col in df.columns for col in FEATURES + [LABEL]), "Missing required columns."

plt.figure(figsize=(5, 3))
df[LABEL].value_counts().sort_index().plot(kind="bar")
plt.title("Class Balance (0=On time, 1=Late)")
plt.xlabel("late")
plt.ylabel("count")
plt.show()

for col in FEATURES:
    plt.figure(figsize=(6, 3))
    plt.hist(df[col], bins=50)
    plt.title(f"Distribution: {col}")
    plt.xlabel(col)
    plt.ylabel("frequency")
    plt.show()

if "arrival_time_min" in df.columns:
    plt.figure(figsize=(6, 3))
    plt.hist(df["arrival_time_min"], bins=60)
    plt.axvline(LATE_THRESHOLD, linestyle="--")
    plt.title("Arrival time distribution (dashed = 08:05 threshold)")
    plt.xlabel("arrival_time_min")
    plt.ylabel("frequency")
    plt.show()
