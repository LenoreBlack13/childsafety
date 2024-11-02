from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    review = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Оставьте свой отзыв'}),
        label=""
    )
    rating = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1, 6)],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Рейтинг'
    )

    class Meta:
        model = Review
        fields = ['review', 'rating']