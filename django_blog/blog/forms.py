from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comment, Post, Tag

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class PostForm(forms.ModelForm):
    tag_str = forms.CharField(label='Tags (comma separated)', required=False)

    class Meta:
        model = Post
        fields = ['title', 'content', 'tag_str']

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['tag_str'].initial = ', '.join([t.name for t in self.instance.tags.all()])

    def save(self, commit=True):
        instance = super(PostForm, self).save(commit=False)
        if commit:
            instance.save()
            # Handle tags
            tag_names = [t.strip() for t in self.cleaned_data['tag_str'].split(',') if t.strip()]
            new_tags = []
            for name in tag_names:
                tag, created = Tag.objects.get_or_create(name=name)
                new_tags.append(tag)
            instance.tags.set(new_tags)
        return instance
