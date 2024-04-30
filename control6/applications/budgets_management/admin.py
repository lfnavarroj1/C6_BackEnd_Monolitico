# from import_export import resources
# from import_export.admin import ImportExportModelAdmin
# from django.contrib import admin
# from .models import Valorizacion, Nodo, NodoMDO, NodoMAT, EtlBudget


# class ValorizacionResource(resources.ModelResource):
#     class Meta:
#         model = Valorizacion
#         fields = (
#             'id_valorizacion',
#             'trabajo',
#             'monto_mano_obra',
#             'monto_materiales',
#             'fecha_valorizacion',
#             'estado',
#             'nivel_tension',
#             'presupuesto',
#         )

# @admin.register(Valorizacion)
# class ValorizacionAdmin(ImportExportModelAdmin):
#     resource_class = ValorizacionResource
#     list_display = (
#         'id_valorizacion',
#         'trabajo',
#         'monto_mano_obra',
#         'monto_materiales',
#         'estado',
#         'nivel_tension',
#         'presupuesto',
#     )

#     search_fields = (
#         'trabajo', 'id_valorizacion',
#     )


# class NodoResource(resources.ModelResource):
#     class Meta:
#         model = Nodo
#         fields = (

#             'id_nodo',
#             'valorizacion',
#             'nodo',
#             'latitud_inicial',
#             'longitud_inicial',
#             'latitud_final',
#             'longitud_final',
#             'punto_fisico_final',
#             'punto_fisico_inicial',
#             'norma_codensa_punto_inicial',
#             'norma_codensa_punto_final',
#             'tipo_nodo',
#             'tipo_instalacion',
#             'nivel_tension',
#             'tramo',
#             'cod_seccion',
#             'cod_defecto',
#             'valor_mano_obra',
#             'valor_materiales',
#             'id_mare',
#         )

# @admin.register(Nodo)
# class NodoAdmin(ImportExportModelAdmin):
#     resource_class = NodoResource
#     list_display = (
#         'id_nodo',
#         'valorizacion',
#         'nodo',
#         'latitud_inicial',
#         'longitud_inicial',
#     )

#     search_fields = (
#         'valorizacion', 'id_nodo',
#     )


# class NodoMDOResource(resources.ModelResource):
#     class Meta:
#         model = NodoMDO
#         fields = (
#             'nodo',
#             'tipo_trabajo_mdo',
#             'codigo_mdo',
#             'cantidad_replanteada',
#             'cantidad_ejecutada',
#             'cantidad_facturada',
#         )

# @admin.register(NodoMDO)
# class NodoMDOAdmin(ImportExportModelAdmin):
#     resource_class = NodoMDOResource
#     list_display = (
#         'nodo',
#         'tipo_trabajo_mdo',
#         'codigo_mdo',
#         'cantidad_replanteada',
#         'cantidad_ejecutada',
#         'cantidad_facturada',
#     )


# class NodoMATResource(resources.ModelResource):
#     class Meta:
#         model = NodoMAT
#         fields = (
#             'nodo',
#             'tipo_trabajo_mat',
#             'codigo_mat',
#             'cantidad_replanteada',
#             'cantidad_ejecutada',
#             'cantidad_facturada',
#             'aportacion',
#         )

# @admin.register(NodoMAT)
# class NodoMATAdmin(ImportExportModelAdmin):
#     resource_class = NodoMATResource
#     list_display = (
#         'nodo',
#         'tipo_trabajo_mat',
#         'codigo_mat',
#         'cantidad_replanteada',
#         'cantidad_ejecutada',
#         'cantidad_facturada',
#         'aportacion',
#     )


# class EtlBudgetResource(resources.ModelResource):
#     class Meta:
#         model = EtlBudget
#         fields = (
#             'nodo',
#             'instalacion_retiro',
#             'codigo',
#             'cantidad',
#             'mat_mdo',
#             'precio',
#             'aportacion',
#         )

