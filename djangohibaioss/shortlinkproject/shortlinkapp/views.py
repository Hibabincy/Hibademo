from django.shortcuts import render, redirect, get_object_or_404
import random, string
from .forms import ShortLinkForm
from .models import ShortLink

# Create your views here.
def index(request):
    return render(request,'index.html')


def generate_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

def home(request):
    short_url = None
    if request.method == 'POST':
        form = ShortLinkForm(request.POST)
        if form.is_valid():
            short_code = generate_code()
            link = form.save(commit=False)
            link.short_code = short_code
            link.save()
            short_url = request.build_absolute_uri(f'/{short_code}')
    else:
        form = ShortLinkForm()
    return render(request, 'home.html', {'form': form, 'short_url': short_url})

def redirect_to_original(request, code):
    link = get_object_or_404(ShortLink, short_code=code)
    return redirect(link.original_url)
