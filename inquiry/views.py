from django.shortcuts import render
from .forms import InquiryForm
from django.core.mail import send_mail

def inquiry(request):
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            company_name = form.cleaned_data['company_name']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            content = form.cleaned_data['content']
            Inquiry.objects.create(company_name=company_name, first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, content=content)

            subject = '問い合わせを受け付けました'
            html_message = render_to_string('inquiry/mail_template/inquiry/message.html', {
                'company_name': company_name,
                'last_name': last_name,
                'first_name': first_name,
                'email': email,
                'phone_number': phone_number,
                'content': content,
            })
            plain_message = strip_tags(html_message)
            from_email = 'info@MeBias.com'
            to_email = [email]
            send_mail(subject, plain_message, from_email, to_email, html_message=html_message)

            subject = '問い合わせを受け付けました'
            html_message = render_to_string('inquiry/mail_template/inquiry/announce.html', {
                'company_name': company_name,
                'last_name': last_name,
                'first_name': first_name,
                'phone_number': phone_number,
                'email': email,
                'content': content,
            })
            plain_message = strip_tags(html_message)
            from_email = 'info@MeBias.com'
            to_email = ['MeBias.info@gmail.com']
            send_mail(subject, plain_message, from_email, to_email, html_message=html_message)

            return redirect('inquiry_complete')
    else:
        form = InquiryForm()
    return render(request, 'inquiry/inquiry.html', {'form': form})

def inquiry_complete(request):
    return render(request, 'inquiry/inquiry_complete.html')
