# !pip install lightgbm

import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Train-test split and training (robust, only this section changed)
_df = globals().get("df")
if _df is None:
    raise NameError(
        "`df` is not defined. Define a pandas DataFrame named `df` with a 'yield' column before running this script."
    )

if "yield" not in _df.columns:
    raise KeyError("Target column 'yield' not found in DataFrame `df`")

X = _df.drop("yield", axis=1)
y = _df["yield"].values
if y.ndim > 1:
    y = y.ravel()

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, shuffle=True
)

lgbm_model = lgb.LGBMRegressor(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=-1,
    num_leaves=31,
    random_state=42,
    n_jobs=-1,
)

# Fit with evaluation and early stopping when supported; fallback otherwise
try:
    lgbm_model.fit(
        X_train,
        y_train,
        eval_set=[(X_test, y_test)],
        eval_metric="l2",
        early_stopping_rounds=50,
        verbose=False,
    )
except TypeError:
    lgbm_model.fit(X_train, y_train)

# Predictions
y_pred = lgbm_model.predict(X_test)

print("MSE:", mean_squared_error(y_test, y_pred))
print("R²:", r2_score(y_test, y_pred))
