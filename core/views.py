from django.shortcuts import render, redirect
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime, timedelta
from django.http.response import Http404 

# Create your views here.

def handler404(request, exception):
    return render(request, '404.html')

def login_user(request):
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('/')

def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
        else:
            messages.error(request, 'Usuário e/ou senha inválidos')
    return redirect('/')    

@login_required(login_url='/login/')
def lista_eventos(request):
    usuario = request.user
    data_atual = datetime.now() - timedelta(hours=1)
    eventos = Evento.objects.filter(usuario=usuario,
                                    data_evento__gt=data_atual)
    dados = {'eventos':eventos}
    return render(request, 'agenda.html', dados)

@login_required(login_url='/login/')
def evento(request):   
    id_evento = request.GET.get('id') 
    dados = {}   
    if id_evento:
        try:        
            dados['evento'] = Evento.objects.get(id=id_evento)
        except Evento.DoesNotExist:
            raise Http404
    return render(request, 'evento.html', dados)

@login_required(login_url='/login/')
def evento_submit(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        data_evento = datetime.strptime(request.POST.get('data_evento'), '%d/%m/%Y %H:%M')
        descricao = request.POST.get('descricao')
        local = request.POST.get('local')
        usuario = request.user        
        id_evento = request.POST.get('id')
        if id_evento:
            evento = Evento.objects.get(id=id_evento)
            if usuario == evento.usuario:
                Evento.objects.filter(id=id_evento).update(
                    titulo=titulo,
                    data_evento=data_evento,
                    descricao=descricao,
                    local=local
                )
        else:    
            Evento.objects.create(
                titulo=titulo,
                data_evento=data_evento,
                descricao=descricao,
                local=local,
                usuario=usuario
            )
    return redirect('/')

@login_required(login_url='/login/')
def delete_evento(request, id_evento):
    usuario = request.user
    try:
        evento = Evento.objects.get(id=id_evento)
    except Evento.DoesNotExist:
        raise Http404
    if usuario == evento.usuario:
        evento.delete()
    else:
        raise Http404
    return redirect('/')

@login_required(login_url='/login/')
def historico_eventos(request):
    usuario = request.user
    data_atual = datetime.now()
    eventos = Evento.objects.filter(usuario=usuario,
                                    data_evento__lt=data_atual)
    dados = {'eventos':eventos}
    return render(request, 'historico.html', dados)