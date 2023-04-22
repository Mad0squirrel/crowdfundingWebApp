# -*- encoding: utf-8 -*-


from distutils.log import error
from django import forms

from django.core.validators import RegexValidator, FileExtensionValidator
from django.urls import URLPattern
from .models import Register
from django.forms.widgets import NumberInput

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class SignupForm(forms.ModelForm):
    """
    Класс формы регистрации пользователя.



    Параметры:
    ----------
    forms.ModelForm

    Атрибуты:
    ----------
    - first_name: CharField с виджетом TextInput для ввода имени пользователя
    - last_name: CharField с виджетом TextInput для ввода фамилии пользователя
    - email: EmailField с виджетом EmailInput для ввода электронной почты пользователя
    - password: CharField с виджетом PasswordInput для ввода пароля пользователя
    - confirmPassword: CharField с виджетом PasswordInput для подтверждения пароля пользователя
    - phone: CharField с виджетом TextInput для ввода номера телефона пользователя
    - image: ImageField с виджетом FileInput для загрузки профильной фотографии пользователя и валидатором
    FileExtensionValidator для проверки на расширение файла "jpg", "png" или "jpeg"
    """
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={
            "placeholder": "First Name",
            "class": "form-control"
        }))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={
            "placeholder": "Last Name",
            "class": "form-control"
        }))
    email = forms.EmailField(max_length=200, help_text='Required', widget=forms.EmailInput(attrs={
        "placeholder": "Email",
        "class": "form-control"
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Password",
        "class": "form-control"
    }))
    #TODO:add regex to password
    confirmPassword = forms.CharField(label="confirm password", widget=forms.PasswordInput(attrs={
        "placeholder": "Confirm Password",
        "class": "form-control"
    }))
    phone = forms.CharField(label="phone number", validators=[RegexValidator(
        '^01[0125][0-9]{8}$', message="Enter a Valid Egyption Phone Number")], widget=forms.TextInput(attrs={
            "placeholder": "Phone Number",
            "class": "form-control"
        }))
    image = forms.ImageField(label="profile image", validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])], widget=forms.FileInput(attrs={
        "placeholder": "Profile Image",
        "class": "form-control"
    }))

    def clean(self):
        """
        Метод clean класса SignupForm проверяет валидность данных, введенных в форму регистрации. Если данные не
        проходят валидацию, то он вызывает исключение forms.ValidationError.



        :return: dict: словарь с валидными данными.
        """
        errors = {}
        cleaned_data = super().clean()
        valpassword = self.cleaned_data.get('password')
        valconfirmpassword = self.cleaned_data.get("confirmPassword")
        if valpassword != valconfirmpassword:
            errors['confirmPassword'] = ('password not match')
        email = self.cleaned_data.get('email')
        if Register.objects.filter(email=email).exists():
            errors['email'] = ("Email exists")
        phone = self.cleaned_data.get('phone')
        if Register.objects.filter(phone=phone).exists():
            errors['phone'] = ("phone exists")

        if errors:
            raise forms.ValidationError(errors)


    class Meta:
        """
        Класс Meta для определения метаданных формы SignupForm.

        Атрибуты:
        ----------
        model : Register
             Модель, с которой связана форма.
        fields : tuple
            Поля модели, которые должны быть отображены в форме.
        """
        model = Register
        fields = ('first_name', 'last_name',  'email',
                  'password', 'confirmPassword', 'phone', 'image')


class LoginForm(forms.Form):
    """
    Форма аутентификации пользователей.

    Атрибуты:
    ----------
    email : EmailField
        Поле для ввода email адреса пользователя.
    password : CharField
        Поле для ввода пароля пользователя.
    """
    email = forms.EmailField(max_length=200, help_text='Required',widget=forms.EmailInput(attrs={
        "placeholder": "Email",
        "class": "form-control"
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Password",
        "class": "form-control"
    }))


