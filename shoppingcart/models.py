from django.db import models
from crum import get_current_user
from genesis.models import Listing
# Create your models here.

class Cart(models.Model):
    listing = models.ForeignKey(
        Listing, null=True, default=None, on_delete=models.RESTRICT)
    total_quantity = models.PositiveIntegerField(
        default=1, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'auth.User', null=True, default=None, on_delete=models.RESTRICT)
    class Meta:
        verbose_name_plural = "1. Shopping Cart"