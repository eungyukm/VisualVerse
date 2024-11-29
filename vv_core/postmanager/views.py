from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.views.generic import ListView, DetailView
from django.views.generic.dates import ArchiveIndexView, YearArchiveView

from .models import Post
from django.utils import timezone

class PostDV(DetailView):
    model = Post


class PostAV(ArchiveIndexView):
    model = Post
    date_field = 'modify_date'


# function based view
def post_main(request):
    slug = request.GET.get('slug', None)
    page = request.GET.get('page', 1)

    posts = Post.objects.values('title', 'slug')

    paginator = Paginator(posts, 20)

    current_page_data = None

    try:
        if slug:
            current_page_data = get_object_or_404(Post, slug=slug)

            post_index = list(posts).index({'title': current_page_data.title, 'slug': current_page_data.slug})
            page = (post_index // 20) + 1  # 페이지 번호 계산

        page_obj = paginator.get_page(page)

    except (ValueError, IndexError, Post.DoesNotExist):
        page_obj = paginator.get_page(1)
        current_page_data = None

    if current_page_data and current_page_data.content:
        current_page_data.content = current_page_data.content.strip()

    render_data = {
        'title': 'Post List',
        'titles': posts,
        'page_obj': page_obj,
        'current_slug': slug,
        'current_page_data': current_page_data,
    }

    template = loader.get_template('post/post_main.html')
    return HttpResponse(template.render(render_data, request))


def post_write(request):
    return render(request, 'post/post_write.html')


def post_write_result(request):
    print(request.POST)
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
    location.href = '/post/post_main'
    </script>
'''
    return HttpResponse(message)
