
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score, recall_score, confusion_matrix
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.metrics import precision_score, f1_score
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.model_selection import cross_val_predict

REPO_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = (
    REPO_ROOT
    / "pandas"
    / "retail_orders_analysis"
    / "data"
    / "day3_retail_orders.csv"
)


def main():
    """Prepare finalized retail orders for classification."""

    # STEP 1: Load the dataset.
    df = pd.read_csv(DATA_PATH)

    # STEP 2: Keep orders with a known final outcome.
    finalized_orders = df[
        df["order_status"].isin(["Completed", "Cancelled"])
    ].copy()

    print("Finalized orders:", len(finalized_orders))

    # STEP 3: Select our initial input features.
    feature_columns = [
        "region",
        "category",
        "quantity",
        "unit_price",
        "discount_pct",
    ]

    X = finalized_orders[feature_columns]

    # STEP 4: Create the binary target.
    # Cancelled = 1, Completed = 0.
    y = (
        finalized_orders["order_status"]
        .eq("Cancelled")
        .astype(int)
    )

    # STEP 5: Separate training and testing data.
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    # STEP 6: Inspect the split.
    print("\nTraining rows:", len(X_train))
    print("Testing rows:", len(X_test))

    print("\nTraining target distribution:")
    print(y_train.value_counts())

    print("\nTesting target distribution:")
    print(y_test.value_counts())

    print("\nTraining features preview:")
    print(X_train.head().to_string(index=False))

    print("\nMissing values in training features:")
    print(X_train.isna().sum())


    # STEP 7: Create a majority-class baseline.
    # This model always predicts the most common class.
    baseline_model = DummyClassifier(
        strategy="most_frequent"
    )

    # Learn which target class occurs most frequently.
    baseline_model.fit(X_train, y_train)

    # Predict outcomes for the unseen test records.
    y_pred = baseline_model.predict(X_test)

    # STEP 8: Evaluate the baseline.
    accuracy = accuracy_score(y_test, y_pred)

    # Positive class 1 represents Cancelled.
    cancellation_recall = recall_score(
        y_test,
        y_pred,
        pos_label=1,
        zero_division=0,
    )

    print("\n--- Baseline Model Results ---")
    print(f"Accuracy: {accuracy:.2%}")
    print(f"Cancellation recall: {cancellation_recall:.2%}")

    print("\nConfusion matrix:")
    print(confusion_matrix(y_test, y_pred, labels=[0, 1]))


    # STEP 9: Define numerical and categorical features.
    numerical_features = [
        "quantity",
        "unit_price",
        "discount_pct",
    ]

    categorical_features = [
        "region",
        "category",
    ]

    # STEP 10: Build the numerical preprocessing pipeline.
    numerical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    # STEP 11: Build the categorical preprocessing pipeline.
    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    # STEP 12: Combine the two preprocessing pipelines.
    preprocessor = ColumnTransformer(
        transformers=[
            ("numerical", numerical_pipeline, numerical_features),
            ("categorical", categorical_pipeline, categorical_features),
        ]
    )

    # STEP 13: Build the complete ML pipeline.
    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", LogisticRegression(max_iter=1000)),
        ]
    )

    # STEP 14: Fit preprocessing and model on training data only.
    model.fit(X_train, y_train)

    # STEP 15: Predict on unseen test data.
    model_predictions = model.predict(X_test)

    # STEP 16: Evaluate our Logistic Regression model.
    model_accuracy = accuracy_score(y_test, model_predictions)

    model_precision = precision_score(
        y_test,
        model_predictions,
        zero_division=0,
    )

    model_recall = recall_score(
        y_test,
        model_predictions,
        zero_division=0,
    )

    model_f1 = f1_score(
        y_test,
        model_predictions,
        zero_division=0,
    )

    print("\n--- Logistic Regression Results ---")
    print(f"Accuracy: {model_accuracy:.2%}")
    print(f"Cancellation precision: {model_precision:.2%}")
    print(f"Cancellation recall: {model_recall:.2%}")
    print(f"Cancellation F1-score: {model_f1:.2%}")

    print("\nConfusion matrix:")
    print(confusion_matrix(
        y_test,
        model_predictions,
        labels=[0, 1],
    ))

    # STEP 17: Configure stratified cross-validation.
    cv = StratifiedKFold(
        n_splits=3,
        shuffle=True,
        random_state=42,
    )

    # STEP 18: Define evaluation metrics.
    scoring = {
        "accuracy": "accuracy",
        "balanced_accuracy": "balanced_accuracy",
        "recall": "recall",
        "f1": "f1",
    }

    # STEP 19: Evaluate both models using training data only.
    models = {
        "DummyClassifier": baseline_model,
        "LogisticRegression": model,
    }

    for name, estimator in models.items():
        scores = cross_validate(
            estimator,
            X_train,
            y_train,
            cv=cv,
            scoring=scoring,
        )

        print(f"\n--- {name}: Cross-Validation ---")

        for metric in scoring:
            values = scores[f"test_{metric}"]

            print(
                f"{metric}: "
                f"{values.mean():.2%} mean"
            )

        print(
            "Recall by fold:",
            scores["test_recall"].round(3),
        )



if __name__ == "__main__":
    main()

