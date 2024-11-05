# contact/views
from django.shortcuts import render, redirect
from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact=form.save()

            # Отправить email с использованием данных формы
            subject = 'Новая запись на занятие'
            message = f'Имя: {contact.name}\n' \
                      f'Телефон: {contact.phone}\n' \
                      f'Email: {contact.email}\n' \
                      f'Проект: {contact.project}\n' \
                      f'Дата заявки: {contact.create_at}'
            recipient_list = [settings.EMAIL_HOST_USER]

            # Отправка письма
            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, fail_silently=False)
                print(f"Данные формы: {form.cleaned_data}")
                print("Письмо отправлено успешно!")
            except Exception as e:
                print(f"Ошибка при отправке почты: {e}")

            return redirect('contact_send_success')
    else:
        form = ContactForm()

    return render(request, 'contact/contact.html', {'form': form, 'active_page': 'contact'})