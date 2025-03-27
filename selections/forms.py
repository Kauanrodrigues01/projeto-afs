from django import forms
from .models import Selection, Teacher
import re


class SelectionForm(forms.ModelForm):
    class Meta:
        model = Selection
        fields = ['teacher', 'email', 'student_name', 'phone_number', 'tier']
        labels = {
            'email': 'Seu Email Institucional (aluno.ce.gov.br)',
            'student_name': 'Seu Nome Completo',
            'tier': 'Sua Turma',
            'teacher': 'Professor Desejado',
            'phone_number': 'Seu Número de Telefone'
        }
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu email'}),
            'student_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu nome'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control student-phone', 'placeholder': 'Digite seu número de telefone'}),
            'tier': forms.Select(attrs={'class': 'form-select'}),
            'teacher': forms.Select(attrs={'class': 'form-select'})
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@aluno.ce.gov.br'):
            raise forms.ValidationError('O email deve terminar com @aluno.ce.gov.br.')
        if Selection.objects.filter(email=email).exists():
            raise forms.ValidationError('Já existe um registro com esse email.')
        return email
    
    def clean_student_name(self):
        student_name = self.cleaned_data.get('student_name')
        if len(student_name) < 8:
            raise forms.ValidationError('O nome deve ter pelo menos 8 caracteres.')
        return student_name
    
    def clean_tier(self):
        tier = self.cleaned_data.get('tier')
        if tier not in dict(Selection.TIER_CHOICES):
            raise forms.ValidationError('Turma inválida.')
        return tier
    
    def clean_teacher(self):
        teacher = self.cleaned_data.get('teacher')
        if not teacher:
            raise forms.ValidationError('Selecione um professor.')
        if Selection.objects.filter(teacher=teacher).count() >= 8:
            raise forms.ValidationError('Este professor já foi escolhido pelo limite máximo de alunos. (8 alunos)')
        return teacher

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        phone_number = phone_number.replace('(', '').replace(')', '').replace('-', '').replace(' ', '')

        # Verifica se o número está presente
        if not phone_number:
            raise forms.ValidationError('O número de telefone é obrigatório.')

        # Expressão regular para validar os formatos 85xxxxxxxx e 85xxxxxxxxx
        pattern = r'^85\d{8,9}$'

        if not re.fullmatch(pattern, phone_number):
            raise forms.ValidationError('O número de telefone deve estar no formato 85xxxxxxxx ou 85xxxxxxxxx.')
        return phone_number
