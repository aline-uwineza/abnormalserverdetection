import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# Load the dataset
data = pd.read_csv('server_activity_data.csv')
print("data")
# Features and Target
X = data[['CPU_Usage (%)', 'Memory_Usage (%)', 'Disk_IO', 'Network_Traffic', 'Error_Count']]
y = data['Target (Normal=0, Abnormal=1)']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest Classifier
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Evaluate
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f"Model Accuracy: {accuracy:.2f}")

# Save the model
joblib.dump(model, 'abnormal_detection_model.joblib')
print("Model saved successfully!")
