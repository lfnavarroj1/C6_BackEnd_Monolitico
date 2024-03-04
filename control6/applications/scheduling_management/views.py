from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from .models import Programacion
from .serializers import ProgramacionSerializer
from ..static_data.serializers.cuadrilla_serializer import CuadrillaSerializer
from ..static_data.models.cuadrilla import Cuadrilla
from ..work_management.models import Trabajo
from ..node_scheduling_management.models import NodoSeguimiento
from ..budgets_management.models import Nodo

import jwt, json


# 1. CREAR PROGRAMACION ----------------------------------------
class CrearProgramacion(generics.CreateAPIView) :
    serializer_class = ProgramacionSerializer
    def post(self, request) :
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload = jwt.decode(token,'secret', algorithms = ['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        
        # 1. Datos para crear la programación
        datos=request.data
        datos["trabajo"] = Trabajo.objects.filter(id_control=datos["trabajo"]).first() 
        
        # 1. Crear la programación.
        response = Programacion.objects.registrar_programacion(request.data)

        # 2. Crear NodoSeguimiento con los nodos envidos, en el request enviar el listado de nodos
        nodos = request.POST.get('nodos' , '[]')
        array_nodos = json.loads(nodos)


        for nodo in array_nodos:
            nd = Nodo.objects.filter(id_nodo = nodo["nodo"]).first()
            nodo_seguimiento = NodoSeguimiento(
                nodo = nd,
                programacion = response,
                programado = nodo['programado']
            )
            nodo_seguimiento.save()

        serializer = ProgramacionSerializer(response)

        return Response(serializer.data)
# ---------------------------------------------------------------------


# 2. LISTAR PROGRAMACIONES ASOCIADAS A UN TRABAJO --------------------------------
class ListarProgramacion(generics.ListAPIView) :
    serializer_class = ProgramacionSerializer
    def get_queryset(self):
        token=self.request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        pk = self.kwargs.get('pk')

        trabajo = Trabajo.objects.get(id_control=pk)

        print(trabajo)

        queryset = Programacion.objects.filter(trabajo = trabajo).all()

        # Validar si el proceso se ejecuta por ticket
        # if trabajo.proceso.ejecucion_ticket:
        #     queryset = Programacion.objects.filter(ticket = trabajo.ticket).all()
        #     return queryset
        # else:
        #     queryset = Programacion.objects.obtener_programacion(pk)
        return queryset
# ---------------------------------------------------------------------

# 2.1 LISTAR CUADRILLAS DISPONIBLES EN UNA FECHA ----------------------
class ListarCuadrillasDisponibles(generics.ListAPIView):
    serializer_class=CuadrillaSerializer
    # serializer_class=ProgramacionSerializer
    def get_queryset(self):
        token=self.request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        
        lista_cuadrillas=set(list(Cuadrilla.objects.all()))
        # print(lista_cuadrillas)
        date = self.kwargs.get('date')
        programacion_fecha=Programacion.objects.filter(fecha_ejecucion=date)
        # cuadrillas=programacion_fecha.cuadrillas
        cuadrillas_programadas_fecha=[]


        for programacion in programacion_fecha:
            cuadrillas=programacion.cuadrillas.all()
            cuadrillas_programadas_fecha.append(list(cuadrillas))

        lista_programada=set([cuadrilla for list in cuadrillas_programadas_fecha for cuadrilla in list])
        lista_disponible=list(lista_cuadrillas.difference(lista_programada))

        # print(lista_disponible)

        # print(cudrillas_programadas_fecha)
        # queryset=Programacion.objects.filter(fecha_ejecucion=date)
        queryset=lista_disponible
        return queryset
# ---------------------------------------------------------------------


# 2.2 LISTAR CUADRILLAS DEL TRABAJO ----------------------
class ListarCuadrillasTrabajo( generics.ListAPIView ) :
    serializer_class = CuadrillaSerializer
    def get_queryset( self) :
        token = self.request.COOKIES.get( 'jwt' )
        if not token:
            raise AuthenticationFailed( "Unauthenticated!" )
        try:
            payload = jwt.decode( token, 'secret', algorithms=[ 'HS256' ])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed( "Unauthenticated!" )
        
        cuadrillas = self.request.query_params.get( 'q', '' )
        cuadrillas = cuadrillas.split( ',' )
        lista_cuadrillas = Cuadrilla.objects.filter( codigo_cuadrilla__in = cuadrillas ).all()
        queryset = lista_cuadrillas
        return queryset
# ---------------------------------------------------------------------


# 3. OBTENER DETALLES DE UNA PROGRAMACION -----------------------------
class ObtenerProgramacion(generics.RetrieveAPIView):
    serializer_class = ProgramacionSerializer

    def get_queryset(self):
        token = self.request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        # Obtiene el parámetro de la URL 'pk' para buscar el trabajo específico
        pk = self.kwargs.get('pk')
        queryset = Programacion.objects.filter(id_programcion=pk)
        return queryset
# ---------------------------------------------------------------------


# 4. ACTUALIZAR ODM ASOCIADAS A UN TRABAJO ----------------------------
class ActualizarProgramacion(generics.UpdateAPIView):
    def put(self, request, pk):
        token=request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        # usuario=User.objects.get(username=payload['username'])
        pk = self.kwargs.get('pk')

        nodos=request.POST.get('nodos','[]')
        array_nodos=json.loads(nodos)

        print("Entra Aquí")

        try:
            response = Programacion.objects.actualizar_programacion(request.data, pk)
            program=response

            # Eliminar los nodos en seguiemiento y colocar lo nuevo
            nodos_relacionados=NodoSeguimiento.objects.filter(programacion=pk).all()
            for nodo in nodos_relacionados:
                nodo.delete()

            for nodo in array_nodos:
                nd=Nodo.objects.filter(id_nodo=nodo["nodo"]).first()
                # prograd="0"

                nodo_seguimiento=NodoSeguimiento(
                    nodo=nd,
                    programacion=program,
                    programado=nodo['programado']
                )
                nodo_seguimiento.save()
            # dic=request.data
            # campos_actualizados=""
            # for campo in dic.keys():
            #     campos_actualizados=campos_actualizados +", "+campo
            
            # datos={}
            # datos["trabajo"]=response.id_control
            # datos["comentario_trazabilidad"]=f"Se actualizaron los campos {campos_actualizados} del trabajo {response.id_control}"
            # Odm.objects.registrar_trazabilidad(datos, usuario)
            return Response({'message': f"La {response} fue actualizada"}, status=201)
        except Exception as e:
            mensaje = str(e)
            return Response({'error': mensaje}, status=401)
# ---------------------------------------------------------------------


# 5. ELIMINAR ODM ASOCIADAS A UN TRABAJO ------------------------------
class EliminarProgramacion(generics.DestroyAPIView):
    queryset = Programacion.objects.all()
    serializer_class = ProgramacionSerializer
    lookup_field = 'pk'

    def post(self, request, *args, **kwargs):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

    def eliminar_datos_relacionados(self,programacion):
        nodos_relacionados=NodoSeguimiento.objects.filter(programacion=programacion).all()

        for nodo in nodos_relacionados:
            nodo.delete()

    def perform_destroy(self, instance):

        self.eliminar_datos_relacionados(instance)
        instance.delete()
# ---------------------------------------------------------------------
