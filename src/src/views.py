from django.shortcuts import render
#from django.shortcuts import redirect
#from django.conf import settings


def cookie(request):
    context = {}
    return render(request,'cookie.html', context)

def progetto(request):
    context = {'value':'progetto'}
    return render(request,'progetto.html', context)
    
def heatmap(request):
    context ={}
    return render(request,'heatmap.html',context)