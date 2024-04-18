from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Feedlist
from .forms import FeedForm
from django.http import JsonResponse
from .models import Category
from .models import Feedlist

@login_required
def feedlist_view(request):
    feedlist = Feedlist.objects.filter(is_published=True).order_by('-time_create')
    return render(request, 'feed/feedlist.html', {'feedlist': feedlist})

@login_required
def create_feed(request):
    categories = Category.objects.all()
    if request.user.is_staff and request.method == 'POST':
        form = FeedForm(request.POST, categories=categories)  
        if form.is_valid():
            feed = form.save(commit=False)
            feed.user = request.user
            feed.save()
            return JsonResponse({'success': True})
    else:
        form = FeedForm(categories=categories)  
    feedlist = Feedlist.objects.all()  
    return render(request, 'feed/feedlist.html', {'form': form, 'feedlist': feedlist})

@login_required
def edit_feed(request, pk):
    feed = get_object_or_404(Feedlist, pk=pk)
    if request.user.is_staff or request.user == feed.user:
        if request.method == 'POST':
            form = FeedForm(request.POST, instance=feed)
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True})
            else:
                print("Form is not valid:", form.errors)
                return JsonResponse({'success': False, 'error': 'Form is not valid'})
        elif request.method == 'GET':
            # Возвращаем данные записи для редактирования в формате JSON
            data = {
                'title': feed.title,
                'content': feed.content,
            }
            return JsonResponse(data)
    print("Reached the end of the view function for editing feed.")
    return JsonResponse({'success': False, 'error': 'Failed to edit feed'})

@staff_member_required
def delete_feed(request, pk):
    feed = get_object_or_404(Feedlist, pk=pk)
    if request.user.is_staff or request.user == feed.user:
        if request.method == 'POST':
            feed.delete()
            return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Failed to delete feed'})
