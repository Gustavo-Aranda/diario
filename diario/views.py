from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Pessoa, Diario, Tags
from datetime import datetime, timedelta
from django.contrib import messages
from django.utils.timezone import now

# Create your views here.
def home(request):
    textos = Diario.objects.order_by('-create_at')[:3]
    pessoas = Pessoa.objects.all()
    nomes = [pessoa.nome for pessoa in pessoas]
    qtds = []
    
    for pessoa in pessoas:
        qtd = Diario.objects.filter(pessoas = pessoa).count()
        qtds.append(qtd)
        
    return render(request, 'home.html', {'textos': textos, 'nomes': nomes, 'qtds': qtds})

def escrever(request):
    if request.method == 'GET':
        pessoas = Pessoa.objects.all()
        tags_created = Tags.objects.all()
        return render(request, 'escrever.html', {'pessoas': pessoas, 'tags_created': tags_created})
    
    elif request.method == 'POST':
        titulo = request.POST.get('titulo')
        tags = request.POST.getlist('tags')
        pessoas = request.POST.getlist('pessoas')
        texto = request.POST.get('texto')
        
        if len(titulo.strip()) == 0 or len(texto.strip()) == 0:
            messages.add_message(request, messages.ERROR, 'ERRO! Não é possivel enviar um diário sem título ou conteúdo.')
            
            return redirect('escrever')
        
        diario = Diario(
            titulo = titulo,
            texto = texto
        )
        diario.set_tags(tags)
        diario.save()
        
        for i in pessoas:
            pessoa = Pessoa.objects.get(id=i)
            diario.pessoas.add(pessoa)
            
        diario.save()

        messages.add_message(request, messages.SUCCESS, 'Muito bem! Seu diário foi registrado!')
        return redirect('escrever')

def cadastrar_pessoa(request):
    if request.method == 'GET':
        return render(request, 'pessoa.html')
    
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        foto = request.FILES.get('foto')
        
        pessoa = Pessoa(
            nome = nome, 
            foto = foto
        )
        if len(nome.strip()) > 0 and foto:
            pessoa.save()
            messages.add_message(request, messages.SUCCESS, f'A pessoa {nome} foi registrada!')
        else:
            messages.add_message(request, messages.ERROR, 'ERRO! Não é possivel criar uma pessoa sem nome ou sem foto!')
            
        return redirect('cadastrar_pessoa')
    
def dia(request):
    data_atual = now()
    data = request.GET.get('data')
    data_formatada = datetime.strptime(data, '%Y-%m-%d')
    diarios = Diario.objects.filter(create_at__gte=data_formatada).filter(create_at__lte=data_formatada + timedelta(days = 1))
    deletado = False
    
    return render(request, 'dia.html', {'diarios':diarios, 'total': diarios.count(), 'data': data, 'data_atual': data_atual, 'deletado': deletado})

def excluir_dia(request):
    dia = datetime.strptime(request.GET.get('data'), '%Y-%m-%d')
    diarios = Diario.objects.filter(create_at__gte=dia).filter(create_at__lte=dia + timedelta(days = 1))
    diarios.delete()
    deletado = True
    return render(request, 'dia.html', {'deletado': deletado})

def criar_tags(request):
    if request.method == 'GET':
        return render(request, 'tags.html')

    elif request.method == 'POST':
        tag = request.POST.get('tag', '').strip()

        if Tags.objects.filter(tag=tag).exists():
            messages.add_message(request, messages.ERROR, f'ERRO! A tag "{tag}" já foi registrada!')
        elif tag:
            Tags.objects.create(tag=tag)
            messages.add_message(request, messages.SUCCESS, f'A tag "{tag}" foi registrada!')
        else:
            messages.add_message(request, messages.ERROR, 'ERRO! Não é possível criar uma tag sem nome!')

        return redirect('criar_tags')