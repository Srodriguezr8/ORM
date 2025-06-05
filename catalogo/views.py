from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.db.models import Count, Q
from .models import Libro, Autor, EjemplarLibro, Genero

# Create your views here.

def index(request):
    """Vista para la página de inicio del sitio."""
    # Generar contadores para algunos de los objetos principales
    num_libros = Libro.objects.count()
    num_ejemplares = EjemplarLibro.objects.count()
    num_ejemplares_disponibles = EjemplarLibro.objects.filter(estado='d').count()
    num_autores = Autor.objects.count()
    
    # Libros que contienen 'novela' en el título
    num_libros_novela = Libro.objects.filter(titulo__icontains='novela').count()
    
    context = {
        'num_libros': num_libros,
        'num_ejemplares': num_ejemplares,
        'num_ejemplares_disponibles': num_ejemplares_disponibles,
        'num_autores': num_autores,
        'num_libros_novela': num_libros_novela,
    }
    
    return render(request, 'index.html', context=context)

class LibroListView(generic.ListView):
    model = Libro
    paginate_by = 10
    
    def get_queryset(self):
        # Filtrar por términos de búsqueda si hay alguno
        query = self.request.GET.get('q')
        if query:
            return Libro.objects.filter(
                Q(titulo__icontains=query) |
                Q(autor__nombre__icontains=query) |
                Q(autor__apellido__icontains=query)
            ).select_related('autor')
        
        # Devolver todos los libros
        return Libro.objects.select_related('autor')
    

    def get_context_data(self, **kwargs):
        # Llamar a la implementación base para obtener el contexto
        context = super().get_context_data(**kwargs)
        
        # Agregar estadísticas de libros al contexto
        context['generos_populares'] = Genero.objects.annotate(
            num_libros=Count('libro')
        ).order_by('-num_libros')[:5]
        
        return context
    
class LibroDetailView(generic.DetailView):
    model = Libro
    
    def get_queryset(self):
        # Optimizar consulta cargando relacionados
        return Libro.objects.select_related('autor').prefetch_related('genero', 'ejemplares')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Añadir información de disponibilidad de ejemplares
        libro = self.get_object()
        context['ejemplares_disponibles'] = libro.ejemplares.filter(estado='d').count()
        
        # Libros relacionados (mismo autor o géneros)
        context['libros_relacionados'] = Libro.objects.filter(
            Q(autor=libro.autor) | Q(genero__in=libro.genero.all())
        ).exclude(id=libro.id).distinct()[:5]
        
        return context