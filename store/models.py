from django.db import models
from django.contrib.auth.models import User

class Developer(models.Model):
    developer_name = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    foundation_date = models.DateField()
    picture = models.ImageField("Изображение", null=True, upload_to="developers")

    def __str__(self):
        return self.developer_name

class Game(models.Model):
    STATUS_CHOICES = [
        ('beta', 'Beta'),
        ('released', 'Released'),
        ('early access', 'Early Access'),
        ('coming soon', 'Coming Soon'),
    ]

    game_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    score = models.FloatField(default=0)
    info = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='coming soon')
    system_requirements = models.TextField()
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)
    picture = models.ImageField("Изображение", null=True, upload_to="games")

    def __str__(self):
        return self.game_name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    avatar = models.URLField(blank=True)

    def __str__(self):
        return self.user.username

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    price_at_purchase = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} — {self.game.game_name}"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    review_text = models.TextField()
    rating = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} — {self.game.game_name}"
