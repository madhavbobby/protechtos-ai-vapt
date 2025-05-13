import pandas as pd
import numpy as np
from collections import Counter
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# Load the data (make sure the path is correct)
data = pd.read_csv('/Users/madhavbobby/Desktop/PROTECHTOS_AI_Scanner/your_data.csv')

# Define the features and target
X_train = data.drop('target_column', axis=1)  # Features: feature_1, feature_2
y_train = data['target_column']  # Target

# Check class distribution before removing sparse classes
print("Class distribution before removing sparse classes:", Counter(y_train))

# If there are multiple classes, proceed with the model
if len(Counter(y_train)) > 1:
    # Initialize Logistic Regression model with class weights to handle imbalance
    logreg_model = LogisticRegression(class_weight='balanced', max_iter=500, random_state=42)

    # Fit the model on the available data
    logreg_model.fit(X_train, y_train)

    # Print the classification report
    print("Model trained successfully on available data.")
else:
    print("Not enough classes for training. Please review your data.")