from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.dates import ArchiveIndexView, YearArchiveView

from .models import Post
from django.utils import timezone


def main(request):
    return render(request, 'main.html')


class PostLV(ListView):
    model = Post
    template_name = ('post/post_main.html')
    context_object_name = 'posts'
    paginate_by = 2


class PostDV(DetailView):
    model = Post


class PostAV(ArchiveIndexView):
    model = Post
    date_field = 'modify_date'


# function based view
def post_write(request):
    return render(request, 'post/post_write.html')


def post_write_result(request):
    content_subject = request.POST['post_subject']
    content_text = request.POST['post_content']
    content_date = timezone.localtime()

    content_model = Post()
    content_model.title = content_subject
    content_model.content = content_text
    content_model.create_dt = content_date
    content_model.save()

    message = f'''
    <script>
    alert('글이 성공적으로 작성되었습니다.');
    location.href = '/post/post_list'
    </script>
'''
    return HttpResponse(message)
