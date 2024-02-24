
from celery import shared_task

@shared_task
def actualizar_maniobras():
    print("Hola Luis Felipe Navarro Julio")

    
        
        # fecha_inicio = timezone.now().date()
        # fecha_fin = fecha_inicio + datetime.timedelta(days=30)

        # url_api_pms = 'http://143.198.142.162/api-jwt/auth/'
        # url_api_list = 'http://143.198.142.162/gds/api/v2/STWeb-TQI/?format=json&start_date={}&end_date={}'.format(fecha_inicio, fecha_fin)
        # body_api = {
        #     "username": "PM-STQI",
        #     "password": "G4_JlV0BcYpRZ9w0Q"  
        # }

        # response = requests.post(url_api_pms, data=body_api)
        # token_api = response.json().get('token', '')
        # header = {'Authorization': 'jwt {}'.format(token_api)}

        # listado_maniobras = requests.get(
        #     url_api_list,
        #     headers = header
        # )

        # lista_respuesta = listado_maniobras.json()
        # maniobras_aprobadas = [maniobra for maniobra in lista_respuesta if maniobra['estado'] == 'Aprobado' or maniobra['estado'] == 'En ejecución']


        # for maniobra in maniobras_aprobadas:
        #     try:
        #         ManiobrasTqi.objects.get(codigo = maniobra['codigo'])
        #         print("Actualizar {}".format(maniobra['codigo']))
        #     except ObjectDoesNotExist:
        #         nueva_maniobra = {}
        #         nueva_maniobra["codigo"] = maniobra["codigo"]

        #         tipo_maniobra = ManiobrasTqi.obtener_valor_tipo_maniobra(maniobra["tipo"])
        #         if tipo_maniobra:
        #             nueva_maniobra["tipo"] = tipo_maniobra
        #         else:
        #              nueva_maniobra["tipo"] = ""

        #         nueva_maniobra["descripcion"] = maniobra["descripcion"]
        #         estado_maniobra =  ManiobrasTqi.obtener_valor_estado_stweb(maniobra["estado"])
        #         if estado_maniobra:
        #            nueva_maniobra["estado_stweb"] = estado_maniobra
        #         else:
        #             nueva_maniobra["estado_stweb"] = ""

        #         nueva_maniobra["fecha_inicio"] = datetime.datetime.strptime(maniobra["fecha_trabajo_inicio"], '%Y-%m-%d').date()
        #         nueva_maniobra["hora_inicio"] = datetime.datetime.strptime(maniobra["hora_trabajo_inicio"], '%H:%M:%S').time()
        #         nueva_maniobra["fecha_fin"] = datetime.datetime.strptime(maniobra["fecha_trabajo_fin"], '%Y-%m-%d').date()
        #         nueva_maniobra["hora_fin"] = datetime.datetime.strptime(maniobra["hora_trabajo_fin"], '%H:%M:%S').time()
        #         nueva_maniobra["pdl_asociado"] = maniobra["pdl_asociado"]
        #         nueva_maniobra["fecha_actualizacion"] = timezone.now()                
        #         nueva_maniobra["direccion"] = maniobra["ubicacion"]

        #         cadena = maniobra["circuito"]

        #         indice_corchete_abierto = cadena.find('[')
        #         if indice_corchete_abierto != -1:
        #             indice_espacio_anterior_corchete = cadena.rfind(' ', 0, indice_corchete_abierto)

        #             if indice_espacio_anterior_corchete + 1 == indice_corchete_abierto:
        #                 indice_espacio_anterior_corchete = 0

        #             if indice_corchete_abierto != -1 and indice_espacio_anterior_corchete != -1:
        #                 resultado = cadena[indice_espacio_anterior_corchete:indice_corchete_abierto-1]

        #         circuito = Circuito.objects.filter(nombre__icontains = resultado).first()

        #         if circuito:
        #             nueva_maniobra["circuito"] = circuito.codigo_circuito
        #             subestacion = Subestacion.objects.filter(codigo=circuito.subestacion.codigo).first() #cambiar por la del circuito
        #             if subestacion:
        #                 nueva_maniobra["subestacion"] = subestacion.codigo
        #                 for unit in subestacion.unidades_territoriales.all():
        #                     unidad_general = unit
        #                 if unidad_general:
        #                     nueva_maniobra["unidad_territorial"] = unidad_general.numero
        #                     nueva_maniobra["unidad_ejecutora"] = unidad_general.numero
        #                 else:
        #                     nueva_maniobra["unidad_territorial"] = ""
        #                     nueva_maniobra["unidad_ejecutora"] = ""

        #             else:
        #                 nueva_maniobra["subestacion"] = ""
        #         else:
        #             nueva_maniobra["circuito"] = ""
        #             nueva_maniobra["subestacion"] = ""
        #             nueva_maniobra["unidad_territorial"] = ""
        #             nueva_maniobra["unidad_ejecutora"] = ""

        #         tipo_causa = ManiobrasTqi.obtener_valor_tipo_causa(maniobra["causal"])
        #         if tipo_causa:
        #              nueva_maniobra["causal"] = tipo_causa
        #         else:
        #              nueva_maniobra["tipo"] = ""

        #         nueva_maniobra["estado_tqi"] = "0"
        #         nueva_maniobra["criticidad_maniobra"] = ""
        #         nueva_maniobra["cuadrilla_responsable"] = maniobra["nombre_responsable"]
        #         nueva_maniobra["telefono_cuadrilla_responsable"] = maniobra["telefono_reponsable"]
        #         # nueva_maniobra["inspector_asingado"] = ""

        #         unidad_entera = maniobra["unidad_responsable"]
        #         unidad_opcion = unidad_entera[0:4]

        #         contrato_maniobra = Contrato.objects.filter(nombre__icontains=unidad_opcion, gestoria =  nueva_maniobra["unidad_territorial"]).first()

        #         if contrato_maniobra:
        #             nueva_maniobra["contrato"] = contrato_maniobra.numero_contrato
        #         else:
        #              nueva_maniobra["contrato"] = ""


        #         # nueva_maniobra["contrato"] = ""

        #         nueva_maniobra["municipio"] = ""
        #         nueva_maniobra["vereda_localidad"] = ""

        #         serializando = ManiobrasTqiSerializer(data=nueva_maniobra)
        #         if serializando.is_valid():
        #             serializando.save()
        #         else:
        #             print("errores", serializando.errors)