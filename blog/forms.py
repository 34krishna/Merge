from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from .models import Post, Comment,Tag
from taggit.forms import TagWidget

User = get_user_model()

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    last_name = forms.CharField(max_length=150, required=True)
    city = forms.CharField(max_length=100, required=True)
    pincode = forms.CharField(max_length=10, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'last_name', 'city', 'pincode')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.last_name = self.cleaned_data["last_name"]
        user.city = self.cleaned_data["city"]
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'phone_num', 'city', 'state', 'country', 'profile', 'bio', 'website']
        widgets = {
            'profile': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_profile(self):
        profile = self.cleaned_data.get('profile')
        return profile or None


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile']

        
class PostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all())
    widget=forms.CheckboxSelectMultiple,
    class Meta:
        model = Post
        fields = ['title', 'content', 'featured_image', 'thumbnail_image', 'published_date', 'category', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'featured_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'thumbnail_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),  
            'tags': TagWidget(attrs={'class': 'form-control', 'placeholder': 'e.g. Django, Web'})  
        }
