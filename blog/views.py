from django.shortcuts import render
from django.views.generic import ListView, DetailView

from blog.models import Post, Category


# CBV (Class Based View) 방식
class PostList(ListView):
    model = Post
    ordering = '-pk'
    # template 명은 post_list.html (모델명_list.html)
    # template로 넘길 때 사용하는 변수명은 post_list (모델명_list)

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects\
            .filter(category=None).count()
        return context

# FBV (Function Based View) 방식
# def index(request):
#     # Post 테이블 내용 전체 가져오기
#     posts = Post.objects.all().order_by('-pk')
#
#     return render(
#         request,
#         'blog/post_list.html',
#         {
#             'posts1': posts,
#         }
#     )

# CBV (Class Based View) 방식
class PostDetail(DetailView):
    model = Post
    # 서버주소/blog/pk에서 pk 값을 가지고 자동으로 데이터베이스의 내용을 가져옴
    # template 명은 post_detail.html (모델명_detail.html)
    # template에서 사용할 변수명은 post (모델명)

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None)\
            .count()
        return context

# FBV (Function Based View) 방식
# def single_post_page(request, pk):
#     post = Post.objects.get(pk=pk)
#
#     return render(
#         request,
#         'blog/post_detail.html',
#         {
#             'post': post,
#         }
#     )


