from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect


from .utils import MD5Strategy, SHA256Strategy, RandomStrategy
from .models import ShortURL
# from django.http import request


def _is_short_url_valid(search_url: str):
    """Search url in db
    
    :param search_url: link in db
    :return: boolean
    """
    return not ShortURL.objects.filter(short_url=search_url).exists()


@login_required
def url(request):
    """Work in url page

    :param request:
    :return: page with short url
    """
    is_valid = False
    if request.method == "POST":
        long_url = request.POST.get('url')
        algorithm = request.POST.get("algorithm", None)

        if algorithm == "md5":
            strategy = MD5Strategy()
        elif algorithm == "sha256":
            strategy = SHA256Strategy()
        else:
            strategy = RandomStrategy()

        while not is_valid:
            short_url = strategy.get_short_url(long_url)
            if short_url is None:
                is_valid = False
            else:
                is_valid = _is_short_url_valid(short_url)

        first_part = request.get_host()
        full_url = f"http://{first_part}/yourdomain/{short_url}"

        ShortURL.objects.create(long_url=long_url, short_url=short_url, full_url=full_url, user_id=request.user)

        return render(request, 'short_link/general_pages/url.html', context={"short_link": full_url,
                                                                             "long_link": long_url})

    return render(request, 'short_link/general_pages/url.html', context={"short_link": "",
                                                                         "long_link": ""})


@login_required
def open_long_url(request, short_url: str):
    """Open page for short user url

    :param request:
    :param short_url: short url
    :return:
    """
    try:
        long_url = ShortURL.objects.all().get(short_url=short_url, user_id=request.user.id).long_url
        return HttpResponseRedirect(long_url)
    except Exception as e:
        return HttpResponseRedirect("/")


@login_required
def home_page(request):
    return render(request, 'short_link/general_pages/home.html')


@login_required
def account(request):
    data = ShortURL.objects.all().filter(user_id=request.user.id).values('long_url', 'full_url')

    return render(request, 'short_link/general_pages/account.html', context={"data": data})


def register_request(request):
    """registration

    :param request:
    :return:
    """
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("/")
        messages.error(request, "Unsuccessful registration. Invalid information.")

    form = NewUserForm()

    return render(request=request,
                  template_name="short_link/login_register/register.html",
                  context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("/")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="short_link/login_register/login.html", context={"login_form": form})


def logout_view(request):
    logout(request)
    return redirect("short_link/general_pages/login.html", args=(), kwargs={})

