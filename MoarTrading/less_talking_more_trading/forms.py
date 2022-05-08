from unicodedata import category
from django import forms
from crispy_forms.helper import FormHelper
Exaxmple_Choices=[('question', 'Question'), ('other','Other')]

class Watchlist_query_form(forms.Form):
 
    name= forms.CharField()
    symbol= forms.CharField()
    date = forms.CharField(label="Date (Y-m-d)")
    quantity=forms.IntegerField()
    price_avg=forms.DecimalField()
    commission=forms.DecimalField()


class Movers_Query_Form(forms.Form):
    change_choice=[('VALUE', 'VALUE'), ('PERCENT','PERCENT')]
    direction_choice=[('UP', 'UP'), ('DOWN','DOWN')]
    market_choice=[('$COMPX','NASDAQ COMPOSITE'), ('$DJI','DOW JONE'), ('$SPX.X','S&P 500')]


    index= forms.ChoiceField(label="Market", choices=market_choice)
    change = forms.ChoiceField(label="Type of change", choices=change_choice)
    direction= forms.ChoiceField(label="Which direction?", choices=direction_choice)


class options_form(forms.Form):
   
    underlying_symbol= forms.CharField()
    quantity=forms.IntegerField()
    
class options_query_form(forms.Form):
    put_or_call=[('PUT', 'p'), ('Call','c')]
    underlying_symbol= forms.CharField()
    start_date = forms.DateTimeField()
    strike_number=forms.IntegerField()
    end_date = forms.DateTimeField()
    contract_type = forms.ChoiceField(choices=put_or_call)




class Quote_Query_Form(forms.Form):
    symbol=forms.CharField(label="Company Symbol")
    

class sell_form_basic(forms.Form):
    
    timing=[('Day', 'day'), ('Good Till Cancel','good till cancel'), ('Fill or Kill','fill or kill')]
    session=[('Seamless', 'seamless'), ('AM','am'), ('PM','pm'), ('Normal','normal')]

    sell_company_symbol= forms.CharField()
    sell_quantity= forms.IntegerField()
    sell_price_limit= forms.DecimalField()
    timing = forms.ChoiceField(choices=timing)
    session = forms.ChoiceField(choices=session)
    

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