from django.db.models import Q
from django.db.models import Count, Case, When, IntegerField
from .models import Libro, Autor, EjemplarLibro, Genero


#BASICO
# Obtener todos los registros
autores = Autor.objects.all()
 # Obtener un registro por su clave primaria
autor = Autor.objects.get(pk=1)
 # Obtener el primer registro que cumpla con ciertos criterios
autor = Autor.objects.filter(apellido="García Márquez").first()

 # Método 1: Obtener, modificar y guardar
autor = Autor.objects.get(pk=1)
autor.nombre = "Gabriel José"
autor.save()
 # Método 2: Actualizar directamente
Autor.objects.filter(pk=1).update(nombre="Gabriel José")


#OBTENER Y ELIMINAR
autor = Autor.objects.get(pk=1)
autor.delete()

 # Filtrar por condición exacta
autores = Autor.objects.filter(apellido="García Márquez")
 # Filtrar por múltiples condiciones (AND)
autores = Autor.objects.filter(apellido="García Márquez", nombre="Gabriel")
 # Excluir registros
autores = Autor.objects.exclude(apellido="García Márquez")
 # Limitar resultados
autores = Autor.objects.all()[:5]  # Primeros 5 resultados
autores = Autor.objects.all()[5:10]  # Resultados del 6 al 10

 # Ordenar por un campo (ascendente)
autores = Autor.objects.order_by('apellido')
 # Ordenar por un campo (descendente)
autores = Autor.objects.order_by('-fecha_nacimiento')
 # Ordenar por múltiples campos
autores = Autor.objects.order_by('apellido', 'nombre')



# Ejemplo detallado: Mostrar todos los campos de un registro seleccionado
def inspeccionar_registro_individual():
    """
    Función para demostrar diferentes métodos de introspección
    para examinar todos los campos de un registro individual.
    """
    # 1. Seleccionar un registro específico
    autor = Autor.objects.get(pk=1)  # Obtenemos el autor con ID 1
    print(f"\n{'='*50}")
    print(f"DETALLES DEL AUTOR: {autor}")
    print(f"{'='*50}")


 # 2. Método 1: Usando __dict__ para obtener los campos como un diccionario
    # Este método es simple pero no muestra información sobre relaciones o metadatos
    print("\nMÉTODO 1: Usando __dict__")
    print(f"{'-'*40}")
    for campo, valor in autor.__dict__.items():
        if not campo.startswith('_'):  # Excluimos campos internos
            print(f"{campo}: {valor}")

 # 3. Método 2: Usando introspección del modelo a través de _meta
    # Este método es más completo y ofrece información sobre el tipo de campo
    print("\nMÉTODO 2: Usando _meta.fields (introspección)")
    print(f"{'-'*40}")
    for campo in autor._meta.fields:
        nombre_campo = campo.name
        valor = getattr(autor, nombre_campo)
        tipo_campo = campo.get_internal_type()

 # Formatear la salida según el tipo de campo
        if tipo_campo == 'ForeignKey' or tipo_campo == 'OneToOneField':
            if valor:
                objeto_relacionado = valor
                print(f"{nombre_campo} ({tipo_campo}): {objeto_relacionado} [ID: {objeto_relacionado}]")
            else:
                print(f"{nombre_campo} ({tipo_campo}): None")
        elif tipo_campo == 'DateField' or tipo_campo == 'DateTimeField':
            print(f"{nombre_campo} ({tipo_campo}): {valor}")
        else:
            print(f"{nombre_campo} ({tipo_campo}): {valor}")


 # 4. Examinar campos ManyToMany, que requieren manejo especial
    print("\nCAMPOS MANY-TO-MANY:")
    print(f"{'-'*40}")
    for campo in autor._meta.many_to_many:
        nombre_campo = campo.name
        queryset_relacionado = getattr(autor, nombre_campo).all()
        
        print(f"{nombre_campo} (ManyToManyField):")
        if queryset_relacionado.exists():
            for obj in queryset_relacionado:
                print(f"  - {obj} [ID: {obj.id}]")
        else:
            print("  - No hay objetos relacionados")


 # 5. Información sobre el modelo
    print("\nMETADATOS DEL MODELO:")
    print(f"{'-'*40}")
    print(f"Nombre del modelo: {autor._meta.model.__name__}")
    print(f"Tabla en BD: {autor._meta.db_table}")
    print(f"Verbose name: {autor._meta.verbose_name}")
    print(f"Verbose name plural: {autor._meta.verbose_name_plural}")
    print(f"Campos: {[campo.name for campo in autor._meta.fields]}")
    print(f"Unique together: {autor._meta.unique_together}")


 # 6. Revisar permisos
    print("\nPERMISOS ASOCIADOS:")
    print(f"{'-'*40}")
    for permiso in autor._meta.permissions:
        print(f"- {permiso}")
 # Llamado de la función para un ejemplo práctico
 # inspeccionar_registro_individual()

