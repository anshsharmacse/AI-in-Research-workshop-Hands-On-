# Section 03: Train an MLP with scaling and evaluate on a held-out test set

X = df[FEATURES].copy()
y = df[LABEL].astype(int).values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=SEED, stratify=y
)

mlp_model = Pipeline([
    ("scaler", StandardScaler()),
    ("mlp", MLPClassifier(
        hidden_layer_sizes=(32, 16),
        activation="relu",
        alpha=2e-4,
        learning_rate_init=1e-3,
        max_iter=1200,
        early_stopping=True,
        validation_fraction=0.15,
        n_iter_no_change=25,
        random_state=SEED
    ))
])

mlp_model.fit(X_train, y_train)

proba = mlp_model.predict_proba(X_test)[:, 1]
pred = (proba >= 0.5).astype(int)

print("ROC-AUC:", round(roc_auc_score(y_test, proba), 4))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, pred))
print("\nClassification Report:\n", classification_report(y_test, pred))

joblib.dump(mlp_model, MODEL_PATH)
print("Saved model:", MODEL_PATH.resolve())
