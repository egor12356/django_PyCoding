from django.shortcuts import render

# Create your views here.

def test_view(requests):
    return render(requests, 'base.html')