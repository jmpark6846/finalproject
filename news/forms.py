# -*- coding: utf-8 -*-
from django import forms


class LoginForm(forms.Form):
	email = forms.CharField(label='email', max_length=100)
	password = forms.CharField(label='password', widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    email = forms.CharField(label='Email', max_length=128)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    username = forms.CharField(label='User Name', max_length=64)

    def clean(self):
        cleaned_data = super(JoinForm,self).clean()
        pw = cleaned_data.get('password')
        pw2 = cleaned_data.get('password2')
        email = cleaned_data.get('email')
        username = cleaned_data.get('username')
        if pw != pw2:
            raise forms.ValidationError('패스워드가 일치하지않습니다.')
        existing_user = User.objects.filter(email=email)
        if existing_user :
            raise forms.ValidationError('이미 사용 중인 이메일 입니다.')
        existing_user = User.objects.filter(username=username)
        if existing_user :
            raise forms.ValidationError('이미 사용 중인 이름입니다.')
        return cleaned_data