class EditProfileForm(forms.ModelForm):
    """
    Форма, используемая для редактирования информации профиля пользователя.



    Атрибуты:
    --------
    first_name (CharField): Поле для имени пользователя.
    last_name (CharField): Поле для фамилии пользователя.
    phone (CharField): Поле для номера телефона пользователя.
    image (ImageField): Поле для изображения профиля пользователя.
    password (CharField): Поле для пароля пользователя.
    confirmPassword (CharField): Поле для подтверждения пароля пользователя.
    country (CharField): Поле для страны пользователя.
    birthdate (DateField): Поле для даты рождения пользователя.
    facebook_profile (URLField): Поле для URL профиля Facebook пользователя.

    Примечание:
    ----------
    Форма наследуется от forms.ModelForm.
    """
    first_name = forms.CharField(
        
        widget=forms.TextInput(
        attrs={
            "placeholder": "First Name",
            "class": "form-control",
      
        }),
        min_length=2,
        max_length=10,
       
    )
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={
            "placeholder": "Last Name",
            "class": "form-control"
        }),
        min_length=2,
        max_length=10,
        )
    phone = forms.CharField(label="phone number", validators=[RegexValidator(
        '^01[0125][0-9]{8}$', message="Enter a Valid Egyption Phone Number")], widget=forms.TextInput(attrs={
            "placeholder": "Phone Number",
            "class": "form-control"
        }))
    image = forms.ImageField(required=False, label="profile image", validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])], widget=forms.FileInput(attrs={
        "placeholder": "Profile Image",
        "class": "form-control"
    }))
    password = forms.CharField(required=False,widget=forms.PasswordInput(attrs={
        "placeholder": "Password",
        "class": "form-control"
    }))
    #TODO:add regex to password
    confirmPassword = forms.CharField(required=False,label="confirm password", widget=forms.PasswordInput(attrs={
        "placeholder": "Confirm Password",
        "class": "form-control"
    }))
    country = forms.CharField(required=False,validators=[RegexValidator(
        '^[A-Za-z]+$', message="Enter a Valid Country Name")],widget=forms.TextInput(
        attrs={
            "placeholder": "Country",
            "class": "form-control"
        }))
    birthdate = forms.DateField(required=False,
        widget=NumberInput(
            attrs={
                'placeholder': 'BirthDate',
                'type': 'date',
                'class': 'form-control'
            }
        ))
    facebook_profile = forms.URLField(required=False, error_messages={'required': 'Please Enter a valid Url'},widget=forms.URLInput(
        attrs={
                'placeholder': 'Profile Facebook Url',
                'class': 'form-control'
            }
    ))


    def clean(self):
        """
        Очищает и проверяет данные формы.


        :return: dict: Словарь очищенных данных.
        """
        errors = {}
        cleaned_data = super().clean()
        valpassword = self.cleaned_data.get('password')
        valconfirmpassword = self.cleaned_data.get("confirmPassword")
        if valpassword != valconfirmpassword:
            errors['confirmPassword'] = ('password not match')  
        phone = self.cleaned_data.get('phone')
        if Register.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
            errors['phone'] = ("phone exists")
     
   
        if errors:
            raise forms.ValidationError(errors)

    class Meta:
        """
        Определяет метаданные модели Register, используемые формой EditProfileForm.

        Атрибуты:
            model (Register): Модель, используемая формой.
            fields (tuple): Кортеж полей формы, которые будут отображаться в шаблоне.

        Примечание:
            Класс Meta используется для определения метаданных формы и является вложенным в класс EditProfileForm.
        """
        model = Register
        fields = ('first_name','last_name','phone','image','country' , 'password', 'confirmPassword','birthdate','facebook_profile')


class ResetPasswordEmailForm(forms.Form):
    """
        Форма для восстановления пароля.

        Атрибуты:
            email (EmailField): Поле для ввода электронной почты пользователя.
        """
    email = forms.EmailField(max_length=200, help_text='Required', widget=forms.EmailInput(attrs={
        "placeholder": "Email",
        "class": "form-control"
    }))

class ResetPasswordForm(forms.ModelForm):
    """
    Класс ResetPasswordForm используется для создания формы сброса пароля.

    Атрибуты:
        password (CharField): Поле для ввода пароля пользователя.
        confirmPassword (CharField): Поле для подтверждения введенного пароля.

    Примечание:
        Класс наследуется от forms.ModelForm.
    """
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Password",
        "class": "form-control"
    }))
    #TODO:add regex to password
    confirmPassword = forms.CharField(label="confirm password", widget=forms.PasswordInput(attrs={
        "placeholder": "Confirm Password",
        "class": "form-control"
    }))
    def clean(self):
        """
        Очищает и проверяет данные формы.

        :return: dict: Словарь очищенных данных.
        """
        errors = {}
        cleaned_data=super().clean()
        valpassword=self.cleaned_data.get('password')
        valconfirmpassword=self.cleaned_data.get("confirmPassword")
        if valpassword != valconfirmpassword:
             errors['confirmPassword'] =  ('password not match')
        if errors:
            raise forms.ValidationError(errors)

    class Meta:
        """
        Определяет метаданные модели Register, используемые формой EditProfileForm.

        Атрибуты:
            model (Register): Модель, используемая формой.
            fields (tuple): Кортеж полей формы, которые будут отображаться в шаблоне.

        Примечание:
            Класс Meta используется для определения метаданных формы и является вложенным в класс EditProfileForm.
        """
        model = Register
        fields = ('password', 'confirmPassword')
        
class DeleteAccountForm(forms.Form):
    """
        Форма для подтверждения удаления учетной записи.

        Атрибуты:
            password (CharField): Поле для ввода пароля пользователя.
        """
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Password",
        "class": "form-control"
    }))
