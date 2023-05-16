from .models import Comment
from django import forms

# Set up Comment Form Class
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


# Set up Edit Comment Form Class
class EditCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
