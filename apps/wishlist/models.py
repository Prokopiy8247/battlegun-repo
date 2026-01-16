
import uuid
from django.db import models
from django.conf import settings
from apps.catalog.models import Product

class WishlistItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='wishlist')
    session_key = models.CharField(max_length=40, null=True, blank=True, db_index=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlisted_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = [
            ('user', 'product'),
            ('session_key', 'product'),
        ]
        indexes = [
            models.Index(fields=['session_key']),
            models.Index(fields=['user']),
        ]

    def __str__(self):
        if self.user:
            return f"{self.user}'s wishlist: {self.product.name}"
        return f"Guest ({self.session_key}) wishlist: {self.product.name}"
