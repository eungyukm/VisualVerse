class TopMenuMiddleware:
    def __init__(self, next_layer=None):
        self.get_response = next_layer

    # 장고에서 미들웨어를 동작시킬 때 호출하는 함수
    def __call__(self, request):
        response = self.process_request(request)

        if response is None:
            response = self.get_response(request)

        response = self.precess_response(request, response)
        return response

    # 요청정보 처리를 하기위해 호출하는 함수
    def process_request(self, request):
        menu_list = ['home', 'post', 'story', 'login', 'register']
        request.menu_list = menu_list

    # 응답정보를 처리하기 위해 호출하는 함수
    def precess_response(self, request, response):
        return response