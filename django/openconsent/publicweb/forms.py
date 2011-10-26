# Create your forms here.

from django import forms
from models import Decision, Feedback
import tinymce.widgets

from django.utils.translation import ugettext_lazy as _
from django.forms.models import inlineformset_factory
from django.forms.fields import ChoiceField

from widgets import JQueryUIDateWidget

mce_attrs_setting = {
            "theme" : "advanced",
            "theme_advanced_buttons1" : "bold,italic,underline,link,unlink," +
                "bullist,blockquote,undo",
            "theme_advanced_buttons2" : "",
            "theme_advanced_buttons3" : "",
            }

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        widgets = {
                   'description': tinymce.widgets.TinyMCE()
                   }

FeedbackFormSet = inlineformset_factory(Decision, Feedback, 
                                       fields=('description','resolved','rating'),
                                       form=FeedbackForm)

class DecisionForm(forms.ModelForm):
    
    watch = forms.BooleanField(required=False, initial=True)
       
    class Meta:
        model = Decision
        widgets = {
                   'description': tinymce.widgets.TinyMCE(mce_attrs=mce_attrs_setting),
                   'feedback': tinymce.widgets.TinyMCE(mce_attrs=mce_attrs_setting),
                   'decided_date': JQueryUIDateWidget,
                   'effective_date': JQueryUIDateWidget,
                   'review_date': JQueryUIDateWidget,
                   'expiry_date': JQueryUIDateWidget,
                   'deadline': JQueryUIDateWidget,
                   'budget': forms.TextInput(),
                   'people': forms.TextInput()
                   }

EXTRA_CHOICE = (3, _('All'))

class FilterForm(forms.Form):
    #this seems clunky...
    list_choices = list(Decision.STATUS_CHOICES)
    list_choices.append(EXTRA_CHOICE)
    FILTER_CHOICES = tuple(list_choices)
    filter = ChoiceField(choices=FILTER_CHOICES,
                         label = _('Status'),
                         initial=EXTRA_CHOICE[0],
                         required=False,
                         widget = forms.Select(attrs={'onchange':'this.form.submit()'}))
    
class SortForm(forms.Form):
    
    #This is a more robus way of getting attributes to sort on.
    #However it generates a list that is probably too long.
    #TDOD: Think about creating a mechanism to integrate the sorting with the fields that are / 
    #shown on the page
    #list_choices = [(field.name, field.name) for field in Decision.get_fields()]        

    list_choices = [('id', _('id')),
                    ('description', _('description')),
                    ('deadline', _('deadline'))]
    sort = ChoiceField(choices=list_choices,
                         label = _('Sort by'),
                         initial=list_choices[0],
                         required=False,
                         widget = forms.Select(attrs={'onchange':'this.form.submit()'}))
    
