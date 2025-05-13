import pandas as pd
from sklearn.datasets import make_classification

# Generate sample data
X, y = make_classification(
    n_samples=50,
    n_features=2,
    n_informative=2,
    n_redundant=0,
    n_classes=2,
    weights=[0.6, 0.4],
    random_state=42
)

# Create DataFrame
df = pd.DataFrame(X, columns=["feature_1", "feature_2"])
df["target_column"] = y

# Save CSV
df.to_csv("your_data.csv", index=False)
print("✅ Sample dataset generated as your_data.csv")