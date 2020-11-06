from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.hashers import make_password, check_password  # 這一行用來加密密碼的

# Create your views here.
def login(request):
    title = '成員登入'
    if request.method == 'POST':
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        remember_me = request.POST.get('remember_me', False)
        print(remember_me, type(remember_me))
        if remember_me == 'yes':
            request.session.set_expiry(None)
            # 如果value等于0，那么session将在web浏览器关闭后就直接过期。
            # 如果value等于None，那么session将用settings.py中设置的全局过期字段SESSION_COOKIE_AGE，这个字段默认是14天，也就是2个礼拜。 
        else:
            print('no')
            request.session.set_expiry(0)
            # 不留存cookies
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)  # 將用戶登入
            return redirect('index')
        else:
            user_not_match = True
        return render(request, 'account/login.html', dict())
    else:
        return render(request, 'account/login.html', dict())

def logout(request):
    auth.logout(request)
    return redirect('index')
