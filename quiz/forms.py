from django import forms
from .models import Question


class AddQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['country', 'country_genitive', 'capital']
        labels = {
            'country': 'Страна (именительный падеж)',
            'country_genitive': 'Страна (родительный падеж)',
            'capital': 'Столица',
        }
        widgets = {
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'country_genitive': forms.TextInput(attrs={'class': 'form-control'}),
            'capital': forms.TextInput(attrs={'class': 'form-control'}),
        }

    
    def clean_country(self):
        country = self.cleaned_data.get('country')
        if Question.objects.filter(country__iexact=country).exists():
            raise forms.ValidationError(f'Страна "{country}" уже есть в базе!')
        return country


class QuizAnswerForm(forms.Form):
    answer = forms.CharField(
        label='Ваш ответ',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите столицу',
            'autofocus': 'autofocus'
        }),
        error_messages={
            'required': 'Пожалуйста, введите ответ!'
        }
    )