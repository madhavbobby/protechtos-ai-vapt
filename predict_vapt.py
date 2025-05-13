import pandas as pd
import joblib

# Load the trained model
model = joblib.load('vapt_model.pkl')

# Load new data to predict (this should match the structure of training features)
# For now, let's hardcode some test data (2 rows with same number of features)
new_data = pd.DataFrame({
    'feature_1': [0.3, -1.2],
    'feature_2': [1.5, 0.7]
})

# Make predictions
predictions = model.predict(new_data)

# Output predictions
for i, pred in enumerate(predictions):
    print(f"Sample {i+1} prediction: {'🔴 Vulnerable' if pred == 1 else '🟢 Not Vulnerable'}")