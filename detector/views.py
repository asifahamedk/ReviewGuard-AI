from django.shortcuts import render
from .ml_utils import analyze_review
from .models import ReviewHistory
from django.db.models import Avg


def home(request):

    if request.method == "POST":

        review = request.POST.get("review")

        result = analyze_review(review)

        # Save review in database
        ReviewHistory.objects.create(
            review_text=review,
            prediction=result['prediction'],
            trust_score=result['trust_score'],
            risk_level=result['risk_level']
        )

        context = {
            'prediction': result['prediction'],
            'trust_score': result['trust_score'],
            'risk_level': result['risk_level'],
            'reasons': result['reasons']
        }

        return render(
            request,
            "detector/result.html",
            context
        )

    return render(
        request,
        "detector/home.html"
    )



def dashboard(request):

    total_reviews = ReviewHistory.objects.count()

    genuine_reviews = ReviewHistory.objects.filter(
        prediction='Genuine'
    ).count()

    suspicious_reviews = ReviewHistory.objects.filter(
        prediction='Suspicious'
    ).count()

    avg_trust = ReviewHistory.objects.aggregate(
        Avg('trust_score')
    )['trust_score__avg']

    context = {
        'total_reviews': total_reviews,
        'genuine_reviews': genuine_reviews,
        'suspicious_reviews': suspicious_reviews,
        'avg_trust': round(avg_trust, 2) if avg_trust else 0
    }

    return render(
        request,
        'detector/dashboard.html',
        context
    )


def history(request):

    reviews = ReviewHistory.objects.order_by(
        '-created_at'
    )

    return render(
        request,
        'detector/history.html',
        {
            'reviews': reviews
        }
    )
    
    