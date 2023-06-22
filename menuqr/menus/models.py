from django.db import models
from django.core.files import File
import qrcode
from io import BytesIO
from PIL import Image, ImageDraw

# Create your models here.

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    price = models.FloatField()

    def __str__(self):
        return self.name

class Food(models.Model):
    name = models.CharField(max_length=100)
    items = models.ManyToManyField(Item)

    def __str__(self):
        return self.name

class Menu(models.Model):
    name = models.CharField(max_length=100)
    foods = models.ManyToManyField(Food)

    def __str__(self):
        return self.name

class Business(models.Model):
    name = models.CharField(max_length=100)
    email_address = models.EmailField(max_length=100)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)
    phone = models.IntegerField()
    facebook = models.URLField(max_length=100)
    instagram = models.URLField(max_length=100)
    menus = models.OneToOneField(Menu, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        qrcode_url = f'http://127.0.0.1:8000/{self.name}'
        qrcode_img = qrcode.make(qrcode_url)
        canvas = Image.new('RGB', (360, 360), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        filename = f'{self.name}-qr_code.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(filename, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)
