from time import sleep
from django.core.mail import send_mail
from celery import shared_task, states
from kinocms import settings
from kinocms.celery import app


@app.task(bind=True)
def send_email_task(self, mail_list, message):
    """Sends an email when the feedback form has been submitted."""
    # Simulate expensive operation(s) that freeze Django
    for x in range(len(mail_list)):
        self.update_state(state='PROGRESS',
                          meta={'done': x, 'total': len(mail_list)})
        send_mail(
            subject='KinoCMS',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[mail_list[x]],
            message='KinoCMS',
            html_message=message,
            fail_silently=True,
        )

        print(f'-----mail {x} sent-----')
    print(f'-----Done-----')

