# detector/explainer.py

def generate_ai_explanation(review, result):
    prediction = result['prediction']
    trust_score = result['trust_score']
    risk_level = result['risk_level']
    reasons = result['reasons']

    explanation = []

    explanation.append(f"Prediction: The model classified this review as {prediction}.")

    explanation.append(f"Trust Score: {trust_score}/100 indicates {risk_level.lower()}.")

    if reasons:
        explanation.append("Key signals detected:")
        for r in reasons:
            explanation.append(f"- {r}")
    else:
        explanation.append("No strong spam indicators were detected.")

    # AI-style interpretation
    if prediction == "Suspicious":
        explanation.append(
            "Overall analysis suggests this review may be artificially generated or promotional in nature."
        )
    else:
        explanation.append(
            "Overall analysis suggests this review appears genuine and natural."
        )

    return "\n".join(explanation)