from django.db import models
from django.contrib.auth.models import Permission,AbstractUser, Group
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class Music(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=50)
    album = models.CharField(max_length=50)
    release_date = models.DateField()
    genre = models.CharField(max_length=50)



    def __str__(self):
        return f'Music: {self.title} by {self.artist}'

class Artist(models.Model):
    id = models.AutoField(primary_key=True)
    Artist = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    country = models.CharField(max_length=50, blank=True)
    typeartist = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f"{self.Artist} - {self.typeartist}"

class Album(models.Model):
    id = models.AutoField(primary_key=True)
    album_name = models.CharField(max_length=100)
    artist = models.ForeignKey('Artist', on_delete=models.CASCADE)
    date_start = models.DateField(_("Start Date"), default=timezone.now)
    date_done = models.DateField()
    
    def __str__(self):
        return self.album_name
    
class Price(models.Model):
    id = models.AutoField(primary_key=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='prices')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.album} - {self.price}'
    

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('viewer', 'Viewer'),
        ('editor', 'Editor'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='viewer')

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Use a unique related name
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',  # Use a unique related name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def has_permission(self, perm):
        if self.role == 'admin':
            return True
        if self.role == 'editor' and perm in ['add', 'change']:
            return True
        if self.role == 'viewer' and perm == 'view':
            return True
        return False
    
