from django.shortcuts import render, HttpResponse, redirect
from miapp.models import Article
from django.db.models import Q
from miapp.forms import FormArticle
from django.contrib import messages

# Create your views here.


layout = """
<h1> Sitio web con Django | CODECRAFTERS </h1>
<hr/>
<ul>
    <li>
        <a href="/inicio">Inicio</a>
    </li>
    <li>
        <a href="/hola-mundo">Quienes somos</a>
    </li>
    <li>
        <a href="/pagina-pruebas">Página de pruebas</a>
    </li>
    <li>
        <a href="/contacto">Contacto</a>
    </li>
</ul>
<hr/>
"""

def index(request):

    html="""
        <h1>Inicio</h1>
        
        <ul>
    
    """
    year =2021
    while year  <= 2050:
        
        if year % 2 == 0:
            html += f"<li>{str(year)}</li>"

        year +=1
            
    html +="</ul>"
    
    nombre = 'CODECRAFTERS'
    lenguajes =  ['Python', 'JavaScript', 'Ruby', 'PHP']

    return render(request, 'index.html', {
        'title':'Inicio',
        'mi_variable': 'Este es el valor de mi variable',
        'nombre' : nombre,
        'lenguajes' : lenguajes,
    })


def hola_mundo(request):
    return render(request, 'hola_mundo.html')
    
def pagina(request, redirigir=0):
    if redirigir ==1:
        return redirect('contacto', nombre="CODE", apellidos="CRAFTERS")
    
    return render(request,'pagina.html')
def contacto(request, nombre="", apellidos=""):
    html ="" 
    if nombre and apellidos:
        html += f"<p>El nombre completo es: </p>"
        html = f"<h3>{nombre} {apellidos}</h3>"
    return HttpResponse(layout+ f"<h2>Contacto  </h2>"+html)


def crear_articulo(request, title, content, public):
    articulo = Article(
        title = title,
        content = content,
        public = public,
    )
    articulo.save()
    
    
    return HttpResponse(f"Articulo Creado: <strong>{articulo.title}</strong> - {articulo.content}")


def save_article(request):
    
    if request.method =='POST':
        title = request.POST['title']
        if len(title) <=5:
            return HttpResponse("Titulo muy corto")
        content = request.POST['content']
        public = request.POST['public']
        articulo = Article(
            title = title,
            content = content,
            public = public,
        )
        articulo.save()
        return HttpResponse(f"Articulo Creado: <strong>{articulo.title}</strong> - {articulo.content}")
        
    else:
        return HttpResponse("<h2> No se ha podido crear el artículo </h2>")
    

def create_article(request):
    return render(request, 'create_article.html')

def create_full_article(request):
    if request.method == 'POST':
        formulario = FormArticle(request.POST)
        if formulario.is_valid():
            data_form = formulario.cleaned_data
            title = data_form.get('title')
            content = data_form.get('content')
            public = data_form.get('public')
            
            # Guardar el artículo
            articulo = Article.objects.create(
                title=title,
                content=content,
                public=public
            )
            articulo.save()
            
            # Redirigir al usuario a la lista de artículos
            return redirect('articulos')
    else:
        formulario = FormArticle()
        
    return render(request, 'create_full_article.html', {'form': formulario})

def articulo(request):
    try:
        articulo= Article.objects.get(title="superman", public=False)
        response = f"Articulo: <br/> {articulo.id}. {articulo.title}"
    except:
        response = "<h1> Artículo no encontrado </h2>"
    return HttpResponse(response)

def editar_articulo(request, id):
    articulo = Article.objects.get(pk=id)
    
    articulo.title = "Batman"
    articulo.content = "Pelicula del 2017"
    articulo.content = True
    
    articulo.save()
    
    return HttpResponse(f"Articulo {articulo.id} editado: <strong>{articulo.title}</strong> - {articulo.content}")

def articulos(request):
    articulos = Article.objects.all().order_by('-id')
    
    """
    articulos = Article.objects.filter(id__lte=12, title__contains="articulo")
    articulos = Article.objects.filter(
        Q(title__contains="2")| Q(public= True)
    )"""
 #articulos = Article.objects.raw("SELECT * FROM miapp_article WHERE title='Articulo 2' AND public=0")
    return render(request, 'articulos.html',{
        'articulos': articulos
    })
    
def borrar_articulo(request, id):
    articulo = Article.objects.get(pk=id)
    articulo.delete()
    return redirect('articulos')
    