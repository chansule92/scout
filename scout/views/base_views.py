from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from ..models import  lck_2021_spring_player
from django.db.models import Q





def index(request):
    list=None
    query=None
    test=0
    if 'word' in request.GET:
        query=request.GET.get('word')
        list=lck_2021_spring_player.objects.values().filter(Q(nickname__icontains=query)|Q(team__icontains=query))

    context = {'test':test, 'list':list}
    return render(request, 'scout/index.html', context)
