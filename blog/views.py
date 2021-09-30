from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from blog.models import Post, Category, Tag


# CBV (Class Based View) 방식
class PostList(ListView):
    template_name = 'blog/test_abc.html'
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

def tag_page(request, slug):
    # URL 주소로 전달받은 slug 값을 이용하여 Tag 테이블을 검색한다.
    # 예) slug 값이 hello일 경우는 Tag 테이블에서 slug가 hello인 태그를 찾고
    # 찾은 태그를 객체화해서 tag 변수에 담는다.
    tag = Tag.objects.get(slug=slug)

    # tag 변수에 담긴 태그 객체를 가지는 Post들을 불러와서 post_list 변수에 담는다.
    post_list = tag.post_set.all()

    # 템플릿은 post_list.html을 사용
    # 글 목록은 위에서 작성한 post_list 변수에 담겨 있고,
    # 템플릿에 넘길 때 post_list 변수로 넘긴다.
    # tag는 현재 화면에 보이는 태그페이지의 태그이름
    # categories는 카테고리 카드에 사용하기 위한 변수
    # no_category_post_count는 카테고리를 가지지 않은 포스트의 수
    return render(
        request,
        'blog/post_list.html',
        {
            'post_list': post_list,
            'tag': tag,
            'categories': Category.objects.all(),
            'no_category_post_count': Post.objects.filter(category=None).count()
        }
    )

# CreateView를 상속받아 Form 양식을 자동으로 생성할 수 있다.
class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    # 1. Post 테이블을 사용하기 위해 model 변수에 Post를 대입
    model = Post

    # Form 양식에서 클라이언트로부터 입력받을 정보(Post 테이블의 필드명)를
    # fields 변수에 대입한다.
    fields = ['title', 'hook_text', 'content', 'head_image',
              'file_upload', 'category']

    # UserPassesTestMixin 클래스의 test_func() 함수 재정의
    # test_func() 함수가 True를 리턴하도록 만들면 포스트 작성 페이지 접속이 가능하다.
    # 아래는 최고관리자 권한 혹은 스테프 권한을 가졌다면 포스트 작성페이지 접속이 가능한 것이다.
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    # form_valid() 함수는 CreateView 클래스에 정의된 form_valid() 함수를 재정의
    # form_valid() 함수의 역할은 필수 입력 값과 제약사항이 지켜졌는지 확인하는 함수
    # 이상이 없다면 클라이언트는 정상적인 결과 페이지를 받게 되고,
    # 이상이 있다면 장고가 작성해준 form 영역에 이상여부를 표시해준다.
    def form_valid(self, form):
        # self.request는 클라이언트가 서버로 요청한 정보를 담고있는 객체
        # self.request.user는 현재 로그인한 사용자의 정보를 담고있는 User 객체
        current_user = self.request.user

        # is_authenticated: 현재 사용자가 로그인한 상태이면 True, 아니면 False
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            # form.instance는 클라이언트에서 form을 통해 입력한 내용을 담고있다.
            # 현재 사용자 정보를 author 필드에 채워 넣어준다. (테스트코드 오류 해결)
            form.instance.author = current_user
            # 우리가 원하는 부분 처리가 끝나고 최종적으로 PostCreate 클래스의 부모인
            # CreateView 클래스의 form_valid() 함수를 실행한다.
            # 실행할 때 author 필드가 채워진 form 객체를 전달받아
            # 기존에 CreateView가 했던 데이터베이스에 글 등록하는 기능을 수행하게 된다.
            return super(PostCreate, self).form_valid(form)
        else:
            # 현재 사용자가 로그아웃 상태일 경우는 목록 페이지로 이동한다.
            # 이동하고자 하는 URL 주소를 redirect() 함수의 파라메터로 넘겨주면 된다.
            return redirect('/blog/')

# 포스트 수정 페이지를 위한 클래스 CBV 방식
# 로그인한 사용자만 접근할 수 있도록 LoginRequiredMixin 클래스를 상속받는다.
# 장고에서 제공하는 UpdateView를 상속받으면 수정페이지에서 수정할 정보를 입력받는
# 영역을 장고가 자동으로 작성해준다.
class PostUpdate(LoginRequiredMixin, UpdateView):
    # 수정 대상 모델을 지정
    model = Post
    # 수정 대상 필드명을 지정
    # 장고는 model, fields 내용을 가지고 클라이언트의 form을 구성하게 된다.
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload',
            'category', 'tags']

    # 수정페이지의 템플릿명을 지정
    template_name = 'blog/post_update_form.html'

    # UpdateView에 정의되어 있는 dispatch() 함수를 재정의한다.
    # 원래는 if문의 return 키워드 옆에 있는 코드와 같이
    # UpdateView의 dispatch() 함수를 실행하여 기본동작을 수행하지만
    # 기본동작을 중간에 가로채서 if문을 이용해 분기점을 만들어준다.
    # 1. 사용자가 로그인한 상태이고 현재 사용자가 현재글의 작성자와 동일할 경우는
    # UpdateView의 dispatch() 함수를 그대로 실행하게 하여 페이지에 정상 접속하게 하고,
    # 2. 그렇지 않다면 else문이 실행되는데, raise라는 키워드를 사용하여
    # 예외를 발생시킨다. (PermissionDenied는 상태코드 403을 만들어 서버가 응답하게 된다.)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied