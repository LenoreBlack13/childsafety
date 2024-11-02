from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Review
from .forms import ReviewForm
from django.urls import reverse
from django.urls import reverse_lazy

class ReviewListView(ListView):
    model = Review
    template_name = 'review/reviews.html'
    context_object_name = 'reviews'
    ordering = ['-date_posted']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_form'] = ReviewForm()
        context['active_page'] = 'reviews'

        # Проверка, оставил ли текущий пользователь отзыв
        if self.request.user.is_authenticated:
            context['user_has_review'] = Review.objects.filter(user=self.request.user).exists()
        else:
            context['user_has_review'] = False  # У анонимных пользователей нет отзывов

        return context

    def post(self, request, *args, **kwargs):
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('review-reviews')
        return self.render_to_response(self.get_context_data(review_form=form))

class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'review/review_form.html'
    success_url = reverse_lazy('review-reviews')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        review = self.get_object()
        return self.request.user == review.user

class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    template_name = 'review/review_confirm_delete.html'
    context_object_name = 'review'
    success_url = reverse_lazy('review-reviews')

    def test_func(self):
        review = self.get_object()
        return self.request.user == review.user

