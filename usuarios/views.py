from django.shortcuts import render,redirect

from django.contrib.auth.models import User

from django.contrib import auth

from django.contrib import messages

from usuarios.forms import LoginForms

from usuarios.forms import CadastroForms

def login(request):
    form = LoginForms()
    if request.method == 'POST':
        form = LoginForms(request.POST)
        if form.is_valid():
            nome= form["nome_login"].value()
            senha= form["senha"].value()

            user = auth.authenticate(
                request,
                username=nome,
                password=senha
            )

            if user is not None:
                auth.login(request, user)
                messages.success(request, f'{nome} logado com sucesso!')
                return redirect('index')
            else:
                messages.error(request, 'Erro ao efetuar login!')
                return redirect('login')
            
    return render(request, 'usuarios/login.html', {'form': form})

def cadastro(request):
    form= CadastroForms()
    if request.method == 'POST':
        form = CadastroForms(request.POST)
        
        if form.is_valid():
            if form["senha_1"].value() != form["senha_2"].value():
                messages.error(request, 'Senhas não são iguais!')
                return redirect('cadastro')
            
            nome= form["nome_cadastro"].value()
            email= form["email"].value()
            senha= form["senha_1"].value()

            if User.objects.filter(username=nome).exists():
                messages.error(request, 'Usuário já existente!')
                return redirect('cadastro')

            user = User.objects.create_user(
                username=nome,
                email=email,
                password=senha
            )
            user.save()
            messages.success(request, 'Usuário criado com sucesso!')
            return redirect('login')

    return render(request, 'usuarios/cadastro.html', {'form': form})

def logout(request):
    auth.logout(request)
    messages.success(request, 'Logout efetuado com sucesso!')
    return redirect('login')
