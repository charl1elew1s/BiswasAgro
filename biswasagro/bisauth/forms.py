from django import forms
from django.forms import ModelForm, Form
from .models import TblUsers, TblRoles
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import check_password


class TblUsersForm(ModelForm):
    class Meta:
        model = TblUsers
        fields = ['name', 'username', 'email', 'password', 'mobile', 'roleid', 'is_active',
                  'created_at', 'updated_at',]

        labels = {
           'name': 'Name',
           'username': 'Username',
           'email': 'Email',
           'password': 'Password',
           'mobile': 'Mobile Number',
           'roleid': 'Role ID',
           'is_active': 'Is Active',
           'created_at': 'Created At',
           'updated_at': 'Updated At',
        }


class TblRolesForm(ModelForm):
    class Meta:
        model = TblRoles
        fields = ['role']

        labels = {
            'role': 'Role'
        }


class RegistrationForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True, validators=[validate_password])
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = TblUsers
        fields = ['name', 'username', 'email', 'mobile', 'password', 'confirm_password']

        labels = {
            'name': 'Name',
            'username': 'Username',
            'email': 'Email',
            'mobile': 'Mobile number',
            'password': 'Password',
            'confirm_password': 'Confirm Password',
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        # check if the username and email (if present) already exist in the system
        username = cleaned_data.get('username')
        if TblUsers.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")

        if 'email' in cleaned_data:
            email = cleaned_data.get('email')
            if TblUsers.objects.filter(email=email).exists():
                raise forms.ValidationError("Email already exists.")

        return cleaned_data


class LoginForm(Form):
    username = forms.CharField(label='Username', max_length=255, required=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        # see if the user exists
        qs = TblUsers.objects.filter(username=username)
        if not qs.exists():
            raise forms.ValidationError("Username does not exist.")

        user = qs[0]
        if not user.is_active:
            raise forms.ValidationError(f"User: {user.username} is inactive")

        # check the password with the hash in the database
        if not check_password(password, user.password):
            raise forms.ValidationError("Incorrect password.")

        return cleaned_data
