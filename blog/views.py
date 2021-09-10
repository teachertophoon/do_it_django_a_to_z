from django.shortcuts import render

from blog.models import Post


def index(request):
    # Post 테이블 내용 전체 가져오기
    posts = Post.objects.all().order_by('-pk')

    return render(
        request,
        'blog/index.html',
        {
            'posts1': posts,
        }
    )
