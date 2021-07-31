from django import forms
from django.forms import fields
from .models import Post, Comment


class PostForm(forms.ModelForm):
    body = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows': "2",
            'cols': "60",
            'placeholder': "What's Happening ?",
            'style': "resize: none; border: none; block-size: fit-content; user-select: text; white-space: pre-wrap; overflow-wrap: break-word;",
        })
    )

    # for the data we want in the form create a Meta class within the PostForm class.
    class Meta:
        # This will tell that the form should be based on the 'post model'.
        model = Post
        # List the fields we want.Here we just want the 'body' field.
        fields = ['body']


class CommentForm(forms.ModelForm):
    comment = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows': "2",
            'cols': "60",
            'placeholder': "Tweet your reply",
            'style': "resize: none; border: none; user-select: text; white-space: pre-wrap; overflow-wrap: break-word;"
        })
    )

    # for the data we want in the form create a Meta class within the PostForm class.
    class Meta:
        # This will tell that the form should be based on the 'post model'.
        model = Comment
        # List the fields we want.Here we just want the 'body' field.
        fields = ['comment']
