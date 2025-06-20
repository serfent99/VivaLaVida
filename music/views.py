from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import Music, Artist, Album, Price, CustomUser
from .forms import MusicForm, ArtistForm, AlbumForm, PriceForm, LoginForm, RegistrationForm
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from .decorators import role_required
from django.db.models import Q

User = get_user_model()

def userlogin(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(reverse('index'))
        else:
            messages.success(request, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, 'authority/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'viewer'
            user.save()
            login(request, user)
            messages.success(request, 'Registration successful. You are now logged in.')
            return redirect('index')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = RegistrationForm()
    return render(request, 'authority/register.html', {'form': form})

def no_permission(request):
    return render(request, 'authority/NoPermission.html')

@login_required
@role_required(['admin'])
def manage_roles(request):
    if request.method == 'POST':
        user_id = request.POST['user']
        role = request.POST['role']
        user = CustomUser.objects.get(id=user_id)
        user.role = role
        user.save()
        messages.success(request, f"Successfully assigned role '{role}' to user '{user.username}'.")
        return redirect('authority')
    users = CustomUser.objects.all()
    roles = ['viewer', 'editor', 'admin']
    return render(request, 'authority/authoritys.html', {'users': users, 'roles': roles})

def logoutnows(request):
    logout(request)
    return redirect('login')
@login_required
def index(request):
    query = request.GET.get('q', '')
    if query:
        music_list = Music.objects.filter(
            Q(title__icontains=query) |
            Q(artist__icontains=query) |
            Q(album__icontains=query) |
            Q(genre__icontains=query) |
            Q(release_date__icontains=query)
        )
    else:
        music_list = Music.objects.all()
    return render(request, 'musics/index.html', {'music_list': music_list, 'query': query})

@login_required
def artist_index(request):
    query = request.GET.get('q', '')
    if query:
        artist_list = Artist.objects.filter(
            Q(Artist__icontains=query) |
            Q(bio__icontains=query) |
            Q(country__icontains=query) |
            Q(typeartist__icontains=query)
        )
    else:
        artist_list = Artist.objects.all()
    return render(request, 'artists/index.html', {'artist_list': artist_list, 'query': query})

@login_required
def album_index(request):
    query = request.GET.get('q', '')
    if query:
        album_list = Album.objects.filter(
            Q(album_name__icontains=query) |
            Q(artist__Artist__icontains=query) |
            Q(date_start__icontains=query) |
            Q(date_done__icontains=query)
        )
    else:
        album_list = Album.objects.all()
    return render(request, 'albums/index.html', {'album_list': album_list, 'query': query})

@login_required
def price_index(request):
    query = request.GET.get('q', '')
    if query:
        price_list = Price.objects.filter(
            Q(album__album_name__icontains=query) |
            Q(album__artist__Artist__icontains=query) |
            Q(price__icontains=query) |
            Q(date__icontains=query)
        )
    else:
        price_list = Price.objects.all()
    return render(request, 'prices/index.html', {'price_list': price_list, 'query': query})


@login_required
def view_music(request, id):
    music = get_object_or_404(Music, pk=id)
    return render(request, 'musics/view.html', {
        'music': music
    })

@login_required
@role_required(['admin', 'editor'])
def add(request):
    if request.method == 'POST':
        form = MusicForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'musics/add.html', {
                'form': MusicForm(),
                'success': True
            })
    else:
        form = MusicForm()
    return render(request, 'musics/add.html', {
        'form': form
    })

@login_required
def edit(request, id):
    music = get_object_or_404(Music, pk=id)
    if request.method == 'POST':
        form = MusicForm(request.POST, instance=music)
        if form.is_valid():
            form.save()
            return render(request, 'musics/edit.html', {
                'form': form,
                'success': True
            })
    else:
        form = MusicForm(instance=music)
    return render(request, 'musics/edit.html', {
        'form': form
    })

@login_required
@role_required(['admin', 'editor'])
def delete(request, id):
    music = get_object_or_404(Music, pk=id)
    if request.method == 'POST':
        music.delete()
        return HttpResponseRedirect(reverse('index'))
    return render(request, 'musics/delete.html', {
        'music': music
    })


@login_required
def view_artist(request, id):
    artist = get_object_or_404(Artist, pk=id)
    return render(request, 'artists/view.html', {
        'artist': artist
    })

@login_required
@role_required(['admin', 'editor'])
def add_artist(request):
    if request.method == 'POST':
        form = ArtistForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'artists/add.html', {
                'form': ArtistForm(),
                'success': True
            })
    else:
        form = ArtistForm()
    return render(request, 'artists/add.html', {
        'form': form
    })

