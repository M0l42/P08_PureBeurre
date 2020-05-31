from django import forms


class EditAccountForm(forms.Form):
    """
    Form to collect all the infos we need to register a new user
    """
    image = forms.ImageField(required=False)
    email = forms.EmailField(required=False)
