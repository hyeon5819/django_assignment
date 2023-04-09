#view
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import SignupForm


# 회원 가입
def signup(request):
    if request.method == 'POST': # POST요청시 SignupForm 유효성검사
        form = SignupForm(request.POST)
        if form.is_valid(): # 유효성검사를 통과하면 데이터베이스에 저장 후 로그인 화면 띄우기
            user = form.save()
            return redirect('/login')
        else: # 유효성검사 통과하지 못하면 회원가입 화면을 다시 띄워주기
            form = SignupForm()
            return render(request, 'accounts/signup.html', {'form': form})
    else: # 회원가입 첫 화면
        form = SignupForm()
        return render(request, 'accounts/signup.html', {'form': form})


# 로그인
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # 로그인 후 홈 화면으로 이동
        else:
            # 로그인 실패
            return render(request, 'accounts/login.html')

    else:
        # GET 방식으로 요청시 로그인 폼 보여줌
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return render(request, 'accounts/login.html')


# 로그아웃
@login_required
def user_logout(request):
    logout(request)
    return redirect('/login') # 로그아웃 후 로그인 화면으로 이동