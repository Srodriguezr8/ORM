from django.db.models import Q
from django.db.models import Count, Case, When, IntegerField
from .models import Libro, Autor, EjemplarLibro, Genero
# Consultas básicas
 # 1. Todos los libros
libros = Libro.objects.all()
 # 2. Libros ordenados por título
libros = Libro.objects.order_by('titulo')
 # 3. Filtrado por autor
libros_de_autor = Libro.objects.filter(autor__apellido='García Márquez')
 # 4. Búsqueda por palabra clave en título o resumen
libros = Libro.objects.filter(Q(titulo__icontains='quijote') | Q(resumen__icontains='quijote'))
 # 5. Ejemplares disponibles
ejemplares_disponibles = EjemplarLibro.objects.filter(estado='d')


#-----------------------------------------------------------------------------------------------------------------

 # Consultas avanzadas
 # 6. Contar libros por género

generos_con_conteo = Genero.objects.annotate(num_libros=Count('libro'))
 # 7. Autores con sus libros (evitando N+1 query)
autores_con_libros = Autor.objects.prefetch_related('libros')
 # 8. Libro con su autor (evitando N+1 query)
libros_con_autor = Libro.objects.select_related('autor')
 # 9. Contar ejemplares por estado
 
libro_stats = Libro.objects.annotate(
    ejemplares_disponibles=Count(
        Case(
            When(ejemplares__estado='d', then=1),
            output_field=IntegerField()
        )
    ),
    ejemplares_prestados=Count(
        Case(
            When(ejemplares__estado='p', then=1),
            output_field=IntegerField()
        )
    )
 )
 # 10. Consulta compleja: libros que no tienen ejemplares disponibles

libros_sin_disponibles = Libro.objects.exclude(
 ejemplares__estado='d'
 ).distinct()
 # 11. Libros con múltiples filtros combinados
libros = Libro.objects.filter(
 Q(autor__apellido='Cervantes') &
 (Q(genero__nombre='Novela') | Q(genero__nombre='Clásico')) &
 ~Q(ejemplares__estado='m')
 ).distinct()

