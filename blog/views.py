from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied, ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from blog.forms import CommentForm
from blog.models import Post, Category, Tag, Comment
from django import forms


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
        context['comment_form'] = CommentForm
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

            # 먼저 부모 클래스의 form_valid() 함수를 이용하여, 필수값이 잘 입력되었는지 확인
            # form_valid()는 추후 클라이언트로 보낼 response(응답) 내용을 리턴한다.
            response = super(PostCreate, self).form_valid(form)

            # 클라이언트로부터 전달받은 request 객체 내부에서
            # POST 방식으로 전달 받았다면 self.request.POST에는 Payload 정보가 존재하는데
            # Payload 정보 중 우리가 추가했던 tags_str 정보를 가져오기 위해 get 함수 사용
            # get 함수가 리턴되는 내용은 클라이언트에서 입력했던 태그 텍스트인데
            # 이를 tags_str 변수에 담은 것이다.
            tags_str = self.request.POST.get('tags_str')

            # tags_str 변수가 객체를 가지고 있다는 뜻은
            # POST 요청을 받았다는 뜻이고, POST 요청일 때만 데이터베이스에
            # 태그를 저장하기 위해서 아래와 같이 if문을 사용하여 분기하였다.
            # (if문을 만족하지 않았다는 뜻은 GET 요청을 받았다는 뜻이다.)
            if tags_str:
                # strip: 벗겨내다는 뜻
                # tags_str 변수에는 문자열이 존재하는데
                # 문자열 좌우에 여백이 존재하면 그 여백을 없앤다는(벗겨낸다)는 뜻이다.
                # 여백을 벗겨낸 결과를 다시 tags_str 변수에 담는다.
                # 예) ' new tag; 한글 태그, python   ' -> 'new tag; 한글 태그, python'
                tags_str = tags_str.strip()

                # tags_str 변수에 담긴 내용 중 콤마(,)를 세미콜론(;)으로 대체한다.
                # 대체한 결과를 다시 tags_str 변수에 담는다.
                # 예) 'new tag; 한글 태그, python' -> 'new tag; 한글 태그; python'
                tags_str = tags_str.replace(',', ';')

                # tags_str 변수에 담긴 내용을 세미콜론(;) 기준으로 쪼개서(split)
                # tags_list 변수에 담는다. 이때 담기는 형태는 배열 형태이다.
                # 예) 'new tag; 한글 태그; python' -> ['new tag',' 한글 태그',' python']
                tags_list = tags_str.split(';')

                # tags_list에 담긴 배열의 항목 하나하나를 for문을 이용해 처리한다.
                for t in tags_list:
                    # tags_list에 담긴 하나의 문자열을 꺼내어 t 변수에 저장된 상태
                    # t.strip()을 하게되면 t 변수에 저장된 내용의 좌우여백의 공백을
                    # 벗겨낸다. 벗겨낸 결과를 t 변수에 담는다.
                    t = t.strip()

                    slug = slugify(t, allow_unicode=True)
                    if len(slug):
                        pass
                    else:
                        return redirect('/blog/create_post/?error=true')

                    # get_or_create() 함수는 리턴되는 값이 2개이다.
                    # 1. name 속성에 대입한 t(문자열)가 Tag 테이블의 name속성에 존재한다면
                    # get() 함수와 같이 동작을 하게되고,
                    # tag 변수에 t 문자열로 name 필드를 이용하여 검색했던 Tag 객체가 저장되고,
                    # is_tag_created 변수에는 False 값이 저장된다.
                    # 2. create() 함수와 같이 동작을 하면
                    # tag 변수에는 새롭게 생성된 Tag 객체가 저장이 되고,
                    # is_tag_created 변수에는 True 값이 저장된다.
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)

                    # 만약 Tag 테이블에 새로운 태그가 저장되었다면
                    if is_tag_created:
                        # slugify() 함수를 통해 slug 값을 생성하고
                        # 생성한 slug 값을 tag 객체에 담는다.
                        # t는 태그의 이름값(문자열)인데 만약 'new tag'일 경우
                        # 'new tag'를 'new-tag'로 변환시켜준다.
                        # allow_unicode=True는 유니코드 값을 허용한다는 뜻인데,
                        # 한글은 unicode로 구성되어 있어 한글을 지원하겠다는 뜻이다.
                        # 예) '한글 태그' -> '한글-태그'
                        tag.slug = slugify(t, allow_unicode=True)

                        # 최종 완성된 태그를 실제 데이터베이스에 반영(update) 한다.
                        tag.save()

                    # self.object는 현재 작성하고 있는 Post 객체인데
                    # Post 객체의 tags 필드에 추가된다.
                    # 예)
                    # for문 첫번째 바퀴: ['new tag']
                    # for문 두번째 바퀴: ['new tag', '한글 태그']
                    # for문 세번째 바퀴: ['new tag', '한글 태그', 'python']
                    self.object.tags.add(tag)

            # 모든 처리가 끝나고 위에서 선언했던 response를 리턴한다.
            # PostCreate 클래스의 부모클래스의 CreateView의 form_valid() 결과
            return response

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
    fields = ['title', 'hook_text', 'content', 'head_image',
              'file_upload', 'category']

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

    def get_context_data(self, **kwargs):
        # PostUpdate 클래스의 부모클래스의 get_context_data() 함수를 먼저 호출한다.
        # 먼저 호출하게 되면 현재 Post 테이블의 내용을 가져와서 context 변수에 담는다.
        context = super(PostUpdate, self).get_context_data()
        
        # self.object는 현재 수정하고자 하는 Post 글의 객체이다.
        # self.object.tags는 현재 수정하고자 하는 글의 tag들이 저장된 객체이고
        # self.object.tags.exists()는 tags 필드에 값이 존재하는지(tag가 저장되었는지)
        # 확인하는 함수이다. 존재한다면 True, 그렇지 않으면 False 리턴

        # 만약 태그가 존재하는 Post 글일 경우
        if self.object.tags.exists():
            # 빈 리스트를 생성하여 tags_str_list 변수에 담는다. []
            tags_str_list = list()

            # 현재 수정글의 tag 개수만큼 for문을 반복한다.
            # 왜나하면 self.object.tags.all() 함수를 호출하여
            # 현재 수정글의 태그 객체 전부를 가져왔기 때문이다.
            for t in self.object.tags.all():
                # tags_str_list 리스트 변수에 태그의 name(문자열)을 추가한다.
                # 예) ['파이썬', '장고']
                tags_str_list.append(t.name)

            # tags_str_list 변수에 담긴 리스트를 가지고 분리자 세미콜론(;)을 사용하여
            # 새로운 문자열을 생성하는 join() 함수를 사용하여 태그 문자열을 만들고,
            # 만든 문자열을 템플릿으로 전달하기 위해서 context에 tags_str_default를
            # 추가한다.
            # 예) '파이썬; 장고'
            context['tags_str_default'] = '; '.join(tags_str_list)
        return context

    # 클라이언트의 form 양식에 작성한 내용을 전달 받은 후
    # 작성한 내용 중 필수 값을 입력했는지 이상 유무를 점검하는 form_vaild() 함수
    # form 파라메터에는 클라이언트로부터 전달받은 내용이 저장되어 있다.
    def form_valid(self, form):
        # 우선 PostUpdate 클래스의 부모클래스의 form_valid() 함수를 호출하여
        # tags 필드를 제외한 나머지 필드들을 먼저 점검한다.
        # 점검 후 다시 response 변수에 결과를 담는다.
        response = super(PostUpdate, self).form_valid(form)

        # 현재 Post 글의 tags 필드에 저장된 태그들을 모두 삭제한다.
        # 왜냐하면 태그 하나하나 비교해서 추가/삭제하여 수정하는 것 보단
        # 내용을 모두 비운 뒤, 클라이언트로부터 전달받은 tags_str 내용을
        # 다시 넣어주는 것이 더 간단한 로직(Logic)이기 때문이다.
        self.object.tags.clear()

        # 클라이언트의 POST 요청내용(self.request.POST) 중
        # tags_str 변수에 담긴 내용을 tags_str 변수에 담는다.
        # 예) '파이썬; 장고, 자바'
        tags_str = self.request.POST.get('tags_str')

        # 클라이언트가 POST 요청을 했고, tags_str 변수값이 존재한다면
        # 아래 if문을 수행하게 된다.
        if tags_str:
            # tags_str 변수의 문자열 좌우여백을 제거
            tags_str = tags_str.strip()
            # tags_str 변수의 문자열 중 콤마(,)를 세미콜론(;)으로 변경
            # 예) '파이썬; 장고; 자바'
            tags_str = tags_str.replace(',', ';')
            # 문자열을 세미콜론(;) 기준으로 나누어 리스트 형태로 만든 뒤
            # tags_list 변수에 담는다.
            # ['파이썬', ' 장고', ' 자바']
            tags_list = tags_str.split(';')

            # tags_list 리스트를 순회하면서 for문을 수행한다.
            for t in tags_list:
                # 리스트 내부의 문자열 좌우여백을 제거
                t = t.strip()

                slug = slugify(t, allow_unicode=True)
                if len(slug):
                    pass
                else:
                    return redirect('/blog/update_post/?error=true')

                # 태그 문자열을 이용하여 name 필드로 검색한다.
                # 존재하는 태그이면 is_tag_created는 False가 저장되고,
                # 존재하지 않는 태그이면 is_tag_created는 True가 된다.
                tag, is_tag_created = Tag.objects.get_or_create(name=t)

                # Tag 테이블에 태그가 새롭게 추가되었다면
                if is_tag_created:
                    # 태그 문자열을 slugify() 함수를 이용하여 slug 형태로 바꾸어
                    # tag의 slug 필드에 저장한다.
                    tag.slug = slugify(t, allow_unicode=True)
                    # 완성된 tag 객체를 데이터베이스의 Tag 테이블에 저장한다.
                    tag.save()

                # 현재 Post 글의 tags 필드에 완성된 tag 객체를 추가한다.
                self.object.tags.add(tag)

        return response

