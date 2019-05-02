from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from todo.models import Todo

@login_required
def home(request):
    models = list(Todo.objects.all())
    page = request.GET.get('page', 1)
    paginator = Paginator(models, 5)
    try:
        todos = paginator.page(page)
    except PageNotAnInteger:
        todos = paginator.page(1)
    except EmptyPage:
        todos = paginator.page(paginator.num_pages)
    return render(request, "home.html", context={"todos":todos})

@login_required
def statistics(request):
    return render(request, "statistics.html")
