from django.db import models
from member.models import Member


class Listing(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=80)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    category = models.CharField(max_length=255)
    condition = models.CharField(max_length=50, choices=[
        ('new', 'New'),
        ('used', 'Used'),
        ('refurbished', 'Refurbished')
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
