from django.shortcuts import render
from django.http import HttpResponse
from . import poker

def index(request):
    return render(request, 'index.html')

def game(request):
    output = poker.run_game()
    # Wrap output in <pre> tags to maintain formatting.
    return HttpResponse(f"<pre>{output}</pre>")
