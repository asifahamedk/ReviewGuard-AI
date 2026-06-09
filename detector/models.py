from django.db import models


class ReviewHistory(models.Model):

    review_text = models.TextField()

    prediction = models.CharField(max_length=50)

    trust_score = models.FloatField()

    risk_level = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.prediction