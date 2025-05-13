import pandas as pd
import numpy as np
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib

# Load the data
data = pd.read_csv('/Users/madhavbobby/Desktop/PROTECHTOS_AI_Scanner/your_data.csv')

# Define features and target
X = data.drop('target_column', axis=1)
y = data['target_column']

# Show class distribution
print("Class distribution:", Counter(y))

# Split into train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train model only if multiple classes exist
if len(set(y_train)) > 1:
    model = LogisticRegression(class_weight='balanced', max_iter=500, random_state=42)
    model.fit(X_train, y_train)

    print("✅ Model trained successfully.")

    # Predict and evaluate
    y_pred = model.predict(X_test)
    print("\n📊 Classification Report:")
    print(classification_report(y_test, y_pred))

    # Save model
    joblib.dump(model, 'vapt_model.pkl')
    print("\n💾 Model saved as 'vapt_model.pkl'")
else:
    print("❌ Not enough classes to train the model.")