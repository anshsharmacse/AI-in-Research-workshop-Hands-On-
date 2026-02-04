# Section 04: Compute model-agnostic feature importance via permutation importance

pi = permutation_importance(
    mlp_model, X_test, y_test,
    n_repeats=12, random_state=SEED
)

importance = pd.Series(pi.importances_mean, index=FEATURES).sort_values(ascending=False)
display(importance)

plt.figure(figsize=(7, 3))
importance.plot(kind="bar")
plt.title("Permutation Feature Importance (MLP)")
plt.xlabel("feature")
plt.ylabel("importance")
plt.show()
