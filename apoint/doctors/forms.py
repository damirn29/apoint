from django import forms

class DoctorАppoint(forms.Form):
    GENDER_CHOICES = [
        ('M', 'male'),
        ('F', 'female'),
    ]

    full_name = forms.CharField(max_length=100,
                                label="First name last name",
                                required=True,
                                error_messages={
                                    'requred': "The field is required"
                                })
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),
                                label='Date of birth',
                                required=True,
                                error_messages={
                                    'requred': "The field is required"
                                })
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect, label="gender")
    contact_number = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'type': 'tel'}),
                                     label='Phone number',
                                     required=True,
                                     error_messages={
                                    'requred': "The field is required"
                                    })
    address = forms.CharField(widget=forms.Textarea, label='Address')
    email = forms.EmailField(label='Email')