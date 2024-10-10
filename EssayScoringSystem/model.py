import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import mean_squared_error

def load_model():
    """Load or create the model and vectorizer."""
    # Load dataset and preprocess (could be optimized to load pre-trained model)
    data = pd.read_csv("essays.csv")
    data['essay_clean'] = data['essay'].apply(lambda x: preprocess_text(x))

    # Train-test split
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(data['essay_clean'], data['score'], test_size=0.2, random_state=42)

    # TF-IDF Vectorizer
    vectorizer = TfidfVectorizer(max_features=5000)
    X_train_tfidf = vectorizer.fit_transform(X_train)
    
    # Train Linear Regression Model
    model = LinearRegression()
    model.fit(X_train_tfidf, y_train)
    
    # Evaluate model (optional)
    X_test_tfidf = vectorizer.transform(X_test)
    y_pred = model.predict(X_test_tfidf)
    print(f"Model MSE: {mean_squared_error(y_test, y_pred)}")

    return model, vectorizer

def predict_score(essay_clean, model, vectorizer):
    """Predict the score of a single essay."""
    essay_tfidf = vectorizer.transform([essay_clean])
    predicted_score = model.predict(essay_tfidf)
    return np.round(predicted_score, 2)