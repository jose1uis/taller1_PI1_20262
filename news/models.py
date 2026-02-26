from django.db import models

class News(models.Model):
    headline = models.CharField(max_length=200)
    body = models. TextField ()
    date = models. DateField()
    image = models.ImageField(upload_to='news_images/', null=True, blank=True)

    def str (self): return self.headline