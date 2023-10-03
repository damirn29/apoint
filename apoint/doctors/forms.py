from django import forms

class DoctorАppoint(forms.Form):
    GENDER_CHOICES = [
        ('M', 'Муж'),
        ('F', 'Жен'),
    ]

    full_name = forms.CharField(max_length=100, label="Имя и фамилия")
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Дата рождения')
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect, label="Пол")
    contact_number = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'type': 'tel'}), label='Номер телефона')
    address = forms.CharField(widget=forms.Textarea, label='Адрес проживания')
    email = forms.EmailField(label='Почта')