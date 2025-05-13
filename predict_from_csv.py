import pandas as pd
import joblib

# Load the trained model
model = joblib.load('vapt_model.pkl')

# Load the new data from CSV
new_data = pd.read_csv('new_data_to_predict.csv')  # <- Make sure this file exists

# Make predictions
predictions = model.predict(new_data)

# Display results
for i, pred in enumerate(predictions):
    status = "🟢 Not Vulnerable" if pred == 1 else "🔴 Vulnerable"
    print(f"Sample {i + 1} prediction: {status}")