# cards/models.py

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class CardHolder(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    age = models.PositiveIntegerField(default=0)
    national_id_number = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username

class MetroCard(models.Model):
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    expiry_date = models.DateField()
    # Correct the ForeignKey relationship here
    holder = models.ForeignKey(CardHolder, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.card_number

# Signal to automatically create CardHolder instance when a User is created
@receiver(post_save, sender=User)
def create_card_holder(sender, instance, created, **kwargs):
    if created:
        CardHolder.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_card_holder(sender, instance, **kwargs):
    # Check if the CardHolder exists before trying to save
    if hasattr(instance, 'cardholder'):
        instance.cardholder.save()
