from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm, Form
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import check_password
from .models import Roles, Usersinfo, Staff, Staffs, Salary


class UsersInfoForm(ModelForm):
    class Meta:
        model = Usersinfo
        fields = ['name', 'username', 'role', 'isactive', 'email', 'mobile']

        widgets = {
            'mobile': forms.TextInput(attrs={'maxlength': 20})
        }

        labels = {
            'name': 'Name',
            'username': 'Username',
            'email': 'Email',
            'mobile': 'Mobile',
            'role': 'Role',
            'isactive': 'Is Active',
        }
        error_messages = {
            'name': {
                'unique': 'User with that name already exists.',
            },
            'username': {
                'unique': 'User with that username already exists.',
            },
        }


class RolesForm(ModelForm):
    class Meta:
        model = Roles
        fields = ['role']

        labels = {
            'role': 'Role'
        }
        error_messages = {
            'role': {
                'unique': 'Role with that name already exists.',
            },
        }


class SalaryForm(ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})  # Use an HTML5 date picker
    )

    class Meta:
        model = Salary
        fields = ['date', 'purpose', 'reason', 'quantity', 'rate', 'total', 'personel',
                  'voucher', 'status', 'comment', ]

        labels = {
            'date': 'Date',
            'purpose': 'Purpose',
            'reason': 'Reason',
            'quantity': 'Quantity',
            'rate': 'Rate',
            'total': 'Total',
            'personel': 'Personnel',
            'voucher': 'Voucher',
            'status': 'Status',
            'comment': 'Additional comments'
        }


class StaffForm(ModelForm):
    class Meta:
        model = Staff
        fields = ['name', 'post', 'salary', 'address', 'mobile', 'reference',]

        labels = {
            'name': 'Name',
            'post': 'Post',
            'salary': 'Salary',
            'address': 'Address',
            'mobile': 'Mobile',
            'reference': 'Reference',
        }
        error_messages = {
            'name': {
                'unique': 'Staff member with that name already exists.',
            },
        }


class StaffsForm(ModelForm):
    class Meta:
        model = Staffs
        fields = ['name', 'designation', 'address', 'mobile',]

        labels = {
            'name': 'Name',
            'designation': 'Designation',
            'address': 'Address',
            'mobile': 'Mobile',
        }


class RegistrationForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True, validators=[validate_password])
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = Usersinfo
        fields = ['name', 'username', 'email', 'mobile', 'password', 'confirm_password']

        widgets = {
            'mobile': forms.TextInput(attrs={'maxlength': 20})
        }

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

        # check if the username and email already exist in the system
        username = cleaned_data.get('username')
        if Usersinfo.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")

        email = cleaned_data.get('email')
        if Usersinfo.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")

        return cleaned_data


class LoginForm(Form):
    username = forms.CharField(label='Username', max_length=255, required=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)

    def clean(self):
        try:
            cleaned_data = super().clean()
            username = cleaned_data.get('username')
            password = cleaned_data.get('password')

            # see if the user exists
            qs = Usersinfo.objects.filter(username=username)
            if not qs.exists():
                raise forms.ValidationError("Username does not exist.")

            user = qs[0]
            if not user.isactive:
                raise forms.ValidationError(f"User: {user.username} is inactive")

            # check the password with the hash in the database
            if not check_password(password, user.password):
                raise forms.ValidationError("Incorrect password.")

        except ValidationError as ve:
            # we get here if super().clean() fails
            # we use this block to skip our custom validations and to just reraise the Error
            raise ve

        return cleaned_data


class ChangePasswordForm(Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    new_password = forms.CharField(widget=forms.PasswordInput, required=True, validators=[validate_password])
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)

    labels = {
        'username': 'Username',
        'password': 'Password',
        'new_password': 'New Password',
        'confirm_password': 'Confirm New Password',
    }

    def clean(self):
        try:
            cleaned_data = super().clean()
            username = cleaned_data.get('username')
            password = cleaned_data.get('password')
            new_password = cleaned_data.get('new_password')
            confirm_password = cleaned_data.get('confirm_password')

            # see if the user exists
            qs = Usersinfo.objects.filter(username=username)
            if not qs.exists():
                raise forms.ValidationError("Username does not exist.")

            user = qs[0]
            if not user.isactive:
                raise forms.ValidationError(f"User: {user.username} is inactive")

            # check the password with the hash in the database
            if not check_password(password, user.password):
                raise forms.ValidationError("Incorrect password.")

            # see if new password is the same as the old password
            if new_password == password:
                raise forms.ValidationError("New Password and Existing Passwords are the same")

            # see if the new password and the confirm_passwords match
            if new_password != confirm_password:
                raise forms.ValidationError("Confirm Password does not match New Password")

        except ValidationError as ve:
            # we get here if super().clean() fails
            # we use this block to skip our custom validations
            raise ve

        return cleaned_data


class AdminChPasswordForm(Form):
    username = forms.CharField(max_length=255, required=True)
    new_password = forms.CharField(widget=forms.PasswordInput, required=True, validators=[validate_password])
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)

    labels = {
        'username': 'Username',
        'new_password': 'New Password',
        'confirm_password': 'Confirm New Password',
    }

    def clean(self):
        try:
            cleaned_data = super().clean()
            username = cleaned_data.get('username')
            new_password = cleaned_data.get('new_password')
            confirm_password = cleaned_data.get('confirm_password')

            # see if the new password and the confirm_passwords match
            if new_password != confirm_password:
                raise forms.ValidationError("Confirm Password does not match New Password")

        except ValidationError as ve:
            # we get here if super().clean() fails
            # we use this block to skip our custom validations
            raise ve

        return cleaned_data
