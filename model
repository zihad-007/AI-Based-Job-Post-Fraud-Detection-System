import re

def preprocess_text(text):

    text = text.lower()

    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)

    return text


def predict_fraud(text):

    fraud_keywords = [
        "registration fee",
        "security deposit",
        "earn money fast",
        "whatsapp",
        "no experience required",
        "guaranteed profit",
        "account activation fee",
        "processing fee",
        "work 2 hours",
        "earn $"
    ]

    for word in fraud_keywords:
        if word in text:
            return "⚠️ Fraud Job Post Detected"

    return "✅ Real Job Post"
