# Ejemplo de Algoritmo Personalizado

Este ejemplo muestra cómo empaquetar un algoritmo para su uso con SageMaker. Hemos elegido una implementación sencilla de árboles de decisión con scikit-learn para ilustrar el proceso.

## Modos de Ejecución en SageMaker

SageMaker admite dos modos de ejecución: **entrenamiento**, donde el algoritmo utiliza datos de entrada para entrenar un nuevo modelo, y **servicio**, donde el algoritmo acepta solicitudes HTTP y utiliza el modelo previamente entrenado para realizar inferencias (también llamado "evaluación", "predicción" o "transformación").

El algoritmo que hemos construido aquí admite tanto el entrenamiento como la evaluación en SageMaker utilizando la misma imagen del contenedor. Es completamente razonable construir un algoritmo que solo soporte entrenamiento o evaluación, así como también crear algoritmos que tengan imágenes de contenedor separadas para cada tarea.

### Guía de ejecución:

TODO

## Tecnología Utilizada

Para construir un servidor de inferencia de calidad de producción dentro del contenedor, usamos el siguiente stack que simplifica el trabajo del implementador:

- **nginx**: una capa ligera que maneja las solicitudes HTTP entrantes y gestiona la entrada y salida del contenedor de manera eficiente.
- **gunicorn**: un servidor de trabajo pre-forking WSGI que ejecuta múltiples copias de tu aplicación y distribuye la carga entre ellas.
- **flask**: un marco web sencillo utilizado en la aplicación de inferencia que escribes, permitiéndote responder a solicitudes en los endpoints `/ping` y `/invocations` sin tener que escribir mucho código.

## Estructura del Código de Ejemplo

Los componentes son los siguientes:

- **Dockerfile**: Describe cómo se construye la imagen y qué contiene. Es una receta para tu contenedor y te brinda una gran flexibilidad para construir casi cualquier entorno de ejecución que puedas imaginar. Aquí utilizamos el Dockerfile para describir un stack estándar de ciencia de datos en Python y los scripts simples que vamos a agregar. Consulta la referencia del Dockerfile para ver lo que es posible aquí.
- **build_and_push.sh**: Un script para construir la imagen de Docker (utilizando el Dockerfile mencionado) y enviarla al Registro de Contenedores de Amazon EC2 (ECR) para que pueda ser desplegada en SageMaker. Especifica el nombre de la imagen como argumento de este script. El script generará un nombre completo para el repositorio en tu cuenta y la región de AWS configurada. Si este repositorio de ECR no existe, el script lo creará.
- **decision-trees**: El directorio que contiene la aplicación que se ejecutará en el contenedor. Consulta la siguiente sección para obtener detalles sobre cada uno de los archivos.
- **local-test**: Un directorio que contiene scripts y una configuración para ejecutar trabajos de entrenamiento e inferencia de manera local, para que puedas probar que todo está configurado correctamente.

## La Aplicación que se Ejecuta Dentro del Contenedor

Cuando SageMaker inicia un contenedor, lo invocará con un argumento de **train** (entrenar) o **serve** (servir). Hemos configurado este contenedor para que el argumento se trate como el comando que ejecuta el contenedor. Cuando se entrena, se ejecutará el programa de entrenamiento incluido; y cuando se sirve, se ejecutará el programa de servicio.

- **train**: El programa principal para entrenar el modelo. Cuando construyas tu propio algoritmo, modificarás esto para incluir tu código de entrenamiento.
- **serve**: El envoltorio que inicia el servidor de inferencia. En la mayoría de los casos, puedes utilizar este archivo tal como está.
- **wsgi.py**: El shell de inicio para los trabajadores individuales del servidor. Solo necesita modificarse si cambias la ubicación o el nombre de predictor.py.
- **predictor.py**: El servidor de inferencia específico del algoritmo. Este es el archivo que se modificará con el código de tu propio algoritmo.
- **nginx.conf**: La configuración para el servidor maestro nginx que gestiona los múltiples trabajadores.

## Configuración para Pruebas Locales

El subdirectorio **local-test** contiene scripts y datos de ejemplo para probar la imagen del contenedor construida en la máquina local. Al crear tu propio algoritmo, querrás modificarlo según sea necesario.

- **train-local.sh**: Instancia el contenedor configurado para entrenamiento.
- **serve-local.sh**: Instancia el contenedor configurado para el servicio.
- **predict.sh**: Ejecuta predicciones contra un servidor instanciado localmente.
- **test-dir**: El directorio que se monta en el contenedor con datos de prueba en todos los lugares que coincidan con el esquema del contenedor.
- **payload.csv**: Datos de ejemplo utilizados por predict.sh para probar el servidor.

## Estructura del Directorio Montado en el Contenedor

La estructura del árbol bajo **test-dir** se monta en el contenedor y simula la estructura de directorios que SageMaker crearía para el contenedor en ejecución durante el entrenamiento o el alojamiento.

- **input/config/hyperparameters.json**: Los hiperparámetros para el trabajo de entrenamiento.
- **input/data/training/leaf_train.csv**: Los datos de entrenamiento.
- **model**: El directorio donde el algoritmo escribe el archivo del modelo.
- **output**: El directorio donde el algoritmo puede escribir su archivo de éxito o fracaso.

## Variables de Entorno

Cuando creas un servidor de inferencia, puedes controlar algunas de las opciones de Gunicorn a través de variables de entorno. Estas pueden ser proporcionadas como parte de la llamada a la API **CreateModel**.


| Parámetro              | Variable de Entorno  | Valor Predeterminado       |
| ----------------------- | -------------------- | -------------------------- |
| Número de trabajadores | MODEL_SERVER_WORKERS | El número de núcleos CPU |
| Tiempo de espera        | MODEL_SERVER_TIMEOUT | 60 segundos                |

Recuerda que este ejemplo es un punto de partida y puedes adaptarlo para ajustarlo a tus necesidades. ¡Buena suerte con tu aprendizaje!
