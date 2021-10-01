class Math():
    # *args: 튜플을 함수에서 받을 수 있는 파라메터
    # 튜플: (1, 2, 1, 2, 3)
    # **kwargs: 딕셔너리를 함수에서 받을 수 있는 파라메터
    # 딕셔너리: {
    #    "abc": "def",
    #    "food": "apple",
    #    "car": "hyundai"
    # }
    def add(self, *args, **kwargs):
        result = 0
        for a in args:
            result += a

        result = f"{kwargs['abc']} {result}"

        return result

    def sub(self, *args, **kwargs):
        result = 0
        for key in kwargs.keys():
            print(kwargs[key])
            if (key == 'abc'):
                for a in kwargs['abc']:
                    print(a)

    def add1(self, a, b, c):
        result = a + b + c
        return result


math = Math()
result = math.add(1, 2, 1, 2, 3, abc='def', food='apple', car='hyundai')
print(result)
math.sub(abc=['def', 'ghi'], food='apple', car='hyundai')
