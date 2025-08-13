# Backend - HADT

Backend para la aplicación "Herramienta para apoyar el diagnóstico de TEP". Se requiere un proyecto de Firebase con los servicios de autenticación y base de datos habilitados (firestore). El proyecto hace uso de las siguientes bibliotecas:

- FastAPI.
- ONNX.
- Firebase admin.

## ¿Cómo ejecutar el proyecto?

1. Cree un entorno virtual de Python:

```
virtualenv -m <nombre-entorno>
```
2. Ejecute el entorno con alguno de los comandos:

```
.\<nombre-entorno>\Scripts\activate        # En el caso de Windows
source .\<nombre-entorno>\Scripts          # En el caso de MacOS y Linux
```

3. Para ejecutar el proyecto debe instalar las dependencias con el siguiente comando:

```
pip install -r requirements-dev.txt
```

4. Para ejecutar la aplicación utilice el siguiente comando:

```
fastapi dev main.py
```

Tenga en cuenta que de esta forma se requiere un header con la clave `Authorization` y el valor `Bearer <token-firebase>` para que las peticiones no sean rechazadas.

### Credenciales de Firebase admin
Debe tener un archivo en formato JSON con el nombre `firebase_token.json`. Este archivo puede ser obtenido desde el apartado de configuración del proyecto en la consola de Firebase.

### Variables de entorno requeridas
```
CORS_ORIGINS=<string>                       # URLs permitidas para CORS (separadas por comas)
ALLOWED_HOSTS=<string>                      # Hosts permitidos (separados por comas)
CLIENTE_FIREBASE_API_KEY=<string>           # API key del proyecto de Firebase
CLIENTE_FIREBASE_AUTH_DOMAIN=<string>       # Dominio de autenticación de Firebase
CLIENTE_FIREBASE_PROJECT_ID=<string>        # ID del proyecto en Firebase
CLIENTE_FIREBASE_STORE_BUCKET=<string>      # ID del bucket de Firestore
CLIENTE_FIREBASE_MESSAGING_SENDER_ID=<int>  # ID para envío de mensajes
CLIENTE_FIREBASE_APP_ID=<string>            # ID de la aplicación de Firebase
CLIENTE_FIREBASE_MEASUREMENT_ID=<string>    # ID de Google Analytics (métricas)
CLIENTE_DRIVE_SCOPES=<string>               # URLs de permisos de Drive requeridos
CLIENTE_CAPTCHA=<string>                    # API key de reCAPTCHA
CAPTCHA_SECRET=<string>                     # Clave secreta de reCAPTCHA
API_RECAPTCHA_URL=<string>                  # URL del API de reCAPTCHA
FIREBASE_ADMIN_CREDS_PATH=<string>          # Ruta al archivo de credenciales de administrador de Firebase
ACTIVAR_DOCS=<string>                       #Activar documentación de la API "false" o "true"
```

## Versión de contenedor

La imagen generada por el `Dockerfile` corresponde a una imagen de despliegue, para construirla use el comando:

```
docker image build -t <nombre-imagen> .
```

Para crear el contenedor utilice el comando:

```
docker container create --name <nombre-contenedor> -p 80:80 --env-file <ruta-archivo> <nombre-imagen>
```

Luego se requiere copiar el archivo con las credenciales de Firebase admin con el comando:

```
docker cp <ruta-archivo-creds> <nombre-contenedor>:<ruta-archivo-contenedor>
```

Finalmente, inicie el contenedor con:

```
docker start <nombre-contenedor>
```

La aplicación será visible en el puerto `80` del `localhost`.

## Sobre el modelo
Puede cambiar el modelo reemplazando el archivo `modelo_redes_neuronbales.onnx` en la carpeta `app/bin`. Tenga en cuenta que se espera
que los datos para realizar diagnósticos ya se encuentren en formato númerico. El backend solo realiza la normalización de los valores y a partir de eso genera la predicción. También se requiere el normalizador utilizado para entrenar los modelos (StandardScaler de Scikit), si desea cambiarlo solo reemplace el archivo `scaler.pkl`.

## Pruebas unitarias

Para ejecutar las pruebas unitarias utilice el siguiente comando:

```
./ejecutar-tests-sh
```  
En la carpeta `tests/scripts` se encuentran los scripts de prueba. En la carpeta `cobertura` se guardan los informes de cobertura de código de las pruebas. De igual forma, la carpeta `resultados` almacena los informes de ejecución en formato **HTML**.  

Sino desea ejecutar las pruebas sin almacenar el informe de resultados y la cobertura, ejecute el comando:

```
pytest
```

Para cambiar la configuración de este apartado, modifique el archivo `pytest.ini` y `conftest.py`. Para más informaciónc consulte la [documentación](https://docs.pytest.org/en/stable/reference/customize.html).