from django import forms
from memes.models import Meme

class MemeTextForm(forms.ModelForm):
    class Meta:
        model = Meme
        fields = ['meme_text']

class MemePhotoForm(forms.ModelForm):
    class Meta:
        model = Meme
        fields = ['author','photos','caption']

class MemeVideoForm(forms.ModelForm):
    class Meta:
        model = Meme
        fields = ['author','videos', 'caption']