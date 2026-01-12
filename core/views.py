
# core/views.py (ATUALIZAÇÃO)
import qrcode
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q # <--- Importe o Q para buscas complexas
from .forms import LoginForm, AnimalForm
from .models import Animal
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from io import BytesIO

# VIEW DE HOME (Protegida para admins logados)
@login_required 
def home_view(request):
    animais = Animal.objects.all()
    query = request.GET.get('q') # Pega o valor do campo 'q' do formulário de busca

    if query:
        # Filtra por nome OU por espécie (buscas case-insensitive)
        animais = animais.filter(
            Q(nome__icontains=query) | Q(especie__icontains=query)
        )

    # Ordena por nome para melhor visualização
    animais = animais.order_by('nome') 
    
    context = {
        'animais': animais,
        'query': query,
    }
    return render(request, 'core/home.html', context)

# ... (Mantenha as outras views: login_view, logout_view, consulta_publica_view)
# ...

# VIEW DE LOGIN
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home') # Se já estiver logado, redireciona para a home

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Tenta autenticar o usuário
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user) # Faz o login
                return redirect('home') # Redireciona para o painel principal
            else:
                # Caso a autenticação falhe
                form.add_error(None, "Usuário ou senha inválidos.")
    else:
        form = LoginForm()

    return render(request, 'core/login.html', {'form': form})

# VIEW DE LOGOUT
def logout_view(request):
    logout(request)
    return redirect('login') # Redireciona para a página de login após o logout

# VIEW DE CONSULTA PÚBLICA (Qualquer um pode acessar)
def consulta_publica_view(request, tag_id):
    try:
        animal = Animal.objects.get(id_tag_nfc=tag_id)
        return render(request, 'core/consulta_publica.html', {'animal': animal})
    except Animal.DoesNotExist:
        return HttpResponse("Animal não encontrado.", status=404)

@login_required
def cadastro_animal_view(request):
    if request.method == 'POST':
        form = AnimalForm(request.POST, request.FILES)
        if form.is_valid():
            animal = form.save(commit=False)
            
            # ATRIBUIÇÕES AUTOMÁTICAS:
            animal.admin_responsavel = request.user
            
            # Cria um ID de TAG Simples e verifica o último ID existente
            # O último animal pode ter sido deletado, então usamos .order_by('-id').first() para segurança.
            ultimo_animal = Animal.objects.order_by('-id').first()
            ultimo_id = ultimo_animal.id if ultimo_animal else 0
            
            animal.id_tag_nfc = f"BIO-{ultimo_id + 1}"
            
            animal.save()
            return redirect('home') # <--- RETORNO 1: Em caso de POST válido
    else:
        form = AnimalForm()
        
    # <--- ESTE É O RETORNO CRÍTICO! É executado para:
    # 1. Requisições GET (exibir o formulário vazio).
    # 2. Requisições POST inválidas (reexibir o formulário com erros).
    return render(request, 'core/cadastro_animal.html', {'form': form})
@login_required # Apenas admins logados devem usar o scanner
def scanner_view(request):
    return render(request, 'core/scanner.html')        
    return render(request, 'core/cadastro_animal.html', {'form': form})

def cadastro_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Cria o usuário como "comum" por padrão
            messages.success(request, "Conta criada com sucesso! Faça login.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'core/registration.html', {'form': form})

@login_required
def excluir_animal(request, id_tag_nfc):
    if request.method == 'POST':
        animal = get_object_or_404(Animal, id_tag_nfc=id_tag_nfc)
        nome_animal = animal.nome
        animal.delete()
        messages.error(request, f"O registro de {nome_animal} foi removido.")
        return redirect('home') # Redireciona para a home após excluir
    return redirect('home')
@login_required
def editar_animal(request, id_tag_nfc):
    # Busca o animal existente pelo ID da Tag
    animal = get_object_or_404(Animal, id_tag_nfc=id_tag_nfc)
    
    if request.method == 'POST':
        # preenche o form com os dados novos + a foto antiga (request.FILES)
        form = AnimalForm(request.POST, request.FILES, instance=animal)
        if form.is_valid():
            form.save()
            messages.success(request, f"Dados de {animal.nome} atualizados!")
            return redirect('consulta_publica', tag_id=animal.id_tag_nfc)
    else:
        # Carrega o formulário com os dados atuais do animal
        form = AnimalForm(instance=animal)
    
    # Reutiliza o template de cadastro, mas passa uma variável 'editando'
    return render(request, 'core/cadastro_animal.html', {
        'form': form,
        'animal': animal,
        'editando': True
    })

def gerar_qr_code(request, tag_id):
    # Constrói a URL completa que o celular deve abrir
    # O ideal é que seja o link do seu site (ou do Ngrok no momento)
    base_url = request.build_absolute_uri(f'/consulta/{tag_id}/')
    
    # Configura o QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(base_url)
    qr.make(fit=True)

    # Cria a imagem
    img = qr.make_image(fill_color="#006400", back_color="white") # Verde BioTag
    
    # Salva em memória para enviar ao navegador
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    
    return HttpResponse(buffer.getvalue(), content_type="image/png")