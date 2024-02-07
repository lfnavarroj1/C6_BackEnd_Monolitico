from django.db import models

from ...static_data.models.cuadrilla import Cuadrilla
from ..models.lcl import Lcl


class ProgramacionManager( models.Manager ) :
    def registrar_programacion(self, req) :
        datos = {}
        campos_creacion = [
            "trabajo",
            "fecha_ejecucion",
            "alcance",
            "estado",
            "observacion",
            "planeacion_segura"
        ]

        for campo in campos_creacion:
            if campo in req:
                if req[campo] == "" or req[campo] is None:
                    datos[campo] = ""
                else:
                    datos[campo] = req[campo]
            else:
                datos[campo] = ""

        datos["pdl"] = True if req["pdl"] == "true" else False
        datos["pi"] = True if req["pi"] == "true" else False
        datos["pstl"] = True if req["pstl"] == "true" else False
        datos["vyp"] = True if req["vyp"] == "true" else False
        datos["ticket"] = True if req["ticket"] == "true" else False

        # Validar con que se realiza la programación
        programacion = self.create( **datos )

        if req[ "lcls" ] != "":
            lista_lcls = list( map( int, req[ "lcls" ].split( ',' ) ) )
            programacion.lcls.set( Lcl.objects.filter( pk__in = lista_lcls ) )
        
        if req[ "cuadrillas" ] != "":
            lista_cuadrillas = list( map( str, req[ "cuadrillas" ].split( ',' ) ) )
            programacion.cuadrillas.set( Cuadrilla.objects.filter( pk__in = lista_cuadrillas ) )

        return programacion
    

    def obtener_programacion( self, id_control ):
        result = self.filter( lcls__odms__valorizacion__trabajo__id_control = id_control ).distinct(  )
        return result
    

    def actualizar_programacion( self, programacion_data, programacion ) :
        programacion_actual = self.get( pk = programacion )

        print("El problema viene por aquí")
        print(programacion_data)

        campos_actualizables = [
            "fecha_ejecucion",
            "cuadrillas",
            "lcls",
            "alcance",
            "observacion",
            "estado",
        ]

        # Actualizando las maniobras necesarias
        maniobras = [
            "pdl",
            "pi",
            "pstl",
            "vyp",
            "ticket"
        ]

        for maniobra_necesaria in maniobras:
            setattr (programacion_actual, maniobra_necesaria, True if programacion_data[ maniobra_necesaria ] == "true" else False)
        
        # CAMPOS RELACIONADOS
        for campo in campos_actualizables:
            if campo in programacion_data:
                if campo == "cuadrillas" :
                    lista_cuadrillas = list( map( str, programacion_data[ "cuadrillas" ].split( ',' ) ) )
                    programacion_actual.cuadrillas.set( Cuadrilla.objects.filter( pk__in = lista_cuadrillas ) )
                elif campo == "lcls":
                    if programacion_data[ "lcls" ] != "":
                        lista_lcls = list( map( int, programacion_data[ "lcls" ].split( ',' ) ) )
                        programacion_actual.lcls.set( Lcl.objects.filter( pk__in = lista_lcls ) )
                else:
                    print(campo)
                    setattr (programacion_actual, campo, programacion_data[campo])
        
        programacion_actual.save()
        return programacion_actual