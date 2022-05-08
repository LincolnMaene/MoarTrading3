from unicodedata import category
from django import forms
from crispy_forms.helper import FormHelper
Exaxmple_Choices=[('question', 'Question'), ('other','Other')]

class order_form_basic(forms.Form):
    timing=[('Day', 'day'), ('Good Till Cancel','good till cancel'), ('Fill or Kill','fill or kill')]
    session=[('Seamless', 'seamless'), ('AM','am'), ('PM','pm'), ('Normal','normal')]
    company_symbol= forms.CharField()
    stock_quantity= forms.IntegerField()
    price_limit= forms.DecimalField()
    timing = forms.ChoiceField(choices=timing)
    session = forms.ChoiceField(choices=session)

class form_example(forms.Form):

    helper=FormHelper()

    #helper.form_show_labels=False
    
    name= forms.CharField()
    email= forms.EmailField(label="E-Mail")
    category=forms.ChoiceField(choices=Exaxmple_Choices)
    subject=forms.CharField (required=False)
    body = forms.CharField(widget=forms.Textarea)