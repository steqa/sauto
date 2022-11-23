import threading
from django.core.mail import EmailMessage
from .models import User


class SendEmailThread(threading.Thread):
    def __init__(self, email: EmailMessage):
        self.email = email
        threading.Thread.__init__(self)
    
    def run(self):
        self.email.send()


class DeleteUserAfterTimeElapsed(threading.Thread):
    def __init__(self, user: User, lifetime: int):
        self.user = user
        self.lifetime = lifetime
        threading.Thread.__init__(self)

    def run(self):
        event = threading.Event()
        event.wait(self.lifetime)
        user = User.objects.get(pk=self.user.pk)
        if user.is_email_verified is False:
            user.delete()
