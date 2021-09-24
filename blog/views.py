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
        # post_list 변수에 Post 테이블 내용 전체가 저장된 상태
        context = super(PostList, self).get_context_data()

        # categories 변수에 Category 테이블의 전체 내용을 담아 템플릿으로 보내주기 위해서
        context['categories'] = Category.objects.all()

        # Post 테이블 내용 중
        # category 필드 값이 None인 Post들만 추려서 갯수를 리턴받아
        # no_category_post_count 변수에 저장한 후
        # 템플릿으로 전달하기 위해서 작성
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

# 웹 브라우저에서 /blog/category/[slug] 형태의 주소를 입력 받으면
# blog의 urls.py 파일에서 category_page 함수를 호출한다. (FBV 방식)
# <str:slug>를 통해 생성된 slug 변수를 category_page의 두 번째 파라메터로 전달받는다.
def category_page(request, slug):
    if slug == 'no_category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)

    # URL을 통해서 전달받은 slug 변수를 이용하여
    # Category 테이블을 조회한다.
    # 예) slug 값이 'programming'이면 Category 테이블에서 slug 값이 'programming'인
    # 'programming' 카테고리 객체를 가져와 category 변수에 담는다.
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)

    # FBV 방식은 render 함수를 통해 템플릿으로 변수값들을 전달한다.
    # (CBV 방식의 get_context_data() 함수와 비교해보세요.)
    # 첫 번째 파라메터: 클라이언트로부터 요청받은 request 변수를 그대로 전달
    # 두 번째 파라메터: 템플릿 경로
    # 세 번째 파라메터: 딕셔너리(Dictionary) 형태로 '변수명': 변수값을 작성한다.
    # 세 번째 파라메터 내용이 두 번째 파라메터로 지정한 템플릿으로 전달하게 된다.
    return render(
        request,
        'blog/post_list.html',
        {
            'post_list': post_list,
            'categories': Category.objects.all(),
            'no_category_post_count': Post.objects.filter(category=None).count(),
            'category': category,
        }
    )
