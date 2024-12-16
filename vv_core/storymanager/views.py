from django.conf import settings
from django.shortcuts import render
from postmanager.models import Post

def index(request):
    # Fetch all posts and their associated images
    posts_with_images = Post.objects.prefetch_related('images').all()

    # Prepare data for rendering
    post_cards = []
    for post in posts_with_images:
        # Check if the post has at least one associated image
        if post.images.exists():
            post_image = f"{settings.MEDIA_URL}{post.images.first().image}"
            post_cards.append({
                "title": post.title,
                "image_url": post_image,
                "slug": post.slug,
            })

    return render(request, 'storymanager/index.html', {"post_cards": post_cards})
