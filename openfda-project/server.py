import http.server
import socketserver
import json


DNS_openfda = 'api.fda.gov'
parametro_json = '/drug/label.json'
parametro_drogas = '&search=active_ingredient:'
parametro_compañias = '&search=openfda.manufacturer_name:'
MAX_OPEN_REQUESTS = 5
class OpenFDAParser():
    def resultados (self, limit = '10'):
        conexion = http.client.HTTPSConnection(DNS_openfda)
        conexion.request('GET', parametro_json + '?limit=' + str(limit))
        print(parametro_json + '?limit=' + str(limit))
        respuesta = conexion.getresponse()
        leer_medicamentos = respuesta.read().decode('utf8')
        datos = json.loads(leer_medicamentos)
        resultados = datos['results']
        return resultados

    def resultados_search_meds (self, limit = '10'):
        drug = self.path.split('=')[1]
        connection = http.client.HTTPSConnection(DNS_openfda)
        connection.request('GET', parametro_json + '?limit=' + str(limit) + parametro_drogas + drug)
        respuesta_0 = connection.getresponse()
        leer_medicamento_o_empresa = respuesta_0.read().decode('utf8')
        dato = json.loads(leer_medicamento_o_empresa)
        return dato
    def resultados_search_busin (self, limit = '10'):
        company = self.path.split('=')[1]
        connection = http.client.HTTPSConnection(DNS_openfda)
        connection.request('GET', parametro_json + '?limit=' + str(limit) + parametro_compañias + company)
        respuesta_0 = connection.getresponse()
        leer_medicamento_o_empresa = respuesta_0.read().decode('utf8')
        dato = json.loads(leer_medicamento_o_empresa)
        return dato
class OpenFDAHTML(OpenFDAParser):
    def pagina_principal(self):
        formulario = 'formulario.html'
        with open(formulario) as f:
            formulario = f.read()
        return formulario

    def visualizar_medicamentos(self, list_drugs):
        medshtml = '''
                                <html>
                                    <head>
                                        <meta charset = 'utf8'>
                                        <title> Medicamentos de OpenFDA. </title>
                                        <link rel="shortcut icon" href="https://pbs.twimg.com/profile_images/703722838486851588/ZpuXjIAr.jpg" />
                                    </head>
                                    <body style = 'color:Gray'>
                                        <h1 style = 'color: MediumSeaGreen'> <a href='/'>Home</a> Aquí puede ver los medicamentos requeridos:</h1>
                                        <ul>'''
        for elemento in list_drugs:
            medshtml += '<li>' + elemento + '</li>'

        medshtml += '''
                                        </ul>
                                    </body>
                                </html>'''
        return medshtml
    def visualizar_empresas(self, list_companies):
        businesshtml = '''
<html>
    <head>
        <meta charset = 'utf8'>
        <title> Empresas de OpenFDA. </title>
        <link rel="shortcut icon" href="https://pbs.twimg.com/profile_images/703722838486851588/ZpuXjIAr.jpg" />
    </head>
    <body style = 'color:Gray'>
        <h1 style = 'color:MediumSeaGreen'> <a href='/'>Home</a> Aquí puede ver las empresas requeridas:</h1>
        <ul>'''
        for element in list_companies:
            businesshtml += '<li>'+ element + '</li>'

        businesshtml += '''
        </ul>
    </body>
</html>'''
        return businesshtml
    def informacion_ingredientes(self, medicina_lista):
        htmlingredientes = '''
<html>
    <head>
        <meta charset = 'utf8'>
        <title>Ingrediente activo común a los fármacos.</title>
        <link rel="shortcut icon" href="https://pbs.twimg.com/profile_images/703722838486851588/ZpuXjIAr.jpg" />
        </head>
        <body style = 'color:Gray'
            <h1 style = 'color:MediumSeaGreen'> <a href='/'>Home</a> Aquí puede visualizar todos los fármacos que tienen como ingrediente activo el que ha elegido:</h1>
            <ul>
                            '''
        for ingrediente in medicina_lista:
            htmlingredientes += "<li>" + ingrediente + "</li>"

        htmlingredientes += '''
            </ul>
        </body>
</html>
                            '''
        return htmlingredientes
    def informacion_empresas(self, empresa_lista):
        htmlempresas = '''
<html>
    <head>
        <meta charset = 'utf8'>
        <title>Información específica de la empresa elegida.</title>
        <link rel="shortcut icon" href="https://pbs.twimg.com/profile_images/703722838486851588/ZpuXjIAr.jpg" />
        </head>
        <body style = 'color:Gray'
            <h1 style = 'color:MediumSeaGreen'> <a href='/'>Home</a> Aquí puede visualizar la información:</h1>
            <ul>
                            '''
        for empresa in empresa_lista:
            htmlempresas += "<li>" + empresa + "</li>"

        htmlempresas += '''
            </ul>
        </body>
</html>
                            '''
        return htmlempresas
    def advertencias(self, list_warning):
        advertenciashtml = '''
<html>
    <head>
        <meta charset="utf-8">
        <title> Advertencias OpenFDA </title>
        <link rel="shortcut icon" href="https://pbs.twimg.com/profile_images/703722838486851588/ZpuXjIAr.jpg" />
    </head>
    <body style = 'color:OliveDrab'> <a href='/'>Home</a> Por favor, lea con precaución las advertencias:
        <ul>'''
        for el in list_warning:
            advertenciashtml += '<li>'+ el +'</li>'
        advertenciashtml += '''</ul>
                        </body>
                        </html>'''
        return advertenciashtml
    def control_errores(self):
        errores = '''
<html>
    <head>
        <meta charset="utf-8">
        <title> Error </title>
        <link rel="shortcut icon" href="https://pbs.twimg.com/profile_images/703722838486851588/ZpuXjIAr.jpg" />
    </head>
    <body>
        <h3> <a href='/'>Home</a> Se ha detectado un error: </h3>
        <h5 style = 'color:Gray'> No se ha encontrado información sobre el valor introducido. </h5>
    </body>
    </html>'''
        return errores