#----------------------------------------------------------------------------

#INTROSPECCION MULTIPLE



# Ejemplo detallado: Recorrer múltiples registros y mostrar sus campos
def inspeccionar_multiples_registros():
    """
    Función para demostrar cómo recorrer múltiples registros
    y mostrar todos sus campos de manera eficiente.
    """
    # 1. Optimizar la consulta para evitar el problema N+1
    # Usamos select_related para cargar las relaciones ForeignKey
    # y prefetch_related para las relaciones ManyToMany
    libros = Libro.objects.select_related('autor').prefetch_related('genero')
    
    # Podríamos añadir filtros si fuera necesario
    # libros = libros.filter(publicado__year__gte=2000)
    
    total_libros = libros.count()
    
    print(f"\n{'='*60}")
    print(f"ANÁLISIS DE {total_libros} LIBROS (CON OPTIMIZACIÓN DE CONSULTAS)")
    print(f"{'='*60}")


 # 2. Recorrer cada registro
    for i, libro in enumerate(libros, 1):
        print(f"\n[LIBRO {i}/{total_libros}]: {libro.titulo}")
        print(f"{'-'*50}")
        
        # 3. Mostrar campos básicos usando introspección
        for campo in libro._meta.fields:
            nombre_campo = campo.name
            tipo_campo = campo.get_internal_type()
            valor = getattr(libro, nombre_campo)
            
            # Tratar de manera especial diferentes tipos de campos
            if tipo_campo == 'ForeignKey' or tipo_campo == 'OneToOneField':
                if valor:
                    print(f"{nombre_campo} ({tipo_campo}): {valor} [ID: {valor.id}]")
                else:
                    print(f"{nombre_campo} ({tipo_campo}): None")
            elif tipo_campo == 'DateField' or tipo_campo == 'DateTimeField':
                print(f"{nombre_campo} ({tipo_campo}): {valor}")
            else:
                print(f"{nombre_campo} ({tipo_campo}): {valor}")
        
        # 4. Mostrar campos ManyToMany
        for campo in libro._meta.many_to_many:
            nombre_campo = campo.name
            objetos_relacionados = getattr(libro, nombre_campo).all()

            print(f"\n{nombre_campo} (ManyToManyField):")
            if objetos_relacionados.exists():
                for obj in objetos_relacionados:
                    print(f"  - {obj} [ID: {obj.id}]")
            else:
                print("  - No hay objetos relacionados")

 # 5. Estadísticas y resumen
    print(f"\n{'='*60}")
    print("RESUMEN DE ANÁLISIS:")
    print(f"{'-'*50}")
    print(f"Total de libros analizados: {total_libros}")
    
    # Podríamos añadir estadísticas adicionales
    generos_counts = {}
    for libro in libros:
        for genero in libro.genero.all():
            generos_counts[genero.nombre] = generos_counts.get(genero.nombre, 0) + 1
    
    if generos_counts:
        print("\nDistribución por género literario:")
        for genero, count in sorted(generos_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  - {genero}: {count} libros ({count/total_libros:.1%})")


# Llamado de la función para un ejemplo práctico
 # inspeccionar_multiples_registros()

