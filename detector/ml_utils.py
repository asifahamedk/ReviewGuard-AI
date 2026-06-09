import pickle
import re
import string

from textblob import TextBlob
from scipy.sparse import hstack

# Load saved model and vectorizer
import os

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

model_path = os.path.join(
    BASE_DIR,
    'models',
    'reviewguard_hybrid_model.pkl'
)

vectorizer_path = os.path.join(
    BASE_DIR,
    'models',
    'reviewguard_vectorizer.pkl'
)

model = pickle.load(
    open(model_path, 'rb')
)

vectorizer = pickle.load(
    open(vectorizer_path, 'rb')
)


def clean_text(text):

    text = str(text).lower()

    text = re.sub(r'http\S+', '', text)

    text = re.sub(r'\d+', '', text)

    text = text.translate(
        str.maketrans('', '', string.punctuation)
    )

    return text


def extract_numeric_features(review):

    cleaned = clean_text(review)

    review_length = len(cleaned)

    word_count = len(cleaned.split())

    exclamation_count = review.count('!')

    capitals = sum(
        1 for c in review
        if c.isupper()
    )

    capital_ratio = (
        capitals / len(review)
        if len(review) > 0
        else 0
    )

    sentiment_score = (
        TextBlob(cleaned)
        .sentiment
        .polarity
    )

    return [
        review_length,
        word_count,
        exclamation_count,
        capital_ratio,
        sentiment_score
    ]


def analyze_review(review):

    cleaned = clean_text(review)

    text_features = vectorizer.transform(
        [cleaned]
    )

    numeric_features = extract_numeric_features(
        review
    )

    combined_features = hstack(
        [text_features, [numeric_features]]
    )

    prediction = model.predict(
        combined_features
    )[0]

    probability = model.predict_proba(
        combined_features
    )[0]

    trust_score = round(
        (1 - probability[1]) * 100,
        2
    )

    if trust_score >= 80:
        risk = "Low Risk"

    elif trust_score >= 50:
        risk = "Medium Risk"

    else:
        risk = "High Risk"
    reasons = generate_reasons(review)
    return {
    'prediction':
        'Genuine'
        if prediction == 0
        else 'Suspicious',

    'trust_score':
        trust_score,

    'risk_level':
        risk,

    'reasons':
        reasons
}

def generate_reasons(review):

    reasons = []

    if review.count('!') > 3:
        reasons.append(
            "Contains excessive exclamation marks"
        )

    if len(review.split()) < 5:
        reasons.append(
            "Review is unusually short"
        )

    if review.isupper():
        reasons.append(
            "Contains excessive capital letters"
        )

    positive_words = [
        'best',
        'amazing',
        'perfect',
        'excellent',
        'awesome'
    ]

    review_lower = review.lower()

    count = sum(
        word in review_lower
        for word in positive_words
    )

    if count >= 3:
        reasons.append(
            "Contains excessive promotional language"
        )

    return reasons