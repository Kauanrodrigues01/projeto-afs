from django.shortcuts import render, redirect
from django.http import JsonResponse
from selections.forms import SelectionForm
from .models import Teacher
from django.db.models import Count, Case, When, Value, BooleanField

def home(request):
    """Exibe a página inicial com o formulário e a lista de professores."""
    if request.method == "POST":
        form = SelectionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("teachers:success_page")  # Redireciona para uma página de sucesso após o envio
    else:
        form = SelectionForm()

    teachers = Teacher.objects.annotate(
        num_selections=Count('selections'),
        is_available=Case(
            When(num_selections__gte=9, then=Value(False)),  # Se tiver 9 ou mais seleções, não está disponível
            default=Value(True),  # Caso contrário, está disponível
            output_field=BooleanField()
        )
    )
    return render(request, 'teachers/pages/home.html', {'teachers': teachers, 'form': form})


def success_page(request):
    return render(request, 'teachers/pages/success_page.html')

def get_teacher_data(request, teacher_id):
    """Retorna os dados do professor para popular a imagem via AJAX."""
    try:
        teacher = Teacher.objects.get(id=teacher_id)
        photo_url = teacher.photo.url if teacher.photo else "/static/default-avatar.png"  # Adicionada verificação para evitar erro se a foto não existir
        return JsonResponse({
            'name': teacher.name,
            'photo_url': photo_url
        })
    except Teacher.DoesNotExist:
        return JsonResponse({'error': 'Professor não encontrado'}, status=404)
    
def get_teachers_data(request):
    teachers = Teacher.objects.annotate(
        num_selections=Count('selections'),
        is_available=Case(
            When(num_selections__gte=8, then=Value(False)),  # Indisponível se tiver 9 ou mais seleções
            default=Value(True),
            output_field=BooleanField()
        )
    ).values("id", "name", "is_available")  # Pegando apenas os campos necessários

    return JsonResponse(list(teachers), safe=False)  # Convertendo a QuerySet em uma lista para serialização

