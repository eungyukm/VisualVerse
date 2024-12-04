from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.template import loader
from django.http import HttpResponse
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

def logout_view(request):
    logout(request)
    return redirect('login')

def signup_view(request):
    login_chk = request.GET.get('login_chk')
    print(login_chk)

    render_data = { 'login_chk': login_chk }
    template = loader.get_template('signup.html')
    return HttpResponse(template.render(render_data, request))

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