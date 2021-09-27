from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.test import TestCase, Client

from blog.models import Post, Category, Tag


class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_trump =\
            User.objects.create_user(username='trump', password='somepassword')
        self.user_obama =\
            User.objects.create_user(username='obama', password='somepassword')

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