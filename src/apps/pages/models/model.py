import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
import pickle
from utils.preprocess import Preprocessor
import os

# Create dataset folder if it doesn't exist
if not os.path.exists("dataset"):
    os.makedirs("dataset")
    print("Dataset folder created. Please place spam.csv in the dataset folder.")
    exit()


# Load dataset
df = pd.read_csv("dataset/spam.csv", encoding="latin-1")[["v1", "v2"]]
df.columns = ["label", "message"]
df["label"] = df["label"].map({"ham": 0, "spam": 1})

# Preprocess data
preprocessor = Preprocessor()
X = preprocessor.fit_transform(df["message"])
y = df["label"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = MultinomialNB()
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Save model and vectorizer
with open("utils/model.pkl", "wb") as model_file, open("utils/vectorizer.pkl", "wb") as vec_file:
    pickle.dump(model, model_file)
    pickle.dump(preprocessor.vectorizer, vec_file)
