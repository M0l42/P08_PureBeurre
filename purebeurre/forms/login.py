from django import forms


class SignUpForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    first_name = forms.CharField(label='First Name', max_length=100)
    last_name = forms.CharField(label='Last Name', max_length=100)
    email = forms.EmailField()
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=32, widget=forms.PasswordInput)


class LogInForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)