# @admin.register(EtlBudget)
# class EtlBudgetAdmin(ImportExportModelAdmin):
#     resource_class = EtlBudgetResource
#     list_display = (
#         'nodo',
#         'instalacion_retiro',
#         'codigo',
#         'cantidad',
#         'mat_mdo',
#         'precio',
#         'aportacion',
#     )






# from django.contrib import admin
# from import_export import resources
# from import_export.admin import ImportExportModelAdmin
# from .models import Prestacion

# # Register your models here.

# # PRESTACIONES
# class PrestacionResource( resources.ModelResource ):
#     class Meta:
#         import_id_fields = ('codigo_prestacion',)
#         model = Prestacion
#         fields = (
#             'codigo_prestacion',
#             'codigo_elenco',
#             'texto_prestacion',
#             'alcance',
#             'unidad_medida',
#             'posicion',
#             'factor_dispersion',
#             'grupo_mercologico',
#             'precio_prestacion',
#             'contrato',
#         )

# @admin.register( Prestacion )
# class PrestacionAdmin( ImportExportModelAdmin ):
#     resource_class = PrestacionResource
#     list_display = (
#         'codigo_prestacion',
#         'codigo_elenco',
#         'texto_prestacion',
#         'unidad_medida',
#         'posicion',
#         'factor_dispersion',
#         'grupo_mercologico',
#         'precio_prestacion',
#         'contrato',
#     )


# from django.contrib import admin
# from import_export import resources
# from import_export.admin import ImportExportModelAdmin
# from .models import Prestacion

# class PrestacionResource( resources.ModelResource ):
#     class Meta:
#         import_id_fields = ('codigo_prestacion',)
#         model = Prestacion
#         fields = (
#             'codigo_prestacion',
#             'codigo_elenco',
#             'texto_prestacion',
#             'alcance',
#             'unidad_medida',
#             'posicion',
#             'factor_dispersion',
#             'grupo_mercologico',
#             'precio_prestacion',
#             'contrato',
#         )

# @admin.register( Prestacion )
# class PrestacionAdmin( ImportExportModelAdmin ):
#     resource_class = PrestacionResource
#     list_display = (
#         'codigo_prestacion',
#         'codigo_elenco',
#         'texto_prestacion',
#         'unidad_medida',
#         'posicion',
#         'factor_dispersion',
#         'grupo_mercologico',
#         'precio_prestacion',
#         'contrato',
#     )


# from django.contrib import admin
# from import_export import resources
# from import_export.admin import ImportExportModelAdmin
# from .models import Material

# # Register your models here.

# # PRESTACIONES
# class MaterialResource( resources.ModelResource ):
#     class Meta:
#         import_id_fields = ( 'codigo_material' )
#         model = Material
#         fields = (
#             'codigo_material',
#             'descripcion',
#             'unidad_medida',
#             'aportacion',
#             'precio',
#         )

# @admin.register( Material )
# class MaterialAdmin( ImportExportModelAdmin ):
#     resource_class = MaterialResource
#     list_display = (
#             'codigo_material',
#             'descripcion',
#             'unidad_medida',
#             'aportacion',
#             'precio',
#     )
#     search_fields=(
#     'codigo_material',
#     )
#     list_filter=(
#         'aportacion', 'codigo_material',
#     )


#     from django.contrib import admin
# from import_export import resources
# from import_export.admin import ImportExportModelAdmin
# from .models import Material

# class MaterialResource( resources.ModelResource ):
#     class Meta:
#         import_id_fields = ( 'codigo_material' )
#         model = Material
#         fields = (
#             'codigo_material',
#             'descripcion',
#             'unidad_medida',
#             'aportacion',
#             'precio',
#         )

# @admin.register( Material )
# class MaterialAdmin( ImportExportModelAdmin ):
#     resource_class = MaterialResource
#     list_display = (
#             'codigo_material',
#             'descripcion',
#             'unidad_medida',
#             'aportacion',
#             'precio',
#     )
#     search_fields=(
#     'codigo_material',
#     )
#     list_filter=(
#         'aportacion', 'codigo_material',
#     )