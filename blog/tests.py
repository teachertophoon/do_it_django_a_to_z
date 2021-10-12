from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.test import TestCase, Client

from blog.models import Post, Category, Tag, Comment


class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_trump =\
            User.objects.create_user(username='trump', password='somepassword')
        self.user_obama =\
            User.objects.create_user(username='obama', password='somepassword')
        # User 객체에 존재하는 is_staff 변수는 스테프인지 아닌지 판단하는 변수이다.
        # 아래는 user_obama User 객체의 is_staff 변수를 True로 바꾸어
        # 오바마 사용자를 스테프 권한을 주도록 바꾼 것이다.
        # 설정이 끝나면 마지막에 User 객체의 save() 함수를 꼭! 실행해야 한다.
        self.user_obama.is_staff = True
        self.user_obama.save()

        self.category_programming = Category.objects\
            .create(name='programming', slug='programming')
        self.category_music = Category.objects\
            .create(name='music', slug='music')
        
        # 모든 테스트에서 활용하기 위해 Tag를 추가하고 변수에 저장
        self.tag_python_kor = Tag.objects.create(name='파이썬 공부', slug='파이썬-공부')
        self.tag_python = Tag.objects.create(name='python', slug='python')
        self.tag_hello = Tag.objects.create(name='hello', slug='hello')

        self.post_001 = Post.objects.create(
            title='첫 번째 포스트입니다.',
            content='Hello World, We are the world.',
            category=self.category_programming,
            author=self.user_trump,
        )
        self.post_001.tags.add(self.tag_hello)

        self.post_002 = Post.objects.create(
            title='두 번째 포스트입니다.',
            content='1등이 전부는 아니잖아요?',
            category=self.category_music,
            author=self.user_obama,
        )

        self.post_003 = Post.objects.create(
            title='세 번째 포스트입니다.',
            content='category가 없을 수도 있죠',
            author=self.user_obama,
        )
        self.post_003.tags.add(self.tag_python_kor)
        self.post_003.tags.add(self.tag_python)

        # 댓글 작성
        self.comment_001 = Comment.objects.create(
            post=self.post_001,
            author=self.user_obama,
            content='첫 번째 댓글입니다.'
        )

    def navbar_test(self, soup):
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)

        # 로고 버튼은 홈으로 이동해야 한다.
        logo_btn = navbar.find('a', text='Do It Django')
        self.assertEqual(logo_btn.attrs['href'], '/')

        # Home 버튼은 홈으로 이동해야 한다.
        home_btn = navbar.find('a', text='Home')
        self.assertEqual(home_btn.attrs['href'], '/')

        # Blog 버튼은 포스트 목록 페이지로 이동해야 한다.
        blog_btn = navbar.find('a', text='Blog')
        self.assertEqual(blog_btn.attrs['href'], '/blog/')

        # About Me 버튼은 자기소개 페이지로 이동해야 한다.
        about_me_btn = navbar.find('a', text='About Me')
        self.assertEqual(about_me_btn.attrs['href'], '/about_me/')

    # 카테고리 카드영역 테스트
    def category_card_test(self, soup):
        categories_card = soup.find('div', id='categories-card')
        self.assertIn('Categories', categories_card.text)
        self.assertIn(f'{self.category_programming.name} '
                      f'({self.category_programming.post_set.count()})',
                      categories_card.text)
        self.assertIn(f'{self.category_music.name} '
                      f'({self.category_music.post_set.count()})',
                      categories_card.text)
        self.assertIn(f'미분류 (1)', categories_card.text)

    # 테스트할 함수명 앞에는 꼭 test_를 붙여 주셔야 합니다.
    def test_post_list(self):
        # 포스트가 있는 경우
        self.assertEqual(Post.objects.count(), 3)

        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.navbar_test(soup)
        self.category_card_test(soup)

        main_area = soup.find('div', id='main-area')
        self.assertNotIn('아직 게시물이 없습니다', main_area.text)

        post_001_card = main_area.find('div', id='post-1')
        self.assertIn(self.post_001.title, post_001_card.text)
        self.assertIn(self.post_001.category.name, post_001_card.text)
        
        # post_001 카드에 작성자명이 포함되어 있는지 확인
        self.assertIn(self.post_001.author.username.upper(), post_001_card.text)
        # post_001 카드에 hello 태그가 포함되어 있는지 확인
        self.assertIn(self.tag_hello.name, post_001_card.text)
        # post_001 카드에 hello 태그를 제외한 나머지 태그가 불포함되었는지 확인
        self.assertNotIn(self.tag_python.name, post_001_card.text)
        self.assertNotIn(self.tag_python_kor.name, post_001_card.text)

        post_002_card = main_area.find('div', id='post-2')
        self.assertIn(self.post_002.title, post_002_card.text)
        self.assertIn(self.post_002.category.name, post_002_card.text)

        # post_002 카드에 작성자명이 포함되어 있는지 확인
        self.assertIn(self.post_002.author.username.upper(), post_002_card.text)
        # post_002 카드에 태그가 불포함되었는지 확인
        self.assertNotIn(self.tag_hello.name, post_002_card.text)
        self.assertNotIn(self.tag_python.name, post_002_card.text)
        self.assertNotIn(self.tag_python_kor.name, post_002_card.text)

        post_003_card = main_area.find('div', id='post-3')
        self.assertIn('미분류', post_003_card.text)
        self.assertIn(self.post_003.title, post_003_card.text)

        # post_003 카드에 작성자명이 포함되어 있는지 확인
        self.assertIn(self.post_003.author.username.upper(), post_003_card.text)
        # post_003 카드에 hello 태그가 불포함되어 있는지 확인
        self.assertNotIn(self.tag_hello.name, post_003_card.text)
        # post_003 카드에 hello 태그를 제외한 나머지 태그가 포함되었는지 확인
        self.assertIn(self.tag_python.name, post_003_card.text)
        self.assertIn(self.tag_python_kor.name, post_003_card.text)

        self.assertIn(self.user_trump.username.upper(), main_area.text)
        self.assertIn(self.user_obama.username.upper(), main_area.text)

        # 포스트가 없는 경우
        Post.objects.all().delete()
        self.assertEqual(Post.objects.count(), 0)
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다', main_area.text)

    # 포스트 상세페이지 테스트
    def test_post_detail(self):
        # 1.1 포스트가 하나 있다.
        # 포스트 글은 이미 setUp 함수에 작성된 상태이다.

        # 1.2 그 포스트의 url은 '/blog/1/' 이다.
        self.assertEqual(self.post_001.get_absolute_url(), '/blog/1/')

        # 2. 첫 번째 포스트의 상세 페이지 테스트
        # 2.1 첫 번째 포스트의 url로 접근하면 정상적으로 작동한다(status code: 200)
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        # 2.2 포스트 목록 페이지와 똑같은 내비게이션 바가 있다.
        self.navbar_test(soup)

        # 2.2.1 포스트 우측 카테고리 카드가 있다.
        self.category_card_test(soup)

        # 2.3 첫 번째 포스트의 제목이 웹 브라우저 탭 타이틀에 들어 있다.
        self.assertIn(self.post_001.title, soup.title.text)

        # 2.4 첫 번째 포스트의 제목이 포스트 영역에 있다.
        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(self.post_001.title, post_area.text)
        self.assertIn(self.category_programming.name, post_area.text)

        # 2.5 첫 번째 포스트의 작성자(author)가 포스트 영역에 있다.(아직 구현할 수 없음)
        self.assertIn(self.user_trump.username.upper(), post_area.text)

        # 2.6 첫 번째 포스트의 내용(content)이 포스트 영역에 있다.
        self.assertIn(self.post_001.content, post_area.text)

        self.assertIn(self.tag_hello.name, post_area.text)
        self.assertNotIn(self.tag_python.name, post_area.text)
        self.assertNotIn(self.tag_python_kor.name, post_area.text)

        # comment area
        comments_area = soup.find('div', id='comment-area')
        comment_001_area = comments_area.find('div', id='comment-1')
        self.assertIn(self.comment_001.author.username, comment_001_area.text)
        self.assertIn(self.comment_001.content, comment_001_area.text)

    # 카테고리 페이지 테스트하기
    def test_category_page(self):
        # 'programming' 카테고리를 가지는 포스트 글들을 출력하는 페이지로 접속한다.
        # 접속 후 응답 내용들은 response 변수에 저장된다.
        # self.category_programming.get_absolute_url() 함수는 추후 구현해야한다.
        response = self.client.get(self.category_programming.get_absolute_url())

        # 응답 내용 중 status_code 값을 통해서 페이지가 정상적으로 동작하는지 확인한다.
        self.assertEqual(response.status_code, 200)

        # 응답 내용의 content 변수에 담긴 html 문서를 BeautifulSoup이 구문 분석하고
        # 분석한 결과를 soup 변수에 저장한다.
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 내비게이션 테스트 함수 호출하여 내비게이션 테스트 수행
        self.navbar_test(soup)
        
        # 카테고리 카드 테스트 함수를 호출하여 카테고리 카드 테스트 수행
        self.category_card_test(soup)

        # 카테고리 페이지 내에 'programming' 카테고리 뱃지가 포함되어 있는지 확인
        self.assertIn(self.category_programming.name, soup.h1.text)

        # 카테고리 페이지 내부의 div 태그 중 id가 main-area인 div 태그를 찾는다.
        # 찾은 div 태그 내용을 main_area 변수에 담는다.
        main_area = soup.find('div', id='main-area')

        # main_area 영역 내에 'programming' 카테고리 뱃지 포함 유무를 체크한다.
        self.assertIn(self.category_programming.name, main_area.text)

        # 현재 첫 번째 글이 가지고 있는 카테고리의 페이지 ('programming' 카테고리 페이지)에
        # 접속한 상태이므로 첫 번째 글의 제목은 main_area에 존재해야 하지만
        # 두 번째, 세 번째 글의 제목은 main_area에 존재하면 안된다.
        # (두 번째, 세 번째 글의 카테고리는 'programming' 카테고리가 아니므로)
        self.assertIn(self.post_001.title, main_area.text)
        self.assertNotIn(self.post_002.title, main_area.text)
        self.assertNotIn(self.post_003.title, main_area.text)

    # 태그 페이지 테스트
    def test_tag_page(self):
        # hello 태그 페이지로 접속하여 정상동작하는지 확인
        response = self.client.get(self.tag_hello.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        # hello 태그 페이지의 내비게이션바 테스트
        self.navbar_test(soup)
        
        # hello 태그 페이지의 카테고리 카드 테스트
        self.category_card_test(soup)

        # hello 태그 이름과 hello 태그 페이지의 타이틀이 일치하는지 확인
        self.assertIn(self.tag_hello.name, soup.h1.text)

        # hello 태그 페이지의 main-area를 찾는다.
        main_area = soup.find('div', id='main-area')

        # main-area 내부에는 hello 태그이름과 post_001 글의 타이틀만 존재해야 한다.
        # post_002글과 post_003글의 제목은 main-area에 포함되면 안된다.
        # (post_001 글만 hello 태그를 가지고 있기 때문)
        self.assertIn(self.tag_hello.name, main_area.text)
        self.assertIn(self.post_001.title, main_area.text)
        self.assertNotIn(self.post_002.title, main_area.text)
        self.assertNotIn(self.post_003.title, main_area.text)

    def test_create_post(self):
        # 로그인하지 않으면 status_code가 200이면 안 된다!
        response = self.client.get('/blog/create_post/')
        self.assertNotEqual(response.status_code, 200)

        # staff가 아닌 trump가 로그인을 한다.
        self.client.login(username='trump', password='somepassword')
        response = self.client.get('/blog/create_post/')
        self.assertNotEqual(response.status_code, 200)

        # staff인 obama로 로그인한다.
        self.client.login(username='obama', password='somepassword')

        # 1. (상민씨)
        response = self.client.get('/blog/create_post/')
        self.assertEqual(response.status_code, 200)

        # 2. (기백씨)
        soup = BeautifulSoup(response.content, 'html.parser')

        # 3. (남곤씨)
        self.assertEqual('Create Post - Blog', soup.title.text)

        # 4. (동빈씨)
        main_area = soup.find('div', id='main-area')
        self.assertIn('Create New Post', main_area.text)

        # 템플릿에서 id가 id_tags_str를 가지는 input 태그가 존재하는지 확인
        tag_str_input = main_area.find('input', id='id_tags_str')
        self.assertTrue(tag_str_input)

        # 5. POST 방식으로 포스트 글 내용을 작성하고
        # 글 작성 요청을 위한 주소를 기입한다.
        # 첫 번째 파라메터: 클라이언트로부터 요청받을 서버주소
        # 두 번째 파라메터: 서버로 전송할 필드명과 값을 딕셔너리 형태로 작성
        self.client.post(
            '/blog/create_post/',
            {
                'title': 'Post Form 만들기',
                'content': 'Post Form 페이지를 만듭시다.',
                'tags_str': 'new tag; 한글 태그, python'
            }
        )
        # 6. last() 함수는 포스트 글 중 제일 최근에 작성한
        # 포스트 글 하나를 가져온다.
        last_post = Post.objects.last()

        # 7. 제일 최근에 작성한 글의 제목과 작성자명을 비교한다.
        # 제일 최근에 작성한 글 제목은 5번 주석에 입력했던 title 이고,
        # 작성자명은 현재 로그인된 obama 이다.
        self.assertEqual(last_post.title, 'Post Form 만들기')
        self.assertEqual(last_post.author.username, 'obama')

        # 5번에서 작성했던 태그 3개가 정상적으로 입력 되었는지 확인
        # 수정한 태그의 개수 총 3개인지 확인 
        self.assertEqual(last_post.tags.count(), 3)
        
        # 입력한 태그 중 'new tag'와 '한글 태그'가 존재하는지 확인
        self.assertTrue(Tag.objects.get(name='new tag'))
        self.assertTrue(Tag.objects.get(name='한글 태그'))
        
        # 현재 데이터베이스에 저장된 태그의 총 개수가 5개인지 확인
        self.assertEqual(Tag.objects.count(), 5)

    # 포스트 수정 페이지 테스트
    def test_update_post(self):
        # setUp() 함수에서 작성한 세 번째 포스트 글을 수정하기 위해
        # 주소를 작성하고 작성한 주소를 update_post_url 변수에 담는다.
        update_post_url = f'/blog/update_post/{self.post_003.pk}/'

        # 로그인하지 않은 경우
        # 로그인하지 않은 경우는 포스트 수정페이지에 진입할 수 없다.
        response = self.client.get(update_post_url)
        self.assertNotEqual(response.status_code, 200)

        # 로그인은 했지만 작성자가 아닌 경우
        # 세 번째 글을 작성한 트럼프만 글을 수정할 수 있다.
        # 포스트 수정페이지는 특정 글의 작성자만 수정할 수 있는 권한을 가진다.
        self.assertNotEqual(self.post_003.author, self.user_trump)
        self.client.login(
            username=self.user_trump.username,
            password='somepassword'
        )
        response = self.client.get(update_post_url)

        # 서버에서 작성자를 비교하고 작성자가 다르다면 403 응답을
        # 클라이언트로 보내게 된다.
        self.assertEqual(response.status_code, 403)

        # 작성자(obama)가 접근하는 경우
        # 세 번째 글을 오바마가 작성했으므로 수정페이지에 접근이 가능하다.
        self.client.login(
            username=self.post_003.author.username,
            password='somepassword'
        )
        response = self.client.get(update_post_url)
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        # 포스트 수정페이지의 title은 'Edit Post - Blog' 이어야 한다.
        self.assertEqual('Edit Post - Blog', soup.title.text)

        # main-area 영역에는 'Edit Post'라는 제목이 보여야 한다.
        main_area = soup.find('div', id='main-area')
        self.assertIn('Edit Post', main_area.text)

        # 수정페이지에서 데이터베이스로부터 불러온 태그를 출력하는 input 태그를 찾아
        # input 태그 객체를 tag_str_input 변수에 담는다.
        tag_str_input = main_area.find('input', id='id_tags_str')

        # tag_str_input 변수가 존재하는지 확인 (변수값이 null이 아니면 True)
        self.assertTrue(tag_str_input)

        # 불러온 글의 태그인 '파이썬 공부'와 'python'이 정상적으로
        # 태그 input 박스에 불러와졌는지 확인한다.
        # input 태그의 value 속성은 현재 입력된 값을 나타낸다.
        # <input id='id_tags_str' value='파이썬 공부; python' type='text'>
        self.assertIn('파이썬 공부; python', tag_str_input.attrs['value'])

        # 글을 수정하기 위해 POST 방식으로 수정 내용을 서버로 전달한다.
        # POST update_post_url 에 대한 처리는 장고가 자동으로 처리해준다.
        # 두 번째 파라메터는 수정할 내용을 필드명과 수정내용 작성하여 딕셔너리
        # 형태로 만든다.
        # 세 번째 파라메터 follow=True는 글 수정 이후
        # 테스트 코드에서 우리가 페이지 이동하는 코드를 작성하지 않더라도
        # 수정페이지 이후 이동하는 페이지로 자동으로 이동하게 된다.
        response = self.client.post(
            update_post_url,
            {
                'title': '세 번째 포스트를 수정했습니다.',
                'content': '안녕 세계? 우리는 하나!',
                'category': self.category_music.pk,
                'tags_str': '파이썬 공부; 한글 태그, some tag'
            },
            follow=True
        )

        # 수정페이지 이후 이동된 페이지 내용을 다시 읽어드린 후
        # 해당 글의 제목과 내용이 수정됐는지를 포스트 상세페이지에서
        # 확인을 한다.
        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id='main-area')
        self.assertIn('세 번째 포스트를 수정했습니다.', main_area.text)
        self.assertIn('안녕 세계? 우리는 하나!', main_area.text)
        self.assertIn(self.category_music.name, main_area.text)

        # 수정이 끝난 후 포스트 상세 페이지에서 변경한 태그가 제대로 적용되었는지 확인
        self.assertIn('파이썬 공부', main_area.text)
        self.assertIn('한글 태그', main_area.text)
        self.assertIn('some tag', main_area.text)
        self.assertNotIn('python', main_area.text)

    # 댓글 작성 폼 테스트
    def test_comment_form(self):
        # Comment 테이블에 등록된 댓글의 전체 개수 확인하기
        # setUp() 함수에서 작성한 댓글 하나만 존재하므로 총 댓글 개수는 1개
        self.assertEqual(Comment.objects.count(), 1)
        
        # post_001 포스트 글에 추가된 댓글이 하나인지 테스트
        self.assertEqual(self.post_001.comment_set.count(), 1)

        # 로그인하지 않은 상태
        # 로그인하지 않은 상태에서 첫 번째 포스트 상세페이지에 접속이 가능해야 한다.
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        # 댓글 영역을 찾아서
        comment_area = soup.find('div', id='comment-area')

        # 댓글 영역에 [로그인해야 댓글을 남길 수 있다]는 안내문구가 표시되어야 한다.
        self.assertIn('Log in and leave a comment', comment_area.text)

        # 로그인 하지 않은 상태에서는 댓글 작성 form이 보이지 않아야 한다.
        self.assertFalse(comment_area.find('form', id='comment-form'))

        # 로그인한 상태
        # obama 사용자로 로그인 한다.
        self.client.login(username='obama', password='somepassword')
        # 로그인한 상태에서 첫 번째 포스트 글 상세페이지로 이동한다.
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        # 로그인한 상태이기 때문에 댓글 영역에 'Log in and leave a comment'
        # 메시지가 더이상 표시되지 않는다.
        comment_area = soup.find('div', id='comment-area')
        self.assertNotIn('Log in and leave a comment', comment_area.text)

        # 로그인한 상태이기 때문에 댓글을 작성할 수 있는 영역이 노출된다.
        # 작성한 댓글을 서버로 POST 요청을 보내기 위한 form 태그가 존재하는지 확인
        comment_form = comment_area.find('form', id='comment-form')
        # 댓글을 작성하는 영역인 textarea 태그가 존재하는지 확인
        self.assertTrue(comment_form.find('textarea', id='id_content'))

        # 최종적으로 작성한 댓글을 [포스트 상세페이지 주소 + new_comment/] 주소로
        # POST 방식으로 서버에 요청을 보낸다.
        # follow가 True이기 때문에 서버로부터 응답을 받으면 다시 상세페이지로
        # 접속을 하게 된다.
        response = self.client.post(
            self.post_001.get_absolute_url() + 'new_comment/',
            {
                'content': "오바마의 댓글입니다.",
                'my_score': 4
            },
            follow=True
        )

        self.assertEqual(response.status_code, 200)

        # 방금 위 코드에서 댓글 하나를 더 추가했으므로 전체 댓글의 수는 2개가 된다.
        self.assertEqual(Comment.objects.count(), 2)

        # 첫 번째 포스트 글에 댓글 하나를 더 추가했으므로
        # 첫 번째 포스트 글의 댓글 개수는 2개가 된다.
        self.assertEqual(self.post_001.comment_set.count(), 2)

        # Comment 테이블에서 제일 마지막에 존재하는 레코드를 가져온 것이니
        # 제일 최근에 작성한 댓글이고, 이 댓글 객체를 new_comment 변수에 담은 것이다.
        new_comment = Comment.objects.last()

        soup = BeautifulSoup(response.content, 'html.parser')

        # 최근 작성한 댓글의 객체를 이용해서 댓글을 작성한 포스트 글에 접근한 뒤
        # 실제 페이지에 출력된 Post의 제목과 title 태그의 text를 비교한다.
        # 이 테스트를 통과한다면 첫 번째 포스트 글의 댓글인 셈이다.
        self.assertIn(new_comment.post.title, soup.title.text)

        # 댓글 영역을 찾아서 댓글 작성자와 내용이 일치하는지 확인하여 정상등록 됐는지 확인
        comment_area = soup.find('div', id='comment-area')
        new_comment_div = comment_area.find('div', id=f'comment-{new_comment.pk}')
        self.assertIn('obama', new_comment_div.text)
        self.assertIn('오바마의 댓글입니다.', new_comment_div.text)

    def test_comment_update(self):

        comment_by_trump = Comment.objects.create(
            post=self.post_001,
            author=self.user_trump,
            content='트럼프의 댓글입니다.'
        )

        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        comment_area = soup.find('div', id='comment-area')
        self.assertFalse(comment_area.find('a', id='comment-1-update-btn'))
        self.assertFalse(comment_area.find('a', id='comment-2-update-btn'))

        # 로그인한 상태
        self.client.login(username='obama', password='somepassword')
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        comment_area = soup.find('div', id='comment-area')
        self.assertFalse(comment_area.find('a', id='comment-2-update-btn'))
        comment_001_update_btn = comment_area.find('a', id='comment-1-update-btn')
        self.assertIn('edit', comment_001_update_btn.text)
        self.assertEqual(comment_001_update_btn.attrs['href'], '/blog/update_comment/1/')

        self.assertIn('edit', comment_001_update_btn.text)
        self.assertEqual(comment_001_update_btn.attrs['href'],
                         '/blog/update_comment/1/')

        response = self.client.get('/blog/update_comment/1/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.assertEqual('Edit Comment - Blog', soup.title.text)
        update_comment_form = soup.find('form', id='comment-form')
        content_textarea = update_comment_form.find('textarea', id='id_content')
        self.assertIn(self.comment_001.content, content_textarea.text)

        response = self.client.post(
            f'/blog/update_comment/{self.comment_001.pk}/',
            {
                'content': "오바마의 댓글을 수정합니다.",
                'my_score': 5
            },
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        comment_001_div = soup.find('div', id='comment-1')
        self.assertIn('오바마의 댓글을 수정합니다.', comment_001_div.text)
        self.assertIn('Updated: ', comment_001_div.text)

    def test_delete_comment(self):
        comment_by_trump = Comment.objects.create(
            post=self.post_001,
            author=self.user_trump,
            content='트럼프의 댓글입니다.'
        )

        self.assertEqual(Comment.objects.count(), 2)
        self.assertEqual(self.post_001.comment_set.count(), 2)

        # 로그인하지 않은 상태
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        comment_area = soup.find('div', id='comment-area')
        self.assertFalse(comment_area.find('a', id='comment-1-delete-btn'))
        self.assertFalse(comment_area.find('a', id='comment-2-delete-btn'))

        # trump로 로그인한 상태
        self.client.login(username='trump', password='somepassword')
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        comment_area = soup.find('div', id='comment-area')
        self.assertFalse(comment_area.find('a', id='comment-1-delete-btn'))
        comment_002_delete_modal_btn = comment_area.find(
            'a', id='comment-2-delete-modal-btn'
        )
        self.assertIn('delete', comment_002_delete_modal_btn.text)
        self.assertEqual(
            comment_002_delete_modal_btn.attrs['data-target'],
            '#deleteCommentModal-2'
        )

        delete_comment_modal_002 = soup.find('div', id='deleteCommentModal-2')
        self.assertIn('Are You Sure?', delete_comment_modal_002.text)
        really_delete_btn_002 = delete_comment_modal_002.find('a')
        self.assertIn('Delete', really_delete_btn_002.text)
        self.assertEqual(
            really_delete_btn_002.attrs['href'],
            '/blog/delete_comment/2/'
        )

        response = self.client.get('/blog/delete_comment/2/', follow=True)
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertIn(self.post_001.title, soup.title.text)
        comment_area = soup.find('div', id='comment-area')
        self.assertNotIn('트럼프의 댓글입니다.', comment_area.text)

        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(self.post_001.comment_set.count(), 1)

    def test_search(self):
        post_about_python = Post.objects.create(
            title='파이썬에 대한 포스트입니다.',
            content='Hello World. We are the world.',
            author=self.user_trump
        )

        response = self.client.get('/blog/search/파이썬/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        main_area = soup.find('div', id='main-area')

        self.assertIn('Search: 파이썬 (2)', main_area.text)
        self.assertNotIn(self.post_001.title, main_area.text)
        self.assertNotIn(self.post_002.title, main_area.text)
        self.assertIn(self.post_003.title, main_area.text)
        self.assertIn(post_about_python.title, main_area.text)


