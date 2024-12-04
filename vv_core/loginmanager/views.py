from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.template import loader
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

from .models import CustomUser

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@csrf_exempt
def login_result(request):
    email = request.POST['email']
    password = request.POST['password']

    try:
        user_model = CustomUser.objects.get(email=email)

        if user_model.check_password(password):
            login(request, user_model)
            # 로그인에 성공할 경우 셰션에 로그인 여부값을 저장합니다.
            request.session['login_chk'] = True
            request.session['login_user_id'] = user_model.id

            message = '''
            <script>
                alert('로그인 되었습니다.');
                location.href = '/';
            </script>
            '''
        else:
            message = '''
            <script>
                alert('비밀번호가 일치하지 않습니다.');
                location.href = '/auth/login?login_chk=1';
            </script>
            '''
    except:
        message = '''
        <script>
            alert('존재하지 않는 이메일입니다.');
            location.href = '/auth/login?login_chk=1';
        </script>
        '''
    return HttpResponse(message)



def logout_result(request):
    del request.session['login_chk']
    del request.session['login_user_id']

    message = f'''
    <script>
        alert('로그아웃 되었습니다.');
        location.href = '/';
    </script>
    '''
    return HttpResponse(message)

def signup_view(request):
    login_chk = request.GET.get('login_chk')
    print(login_chk)

    render_data = { 'login_chk': login_chk }
    template = loader.get_template('signup.html')
    return HttpResponse(template.render(render_data, request))

@csrf_exempt
def signup_result(request):
    username = request.POST['username']
    password1 = request.POST['password1']
    password2 = request.POST['password2']
    email = request.POST['email']

    # 비밀번호 확인
    if password1 != password2:
        return HttpResponse('''
            <script>
                alert('비밀번호가 일치하지 않습니다.');
                history.back();
            </script>
        ''')

    # 이메일 중복 확인
    if CustomUser.objects.filter(email=email).exists():
        return HttpResponse('''
            <script>
                alert('이미 가입된 이메일입니다.');
                history.back();
            </script>
        ''')

    user = CustomUser.objects.create_user(username=username, password=password1, email=email)
    user.save()

    confirm = '''
    <script>
        alert('회원가입이 완료되었습니다.');
        location.href = '/';
    </script>
    '''

    return HttpResponse(confirm)


def modify_profile_view(request):
    try:
        # 세션에서 로그인된 사용자 ID 가져오기
        login_user_id = request.session.get('login_user_id')

        if not login_user_id:
            # 세션에 로그인 사용자 ID가 없는 경우
            return HttpResponse('''
                <script>
                    alert('로그인 정보가 없습니다. 다시 로그인해 주세요.');
                    location.href = '/auth/login';
                </script>
            ''')

        # 사용자 데이터 가져오기
        login_user_model = CustomUser.objects.get(id=login_user_id)

    except ObjectDoesNotExist:
        # 사용자 정보가 없는 경우 처리
        return HttpResponse('''
            <script>
                alert('사용자 정보를 찾을 수 없습니다. 다시 로그인해 주세요.');
                location.href = '/auth/login';
            </script>
        ''')

    # 사용자 데이터를 템플릿에 전달
    render_data = {
        'login_user_data': login_user_model
    }
    template = loader.get_template('modify_profile.html')
    return HttpResponse(template.render(render_data, request))

@csrf_exempt
def modify_profile_result(request):
    password = request.POST['password']
    login_user_id = request.session.get('login_user_id')

    try:
        login_user_model = CustomUser.objects.get(id=login_user_id)
        login_user_model.set_password(password)
        login_user_model.save()

        message = '''
        <script>
            alert('비밀번호가 변경되었습니다.');
            location.href = '/';
        </script>
        '''
    except ObjectDoesNotExist:
        message = '''
        <script>
            alert('사용자 정보를 찾을 수 없습니다. 다시 로그인해 주세요.');
            location.href = '/auth/login';
        </script>
        '''
    return HttpResponse(message)