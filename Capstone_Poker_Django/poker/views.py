from django.shortcuts import render
import os
import subprocess
# Create your views here.
from django.http import HttpResponse
from . import poker as poker
def index(request):
 
   return render(request, 'index.html')


def game(request):
   poker.main()
   return render(request,'index.html')