# 댓글 작성 POST 요청이 들어올 경우 처리
def new_comment(request, pk):

    # 로그인한 경우
    if request.user.is_authenticated:
        # 요청받은 주소에서 pk 번호를 이용해 Post 테이블을 조회
        # 해당 pk를 가지는 포스트가 존재한다면 get 동작 수행
        # 그렇지 않으면 404 예외발생하여 코드 실행을 중단하고
        # 클라이언트에게 404 응답을 보내게 된다.
        post = get_object_or_404(Post, pk=pk)

        # request 요청 내용 중 method 변수를 확인하여
        # POST 요청인지 확인한다.
        if request.method == 'POST':
            # CommentForm에 POST 요청받은 내용을 담아 form 객체를 생성
            comment_form = CommentForm(request.POST)
            # form 객체 내부의 is_valid() 함수를 실행하여 유효성 검사 후
            # 이상이 없다면 if문 실행
            if comment_form.is_valid():
                # comment_form에 담긴 내용을 DB에 저장하는 동작은 하지만
                # 트랜젝션(Transaction)은 이뤄지지 않았다. (commit=False)
                # comment 변수에는 Comment 객체가 담겨져 있다.
                comment = comment_form.save(commit=False)
                # comment 객체에 post 필드를 채워준다. (처음 pk로 불러온 Post)
                comment.post = post
                # author 필드는 현재 로그인한 사용자의 객체를 담는다.
                comment.author = request.user
                # comment 객체의 모든 내용을 채웠으므로
                # 최종적으로 데이터베이스에 저장한다. 트랜젝션이 이루어진다.
                
                # 우리가 만든 별점 버튼을 이용해서 받은 별점을 comment의 score
                # 필드에 저장
                comment.score = request.POST.get('my_score')
                comment.save()
                # 댓글이 작성된 곳으로 페이지 이동한다.
                return redirect(comment.get_absolute_url())
        else:
            # POST 방식이 아닌 요청이 들어온 경우는
            # 포스트 상세페이지로 다시 이동한다.
            return redirect(post.get_absolute_url())
    else:
        # 로그인하지 않은 사용자가 접근한 경우는 PermissionDenied 예외를 발생시키고
        # 허가거부 페이지를 응답으로 보내게 된다.
        raise PermissionDenied

class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and \
                request.user == self.get_object().author:
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def form_valid(self, form):
        response = super(CommentUpdate, self).form_valid(form)
        my_score = self.request.POST.get('my_score')

        if my_score and (0 < int(my_score) <= 5):
            self.object.score = my_score
            self.object.save()

        else:
            raise ValueError('별점은 1~5점을 입력하셔야 합니다.')

        return response

def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post
    if request.user.is_authenticated and request.user == comment.author:
        comment.delete()
        return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied


