from django.db import models


class Currency(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=5)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_value = models.ImageField(upload_to='images/')
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.name







