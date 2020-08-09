from django import forms
from article.models import Articel,Message

class ArticleForm(forms.ModelForm):
    class Meta:
        model=Articel
        fields='__all__'
        exclude=['click_num','love_num']

class MessageForm(forms.ModelForm):
    class Meta:
        model=Message
        fields='__all__'
      