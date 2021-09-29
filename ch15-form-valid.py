# 장고에 작성되어 있던 CreateView 클래스를 가상코드로 작성
class CreateView():
    model = ""
    fields = ""

    def form_valid(self, form):
        # 필수 값 체크
        if form['title'] and form['content'] and form['author']:
            print('title: ' + form['title'] + ' / ' + form['content'] + ' / ' + form['author']['username'])
        else:
            print('필수 입력 값을 입력하지 않았습니다.')

# 우리가 작성한 PostCreate 클래스
class PostCreate(CreateView):
    model = 'Post 모델'
    fields = ['title', 'hook_text', 'content', 'head_image',
              'file_upload', 'category']

    def form_valid(self, form):
        current_user = {
            'username': 'trump',
            'is_authenticated': True
        }

        if current_user['is_authenticated']:
            form['author'] = current_user
            return super(PostCreate, self).form_valid(form)
        else:
            return print('로그인 되지 않았습니다. [포스트 목록 페이지로 이동]')

def main():
    # 클라이언트로부터 전달받은 form 정보
    form = {
        'title': 'Post Form 만들기',
        'content': 'Post Form 페이지를 만듭시다.'
    }

    # 장고 내부 동작을 가상코드로 작성
    result = PostCreate()
    result.form_valid(form)

# 예제코드 시작
main()



