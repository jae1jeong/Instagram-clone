from django.contrib.auth.models import User
from django import forms
from .models import Profile

class SignUpForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    repeat_password = forms.CharField(label="Repeat Password",widget=forms.PasswordInput)

    class Meta:
        model = User
        # 입력 받을 필드 선언
        fields = ["username","password","repeat_password","email",]

    def clean_repeat_password(self):
        cd = self.cleaned_data
        if cd['password'] != cd["repeat_password"]:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")
        return cd['repeat_password']

class ProfileUploadForm(forms.ModelForm):
    model = Profile
    fields = ["nick_name","profile_photo",]