@login_required
@role_required(['admin', 'editor'])
def edit_artist(request, id):
    artist = get_object_or_404(Artist, pk=id)
    if request.method == 'POST':
        form = ArtistForm(request.POST, instance=artist)
        if form.is_valid():
            form.save()
            return render(request, 'artists/edit.html', {
                'form': form,
                'success': True
            })
    else:
        form = ArtistForm(instance=artist)
    return render(request, 'artists/edit.html', {
        'form': form
    })

@login_required
@role_required(['admin', 'editor'])
def delete_artist(request, id):
    artist = get_object_or_404(Artist, pk=id)
    if request.method == 'POST':
        artist.delete()
        return HttpResponseRedirect(reverse('artist_index'))
    return render(request, 'artists/delete.html', {
        'artist': artist
    })


@login_required
def view_album(request, id):
    album = get_object_or_404(Album, pk=id)
    return render(request, 'albums/view.html', {
        'album': album
    })

@login_required
@role_required(['admin', 'editor'])
def add_album(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'albums/add.html', {
                'form': AlbumForm(),
                'success': True
            })
    else:
        form = AlbumForm()
    return render(request, 'albums/add.html', {
        'form': form
    })

@login_required
@role_required(['admin', 'editor'])
def edit_album(request, id):
    album = get_object_or_404(Album, pk=id)
    if request.method == 'POST':
        form = AlbumForm(request.POST, instance=album)
        if form.is_valid():
            form.save()
            return render(request, 'albums/edit.html', {
                'form': form,
                'success': True
            })
    else:
        form = AlbumForm(instance=album)
    return render(request, 'albums/edit.html', {
        'form': form
    })

@login_required
@role_required(['admin', 'editor'])
def delete_album(request, id):
    album = get_object_or_404(Album, pk=id)
    if request.method == 'POST':
        album.delete()
        return HttpResponseRedirect(reverse('album_index'))
    return render(request, 'albums/delete.html', {
        'album': album
    })


@login_required
def view_price(request, id):
    price = get_object_or_404(Price, pk=id)
    return render(request, 'prices/view.html', {
        'price': price
    })

@login_required
@role_required(['admin', 'editor'])
def add_price(request):
    if request.method == 'POST':
        form = PriceForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'prices/add.html', {
                'form': PriceForm(),
                'success': True
            })
    else:
        form = PriceForm()
    return render(request, 'prices/add.html', {
        'form': form
    })

@login_required
@role_required(['admin', 'editor'])
def edit_price(request, id):
    price = get_object_or_404(Price, pk=id)
    if request.method == 'POST':
        form = PriceForm(request.POST, instance=price)
        if form.is_valid():
            form.save()
            return render(request, 'prices/edit.html', {
                'form': form,
                'success': True
            })
    else:
        form = PriceForm(instance=price)
    return render(request, 'prices/edit.html', {
        'form': form
    })

@login_required
@role_required(['admin', 'editor'])
def delete_price(request, id):
    price = get_object_or_404(Price, pk=id)
    if request.method == 'POST':
        price.delete()
        return HttpResponseRedirect(reverse('price_index'))
    return render(request, 'prices/delete.html', {
        'price': price
    })

@login_required
def profile_view(request):
    return render(request, 'profile/profile.html', {'user': request.user})

@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        new_username = request.POST.get('username')
        email = request.POST.get('email')

        if new_username != user.username and User.objects.filter(username=new_username).exists():
            messages.error(request, 'Username is already taken.')
        else:
            user.username = new_username
            user.email = email
            user.save()
            return redirect('profile')

    return render(request, 'profile/edit_profile.html')

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, 'Your account has been deleted.')
        return redirect('home')
    else:
        return redirect('profile')

