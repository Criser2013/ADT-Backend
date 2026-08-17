# Backend — HADT

API REST que proporciona las funcionalidades de inferencia y gestión de usuarios para la aplicación **“Herramienta para apoyar el diagnóstico de TEP”**.

Este proyecto requiere un proyecto de **Firebase** con los servicios de **Authentication** y **Firestore** habilitados. El backend utiliza las siguientes tecnologías y bibliotecas principales:

- **FastAPI**
- **ONNX**
- **ONNX Runtime**
- **Firebase Admin SDK**
- **LIME**
- **reCAPTCHA**

El objetivo del proyecto es proporcionar la infraestructura backend para una aplicación web responsiva que permita utilizar un modelo de inteligencia artificial como herramienta de apoyo al diagnóstico de **tromboembolismo pulmonar (TEP)**.

En particular, este componente aloja el modelo de clasificación de instancias de TEP y proporciona funcionalidades para la gestión de los usuarios registrados en la aplicación.

## Requisitos

Antes de ejecutar el proyecto, es necesario contar con los siguientes recursos y configuraciones:

- Un proyecto creado en **Firebase** con los servicios de **Authentication** y **Cloud Firestore** habilitados.
- **Firebase Authentication** configurado para utilizar **Google** como proveedor de autenticación.
- Una clave de acceso a la **API de Google Drive**. Para obtenerla, es necesario crear y configurar un proyecto en **Google Cloud**.
- Una clave privada para utilizar **Google reCAPTCHA v2**.
- Las credenciales necesarias para utilizar el **Firebase Admin SDK**.
- **Python** y **pip** instalados.
- **Docker**, en caso de realizar un despliegue mediante contenedores.

## Ejecución en entorno de desarrollo

### 1. Clonar el repositorio

```bash
git clone https://github.com/Criser2013/ADT-Backend.git
cd ADT-Backend
```

### 2. Crear un entorno virtual de Python

Se recomienda utilizar un entorno virtual para aislar las dependencias del proyecto.

```bash
pip install virtualenv
virtualenv <nombre-entorno>
```

### 3. Activar el entorno virtual e instalar las dependencias

- En Windows:

```bash
.\<nombre-entorno>\Scripts\activate
```

- En macOS/Linux:
```bash
source <nombre-entorno>/bin/activate
```

Una vez activado el entorno, instalar las dependencias:

```bash
pip install -r requirements-dev.txt
```

### 4. Configurar las variables de entorno

Crear un archivo `.env` a partir de `.env.example` y establecer los valores correspondientes para cada variable de entorno.

### 5. Ejecutar el proyecto en modo desarrollo

```bash
fastapi dev "./app/main.py" --port 5000
```


La aplicación estará disponible en el puerto 5000.

La documentación interactiva de la API estará disponible en:
```
/docs — documentación Swagger UI.
/redoc — documentación ReDoc.
```

Por ejemplo:
```
http://localhost:5000/docs
http://localhost:5000/redoc
```

## Despliegue en producción

La aplicación puede desplegarse mediante servicios de alojamiento como Render o utilizando un contenedor Docker.

Se recomienda construir una imagen a partir del Dockerfile incluido en el repositorio.

### 1. Construir la imagen
```bash
docker image build -t <nombre-imagen> .
```

### 2. Configurar las variables de entorno

Preparar un archivo .env que contenga las variables de entorno requeridas por la aplicación.

### 3. Crear el contenedor
```bash
docker container create \
  --name <nombre-contenedor> \
  -p 80:80 \
  --env-file <ruta-archivo-env> \
  <nombre-imagen>
```

### 4. Copiar las credenciales de Firebase Admin

Copiar el archivo de credenciales de **Firebase Admin SDK** al contenedor:

```bash
docker cp <ruta-archivo-creds> <nombre-contenedor>:<ruta-archivo-contenedor>
```

### 5. Iniciar el contenedor
```bash
docker start <nombre-contenedor>
```


Una vez iniciado, la API estará disponible en el puerto `80`: `http://localhost:80`. También puede accederse mediante `http://127.0.0.1:80`.

## Modelo de ML para la clasificación de TEP

El proyecto utiliza un modelo de redes neuronales basado en `MLPClassifier` de **Scikit-learn** para clasificar las instancias de TEP.

El modelo se encuentra exportado al formato **ONNX**, lo que permite realizar la inferencia mediante **ONNX Runtime** y facilita su integración independientemente del lenguaje o framework utilizado para entrenarlo originalmente.

El modelo puede reemplazarse por otra versión compatible sustituyendo el archivo: `app/bin/modelo_redes_neuronales.onnx`

## Explicación de las predicciones

Las explicaciones de las predicciones se generan mediante la biblioteca **LIME** (*Local Interpretable Model-agnostic Explanations*).

El objeto explicador se encuentra almacenado en: `app/bin/explicador.pkl`


Este objeto está configurado para:

- Generar **2000 muestras** a partir de cada instancia analizada.
- Identificar y retornar los **10 atributos más relevantes** para la predicción.

Para modificar el comportamiento del explicador, es necesario generar una nueva configuración compatible y reemplazar el archivo `explicador.pkl`.

## Pruebas y aseguramiento de la calidad

El aseguramiento de la calidad y la validación del correcto funcionamiento de la aplicación son aspectos fundamentales durante su desarrollo.

El proyecto cuenta con pruebas unitarias implementadas mediante pytest, orientadas a validar las principales funcionalidades del backend.

Actualmente, los indicadores de cobertura son:

- **Cobertura de sentencias:** 100 %
- **Cobertura de ramas:** 96 %

Los casos de prueba y los scripts relacionados se encuentran en: `/tests/scripts`


Los resultados de las pruebas y los informes de cobertura se almacenan, respectivamente, en:

```
/tests/resultados
/tests/cobertura
```

### Ejecución de las pruebas

Las pruebas pueden ejecutarse mediante cualquiera de las siguientes opciones:

```bash
pytest
```

o, utilizando el script proporcionado por el proyecto:
```bash
./ejecutar-tests.sh
```