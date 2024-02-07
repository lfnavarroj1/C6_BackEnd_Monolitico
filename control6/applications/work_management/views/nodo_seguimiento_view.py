from rest_framework.generics import ( ListAPIView )
from rest_framework.exceptions import AuthenticationFailed

from ..models.lcl import Lcl
from ..models.valorizacion import Valorizacion, Nodo

from ..serializers.valorizacion_serializer import NodoSerializer
from ..serializers.nodo_seguimiento_serializers import NodoSeguimientoSerializer
from ..models.nodo_seguimiento import NodoSeguimiento

import jwt
from django.db.models import Q


# 1. LISTAR NODOS ASOCIADOS A UNA PROGRAMACION --------------------------------
class ListarNodosSeguimiento(ListAPIView): 
    serializer_class=NodoSeguimientoSerializer
    def get_queryset(self):
        token=self.request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        pk = self.kwargs.get('pk')
        queryset=NodoSeguimiento.objects.filter(programacion=pk)
        return queryset
# ------------------------------------------------------------------------------
    
# 2. LISTAR NODOS DISPONIBLES ASOCIADOS A LCLs ---------------------------------
class ListarNodosDisponiblesLcl(ListAPIView):
    serializer_class=NodoSerializer
    def get_queryset(self):
            token=self.request.COOKIES.get('jwt')
            if not token:
                raise AuthenticationFailed("Unauthenticated!")
            try:
                payload=jwt.decode(token,'secret',algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed("Unauthenticated!")
            
            vlcls=self.request.query_params.get('vlcls','')
            vect_lcls=vlcls.split(',')
            
            # 1. Listar todos los nodos asociados a una LCL
            v_odms=[]
            for lcl in vect_lcls:
                dato=Lcl.objects.filter(lcl=lcl).all()
                vodms=[odm for l in dato for odm in l.odms.all()]
                for odm in vodms:
                    if odm in v_odms:
                        pass
                    else:
                        v_odms.append(odm)

            v_val=list(set([od.valorizacion for od in v_odms]))

            v_nodos=[]
            for val in v_val:
                nodos=Nodo.objects.filter(valorizacion=val).all()
                for nodo in nodos:
                    if nodo in v_nodos:
                        pass
                    else:
                        v_nodos.append(nodo)
            # 2. Listar todos los nodos ejecutados completo
            v_nodos_programados_completos=[]
            v_nodos_ejecutados_completos=[]
            v_nodos_programados_completos=list(set(NodoSeguimiento.objects.filter(
                Q(nodo__in=v_nodos),
                Q(programado='1'),
                Q(ejecutado=None),
                # Q(id_control__icontains=kword) | Q(caso_radicado__icontains=kword) | Q(ticket__icontains=kword),
            )))
            v_nodos_ejecutados_completos=list(set(NodoSeguimiento.objects.filter(
                Q(nodo__in=v_nodos),
                Q(ejecutado='1'),
                # Q(id_control__icontains=kword) | Q(caso_radicado__icontains=kword) | Q(ticket__icontains=kword),
            )))

            print(v_nodos)
            print(v_nodos_ejecutados_completos)
            print(v_nodos_programados_completos)

            for x in v_nodos_ejecutados_completos:
                print(x.nodo)
                nodo_remover=Nodo.objects.filter(id_nodo=x.nodo).first()
                print(nodo_remover)
                if nodo_remover in v_nodos:
                    v_nodos.remove(nodo_remover)
                print(v_nodos)

            for x in v_nodos_programados_completos:
                print(x.nodo)
                nodo_remover=Nodo.objects.filter(id_nodo=x.nodo).first()
                print(nodo_remover)
                if nodo_remover in v_nodos:
                    v_nodos.remove(nodo_remover)
                print(v_nodos)
            


            # 3. Listar todos los nodos programados completos, con ejecutado vacío

            # 4. Crear un arreglo con los que no se encuentren en el vector nodos_completo.

            return v_nodos
# -------------------------------------------------------------------------------
    

# 3. LISTAR NODOS DISPONIBLES ASOCIADOS A UNA VALORIZACION --------------------------------
class ListarNodosDisponiblesTrabajo(ListAPIView):
    serializer_class=NodoSerializer
    def get_queryset(self):
            token=self.request.COOKIES.get('jwt')
            if not token:
                raise AuthenticationFailed("Unauthenticated!")
            try:
                payload=jwt.decode(token,'secret',algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed("Unauthenticated!")
            
            id_control=self.kwargs.get('pk')

            v_val=Valorizacion.objects.filter(trabajo__id_control=id_control).all()

            print(v_val)

            # v_val=list(set([od.valorizacion for od in v_odms]))

            v_nodos=[]
            for val in v_val:
                nodos=Nodo.objects.filter(valorizacion=val).all()
                for nodo in nodos:
                    if nodo in v_nodos:
                        pass
                    else:
                        v_nodos.append(nodo)
            # 2. Listar todos los nodos ejecutados completo
            v_nodos_programados_completos=[]
            v_nodos_ejecutados_completos=[]
            v_nodos_programados_completos=list(set(NodoSeguimiento.objects.filter(
                Q(nodo__in=v_nodos),
                Q(programado='1'),
                Q(ejecutado=None),
                # Q(id_control__icontains=kword) | Q(caso_radicado__icontains=kword) | Q(ticket__icontains=kword),
            )))
            v_nodos_ejecutados_completos=list(set(NodoSeguimiento.objects.filter(
                Q(nodo__in=v_nodos),
                Q(ejecutado='1'),
                # Q(id_control__icontains=kword) | Q(caso_radicado__icontains=kword) | Q(ticket__icontains=kword),
            )))

            print(v_nodos)
            print(v_nodos_ejecutados_completos)
            print(v_nodos_programados_completos)

            for x in v_nodos_ejecutados_completos:
                print(x.nodo)
                nodo_remover=Nodo.objects.filter(id_nodo=x.nodo).first()
                print(nodo_remover)
                if nodo_remover in v_nodos:
                    v_nodos.remove(nodo_remover)
                print(v_nodos)

            for x in v_nodos_programados_completos:
                print(x.nodo)
                nodo_remover=Nodo.objects.filter(id_nodo=x.nodo).first()
                print(nodo_remover)
                if nodo_remover in v_nodos:
                    v_nodos.remove(nodo_remover)
                print(v_nodos)
            


            # 3. Listar todos los nodos programados completos, con ejecutado vacío

            # 4. Crear un arreglo con los que no se encuentren en el vector nodos_completo.

            return v_nodos
# -------------------------------------------------------------------------------
    

# 4. LISTAR NODOS PROGRAMADOS -------------------------------------------
class ListarNodosProgramados(ListAPIView):
    serializer_class=NodoSerializer
    def get_queryset(self):
            token=self.request.COOKIES.get('jwt')
            if not token:
                raise AuthenticationFailed("Unauthenticated!")
            try:
                payload=jwt.decode(token,'secret',algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed("Unauthenticated!")
            
            id_programacion=self.kwargs.get('pk')

            print(id_programacion)

            nodos_programados=NodoSeguimiento.objects.filter(programacion=id_programacion).all()

            print(nodos_programados)

            v_nodos=[]
            for nodo in nodos_programados:
                print(nodo.nodo)
                nodo_add=Nodo.objects.filter(id_nodo=nodo.nodo).first()
                print(nodo_add)
                if nodo_add in v_nodos:
                    pass
                else:
                    v_nodos.append(nodo_add)

            return v_nodos
# ---------------------------------------------------------------------
