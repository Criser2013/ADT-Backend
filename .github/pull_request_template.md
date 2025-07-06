# Plantilla pull-request.
Plantilla sugerida cada que se haga un pull-request, no es necesario que siga este formato especifico pero debe incluir los campos que aquí se mencionan.
Recuerde como asignar como reviewer a su compañero y coloque la etiqueta correspondiente al tipo de pull-request (solución a un bug, funcionalidad nueva, etc.).

## H.U:
Coloque el # de H.U. y el nombre así.  
  
***Ejemplo:***  
  
H.U. 3 - Carrito de compras.  
  
## Funcionalidad añadida.
Dé una equeña descripción de la funcionalidad.  
  
***Ejemplo:***  
  
API endpoints para realizar operaciones CRUD sobre el modelo "Carrito".

## ¿Cómo hacer peticiones?
Describa los pasos necesarios para hacer peticiones, indicando: método HTTP a utilizar, endpoint, cuerpo de la petición, código de respuesta HTTP y respuesta (si la hay). 
Para el cuerpo de la petición y la respuesta, indicar qué campos están presentes y el tipo de dato. 

***Ejemplo:***
1. Se debe estar autenticado.
2. Endpoints disponibles:
    -  **Añadiendo elementos al carrito:** Usando el método `POST` hacia: `/api/cartAdd/`. **Body:** `{ cliente: <email-str>, producto: <id-int>, unids: <int>}`. Devuelve un objeto JSON con los mismos datos enviados y **status code:** `201`.
    -  **Eliminando un elemento:** Usando el método `DELETE` hacia: `/api/cartEdit/<carrito-id>`. Solo devuelve **status code:** `204`.
    -  **Editando un elemento:** Usando el método `PUT` hacia: `/api/cartEdit/<carrito-id>`. Utilice el mismo **body** que en el endpoint de **añadir**. Devuelve un JSON con los mismos datos enviados y **status code**: `200`.
    - **Ver carrito de un usuario:** Usando el método `GET` hacia: `/api/cartCliente/<cliente-email>`. La respuesta es un JSON con los siguientes campos: `{ data: <array-of-JSON>, count: <array-length-int> }` y **status code:** `200`.

**Importante:** Debe estar autenticado y añadir el token CSRF a un encabezado con la clave `X-CSRFToken`(en los navegadores no es necesario).  

## Ejemplos (opcional):
Colocar algunos ejemplos de cómo se harían las peticiones de forma correcta, cómo no deberían hacerse y posibles errores (colocar capturas de pantalla).

***Ejemplo:***

- **CSRF error:** Sin agregar el `CSRF token` a los encabezados de la petición.

![image](https://github.com/Anezeres/ProyectoDesarrollo2/assets/84862634/aa5a3cf2-cb51-4e64-a5f4-c3fa9c5d0eaf)