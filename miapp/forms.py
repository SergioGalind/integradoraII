from django import forms 
from django.core import validators

class FormArticle(forms.Form):
    
    title = forms.CharField(
        label="Titulo",
        max_length=20,
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder':'Ingrese el titulo del articulo',
                'class': 'titulo_form_article'
                }
            ),
        validators=[
            validators.MinLengthValidator(4, 'El título no debe ser tan corto'),
            validators.RegexValidator('^[A-Za-z0-9]*$', 'El titulo esta mal formado', 'invalid_title')
        ]
    )
    content = forms.CharField( 
        label="Contenido",
        widget=forms.Textarea,
        validators=[
            validators.MaxLengthValidator(50, 'Es demasiado texto')
        ]
    )
    
    content.widget.attrs.update({
        'placeholder':'Ingrese el contenido del articulo',
        'class': 'contenido_form_article',
        'id': 'contenido_form'
    })
    public_options =[
        (1,"Sí"),
        (0, "No")
    ]
    
    public =forms.TypedChoiceField(
        label= "¿Es público?",
        choices = public_options
    )
