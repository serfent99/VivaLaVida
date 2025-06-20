import re  # Add this line at the top of your forms.py file
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django import forms
from .models import Music, Artist,Album,Price,CustomUser

class MusicForm(forms.ModelForm):
    artist = forms.ModelChoiceField(queryset=Artist.objects.all(), empty_label="Select Artist", widget=forms.Select(attrs={'class': 'form-control'}))
    album = forms.ModelChoiceField(queryset=Album.objects.all(), label="Select Album",widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Music
        fields = ['title', 'artist', 'album', 'release_date', 'genre']
        labels = {
            'title': 'Title',
            'artist': 'Artist',
            'album': 'Album',
            'release_date': 'Release Date',
            'genre': 'Genre',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'release_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'genre': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ArtistForm(forms.ModelForm):
    TYPE_CHOICES = (
        ('Solo', 'Solo'),
        ('Group', 'Group'),
    )

    typeartist = forms.ChoiceField(choices=TYPE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Artist
        fields = ['Artist', 'bio', 'country', 'typeartist']  # Updated 'name' to 'Artist'
        labels = {
            'Artist': 'Name',  # Updated 'name' to 'Artist'
            'bio': 'Bio',
            'country': 'Country',
            'typeartist': 'Type of Artist',
        }
        widgets = {
            'Artist': forms.TextInput(attrs={'class': 'form-control'}),  # Updated 'name' to 'Artist'
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
        }

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['album_name', 'artist', 'date_done']
        labels = {
            'album_name': 'Album Name',
            'artist': 'Artist',
            'date_done': 'Completion Date',
            'cover_image': 'Cover Image',
        }
        widgets = {
            'album_name': forms.TextInput(attrs={'class': 'form-control'}),
            'artist': forms.Select(attrs={'class': 'form-control'}),
            'date_done': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        }

class PriceForm(forms.ModelForm):
    album = forms.ModelChoiceField(queryset=Album.objects.all(), label="Select Album",widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Price
        fields = ['album', 'price']
        labels = {
            'price': 'Album Price',
        }
        widgets = {
            'price' : forms.NumberInput(attrs={'class': 'form-control'})
        }

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254, required=True, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(label="Password", strip=False, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    
class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user
