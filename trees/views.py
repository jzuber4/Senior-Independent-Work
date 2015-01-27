from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "trees/index.html")

def question(request):
    pass
