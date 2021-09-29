class Food:
    taste = '(값이 없음)'
    quantity = '(값이 없음)'
    name = '(값이 없음)'

    def introduce(self):
        print('이름=' + self.name + ', ' + '맛=' + self.taste + '양=' + self.quantity)

class Origin(Food):
    origin_name = '한국'
    address = '부산 효성학원'

    def introduce(self):
        print(f'원산지명: {self.origin_name}, 원산지 주소: {self.address}')
        super(Origin, self).introduce()

class Apple(Origin, Food):
    taste = '사과맛'
    quantity = '3개'
    name = '사과'

    def introduce(self):
        print(f'사과: {self.name}, {self.quantity}, {self.taste}')
        super(Apple, self).introduce()

food = Apple()
food.introduce()