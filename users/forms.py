from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True)
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email


class CustomUserChangeForm(UserChangeForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES)
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'role', 'bio', 'profile_picture')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