class serverHTTPRequestHandler(http.server.BaseHTTPRequestHandler, OpenFDAHTML):

    def do_GET(self):
        recurso_lista = self.path.split('?')
        if len(recurso_lista) > 1:
            parametro = recurso_lista[1]
        else:
            parametro = ''
        if parametro:
            analizar_limite = parametro.split('=')
            try:
                if analizar_limite[0] == 'limit':
                    limit = int(analizar_limite[1])
                    if limit > 100:
                         limit = 1
            except ValueError:
                limit = 1

        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = self.pagina_principal()
            self.wfile.write(bytes(html, 'utf8'))
        elif 'listDrugs' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            lista_medicamentos = []
            resultados = self.resultados(limit)
            for resultado in resultados:
                if ('generic_name' in resultado['openfda']) == True:
                    lista_medicamentos.append(resultado['openfda']['generic_name'][0])
                else:
                    lista_medicamentos.append('No se conoce.')
            html_medicamentos = self.visualizar_medicamentos(lista_medicamentos)
            self.wfile.write(bytes(html_medicamentos, 'utf8'))
        elif 'listCompanies' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            lista_empresas = []
            resultados = self.resultados(limit)
            for resultado in resultados:
                if('manufacturer_name' in resultado['openfda']) == True:
                    lista_empresas.append(resultado['openfda']['manufacturer_name'][0])
                else:
                    lista_empresas.append('No se conoce.')
            html_empresas = self.visualizar_empresas(lista_empresas)
            self.wfile.write(bytes(html_empresas, 'utf8'))
        elif 'listWarnings' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            lista_advertencias = []
            resultados = self.resultados(limit)
            for resultado in resultados:
                if ('warnings' in resultado):
                    lista_advertencias.append (resultado['warnings'][0])
                else:
                    lista_advertencias.append('No se conoce.')
            html_warnings = self.advertencias(lista_advertencias)
            self.wfile.write(bytes(html_warnings, 'utf8'))
        elif 'searchDrug' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            medicina_lista = []
            dato = self.resultados_search_meds()
            try:
                result = dato['results']
                for resultado in result:
                    if ('substance_name' in resultado['openfda']):
                        medicina_lista.append(resultado['openfda']['generic_name'][0])
                    else:
                        medicina_lista.append('No se conoce')
                buscar_html_medicina = self.informacion_ingredientes(medicina_lista)
                self.wfile.write(bytes(buscar_html_medicina, "utf8"))
            except KeyError:
                error = self.control_errores()
                self.wfile.write(bytes(error, 'utf8'))

        elif 'searchCompany' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            empresa_lista = []
            dato = self.resultados_search_busin()
            try:
                resultados_0 = dato['results']
                for resultado in resultados_0:
                    if ('manufacturer_name' in resultado['openfda']):
                        empresa_lista.append(resultado['openfda']['manufacturer_name'][0])
                    else:
                        empresa_lista.append('No se conoce')
                buscar_html_empresa = self.informacion_empresas(empresa_lista)
                self.wfile.write(bytes(buscar_html_empresa, "utf8"))
            except KeyError:
                error = self.control_errores()
                self.wfile.write(bytes(error, 'utf8'))
        elif 'redirect' in self.path:
            port = 8000
            self.send_response(302)
            self.send_header('Location', 'http://localhost:'+ str(port))
            self.end_headers()
        elif 'secret' in self.path:
            self.send_response(401)
            self.send_header('WWW-Authenticate', "Basic realm ='Es mi servidor'")
            self.end_headers()
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain; charset = utf8')
            self.end_headers()
            self.wfile.write("No ha sido posible encontrar el recurso '{}'".format(self.path).encode('utf8'))
        return
handler = serverHTTPRequestHandler
class OpenFDAClient():
    host = 'localhost'
    port = 8000
    address = (host, port)
    socketserver.TCPServer.allow_reuse_address= True
    server = socketserver.TCPServer(address, handler)
    print("serving at port", port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
            print('El servidor ha sido interrumpido por usted.')

    server.server_close()
    print('El servidor se ha parado.')
