from django import forms

from .models import Post, Comment

class PostForm(forms.ModelForm):
    """
    Post add and update model form
    """
    image = forms.FileField(
        required=False, 
        widget=forms.FileInput(attrs={
            # 'class':'custom-file-input', 
            # 'name':'image',
            # 'id':'ImageInputPost'
            })
    )
    content = forms.CharField(
        label='',
        required=False, 
        widget=forms.Textarea(attrs={
            'class':'form-control', 
            'name':'content', 
            'placeholder':"What's on your mind?",
            'row':6,
            'style':"resize: none;",
        })
    )
    restrict_comment = forms.BooleanField(required=False)

    class Meta:
        model = Post 
        fields = ['content', 'restrict_comment', 'image']
        # widgets = {'image':forms.FileInput(
        #         attrs={'class':'custom-file-input', 'id':'ImageInputPost'} 
        # )}

    def clean(self):
        """
        Validate if at least one of content and image field is not empty.
        """
        image = self.cleaned_data.get('image')
        content = self.cleaned_data.get('content')
        if not image and not content:
            raise forms.ValidationError("You must either write post or add picture.")
        return self.cleaned_data    

class CommentForm(forms.ModelForm):
    """
    Comment model form
    """
    content = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'class':'form-control float-right input-add-comment',
            # 'id':'add-comment', 
            'name':'content', 
            'placeholder':"Type a comment...",
            'rows':'1',
            'style':"resize: none;",
            'autocomplete':'off',
        })
    )
    
    class Meta:
        model = Comment
        fields = ['content']