from django.db import models
import uuid
# from  django.conf import settings


# Create your models here.

        
class Category(models.Model):
    title = models.CharField(max_length=200)
    category_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
  

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['-title']

    def __str__(self):
        return self.title