from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.views.generic import ListView, DetailView
from django.views.generic.dates import ArchiveIndexView, YearArchiveView

from .models import Post, Image
from django.utils import timezone
from openai import OpenAI
import requests
import os
from django.conf import settings
import threading
from decouple import config

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

# OpenAI API 키 설정
OPENAI_API_KEY = config("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

def process_post_and_generate_image(post_id, content_text):
    try:
        # 1. GPT-4를 사용하여 텍스트 요약
        client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY")
        )

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": content_text,
                },
                {
                    "role": "system",
                    "content": "Summarize the text briefly.",
                }
            ],
            model="gpt-4o"
        )

        summary = chat_completion.choices[0].message.content.strip()
        print(summary)

        # 2. 요약을 기반으로 DALL·E 이미지 생성
        response = client.images.generate(
            prompt=summary,
            size="256x256",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
        print(image_url)

        # 3. 이미지 다운로드 및 저장
        response = requests.get(image_url)
        if response.status_code == 200:
            # 파일 저장 경로
            image_filename = f'images/post_{post_id}_{timezone.now().strftime("%Y%m%d%H%M%S")}.jpg'
            image_path = os.path.join(settings.MEDIA_ROOT, image_filename)
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            with open(image_path, 'wb') as file:
                file.write(response.content)

            # DB에 이미지 정보 저장
            post = Post.objects.get(id=post_id)
            Image.objects.create(post=post, image=image_filename)
        else:
            raise Exception("Failed to download the generated image.")

    except Exception as e:
        print(f"Error processing post {post_id}: {e}")

def post_write_result(request):
    try:
        # POST 데이터 수집
        content_subject = request.POST['post_subject']
        content_text = request.POST['post_content']
        content_date = timezone.localtime()

        # 블로그 포스트 저장
        content_model = Post.objects.create(
            title=content_subject,
            content=content_text,
            create_dt=content_date
        )

        # 비동기로 OpenAI 작업 실행
        threading.Thread(
            target=process_post_and_generate_image,
            args=(content_model.id, content_text)
        ).start()

        # 성공 메시지 반환
        message = f'''
        <script>
        alert('글이 성공적으로 작성되었습니다. 이미지 처리는 백그라운드에서 진행 중입니다.');
        location.href = '/post/post_main';
        </script>
        '''
        return HttpResponse(message)

    except Exception as e:
        # 오류 처리
        error_message = f'''
        <script>
        alert('오류 발생: {str(e)}');
        history.back();
        </script>
        '''
        return HttpResponse(error_message)

