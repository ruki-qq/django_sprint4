from django import forms

from .constants import DATETIME_FORMAT
from .models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = (
            'is_published',
            'author',
        )
        widgets = {
            'pub_date': forms.DateTimeInput(
                format=DATETIME_FORMAT,
                attrs={'type': 'datetime-local'},
            )
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
