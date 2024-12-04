from django.http import HttpResponse

class LoginCheckMiddleware:
    def __init__(self, next_layer=None):
        self.get_response = next_layer

    # 장고에서 미들웨어를 동작시킬 때 호출하는 함수
    def __call__(self, request):
        response = self.process_request(request)

        if response is None:
            response = self.get_response(request)

        response = self.process_response(request, response)
        return response

    def process_request(self, request):
        pass

    # 응답정보를 처리하기 위해 호출하는 함수
    def process_response(self, request, response):
        except_list = [
            'index',
            'login',
            'logout',
            'post_main',
            'register',
            'admin',
            'static',
            'media',
        ]

        # 현재 요청이 로그인이 필요한 페이지인지 확인
        now_name = request.resolver_match.url_name
        print(now_name)

        # 제외 목록에 포함되어 있는 경우
        if now_name in except_list:
            return response
        # 제외 목록에 포함되어 있지 않는 경우
        else :
            # 로그인을 했는지 체크
            if request.session.get('login_chk') == True:
                return response
            else :
                message = '''
                        <script>
                            alert('잘못된 접근 입니다.')
                            location.href = '/'
                        </script>
                        '''
                return HttpResponse(message)