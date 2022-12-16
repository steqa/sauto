from django.db import models
from accounts.models import User
from announcement.models import Announcement


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'избранное'
        verbose_name_plural = 'избранные'
    
    def __str__(self):
        return str(self.announcement)