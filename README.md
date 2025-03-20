# Desarrollo de una Aplicación Web con Flask & SQLite

## Objetivos del Taller

1. Desarrollar una aplicación web básica con Flask que interactúe con una base de datos SQLite.
2. Implementar interfaces de usuario utilizando HTML y JavaScript.
3. Gestionar el control de versiones del proyecto con Git y alojarlo en GitHub.
4. Configurar y comprender los diferentes ambientes de desarrollo: desarrollo, pruebas y producción.

## Contenido

1. [Configuración del Entorno](#1-configuración-del-entorno)
2. [Desarrollo de la Aplicación Web](#2-desarrollo-de-la-aplicación-web)
3. [Uso de Git y GitHub](#3-uso-de-git-y-github)
4. [Gestión de Ambientes de Desarrollo](#4-gestión-de-ambientes-de-desarrollo)

---

## 1. Configuración del Entorno

### Instalación de Python y pip

Asegúrense de tener instalada la última versión de Python y su gestor de paquetes, pip. Pueden descargar Python desde su [sitio oficial](https://www.python.org/).

### Creación de un Entorno Virtual

Para aislar las dependencias del proyecto, creen un entorno virtual:

```bash
python -m venv env
```

Activen el entorno virtual:

- En **Windows**:

  ```bash
  .\env\Scripts\activate
  ```

- En **macOS/Linux**:

  ```bash
  source env/bin/activate
  ```

## 2. Desarrollo de la Aplicación Web

### Instalación de Flask

Instalen Flask y otras dependencias necesarias:

```bash
pip install flask
```

### Estructura del Proyecto

Organicen el proyecto de la siguiente manera:

```
my_flask_app/
├── app.py
├── templates/
│   └── index.html
├── static/
│   └── style.css
└── database.db
```

### Configuración de la Base de Datos SQLite

#### Esquema de la Base de Datos (schema.sql):

Este script crea la base de datos y la tabla posts para almacenar las publicaciones.

```sql
DROP TABLE IF EXISTS posts;

CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    content TEXT NOT NULL
);
```
#### Inicialización de la Base de Datos (init_db.py):


```python
import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Primer Post', 'Contenido del primer post')
            )
cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Segundo Post', 'Contenido del segundo post')
            )

connection.commit()
connection.close()
```

### Creación de Rutas y Vistas

Definan las rutas y vistas necesarias para la aplicación:

```python
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        conn = get_db_connection()
        conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                     (title, content))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        conn.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?',
                     (title, content, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('edit.html', post=post)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
```

Para más detalles, pueden consultar este tutorial: [How to Build a Flask Python Web Application from Scratch](https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3)

### Plantillas HTML

En la carpeta `templates/`, creen archivos HTML para las diferentes vistas, como `index.html` y `create.html`.
¡Hola, estimados estudiantes! 👋

A continuación, les proporcionaré ejemplos de cómo crear las plantillas `index.html` y `create.html` para nuestra aplicación web utilizando **Flask**, **HTML** y **Jinja2**. Estas plantillas se almacenarán en el directorio `templates/` de nuestro proyecto.

**1. Plantilla `index.html`:**

Esta plantilla mostrará una lista de publicaciones almacenadas en la base de datos.

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Lista de Publicaciones</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <h1>Publicaciones</h1>
    <a href="{{ url_for('create') }}">Crear nueva publicación</a>
    <ul>
        {% for post in posts %}
            <li>
                <h2>{{ post['title'] }}</h2>
                <p>{{ post['content'] }}</p>
            </li>
        {% else %}
            <li><p>No hay publicaciones disponibles.</p></li>
        {% endfor %}
    </ul>
</body>
</html>
```

En esta plantilla:

- Utilizamos una estructura básica de HTML5
- Incluimos una hoja de estilos CSS ubicada en el directorio `static/`
- Mostramos un encabezado principal y un enlace para crear una nueva publicación
- Iteramos sobre la lista de publicaciones (`posts`) proporcionada por la vista de Flask. Si no hay publicaciones, mostramos un mensaje indicándolo

**2. Plantilla `create.html`:**

Esta plantilla proporcionará un formulario para crear una nueva publicación.

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Crear Publicación</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <h1>Crear Nueva Publicación</h1>
    <form method="post" action="{{ url_for('create') }}">
        <label for="title">Título:</label>
        <input type="text" id="title" name="title" required>
        <br>
        <label for="content">Contenido:</label>
        <textarea id="content" name="content" rows="4" required></textarea>
        <br>
        <button type="submit">Guardar</button>
    </form>
    <a href="{{ url_for('index') }}">Volver a la lista de publicaciones</a>
</body>
</html>
```

En esta plantilla:

- Creamos un formulario HTML que envía datos mediante el método POST a la ruta `create`
- El formulario incluye campos para el título y el contenido de la publicación, ambos marcados como obligatorios
- Añadimos un botón para enviar el formulario y un enlace para volver a la lista de publicaciones

**Consideraciones Adicionales:**

- **Uso de Jinja2:** Flask utiliza el motor de plantillas Jinja2 para renderizar las plantillas. Las expresiones `{{ ... }}` se utilizan para insertar valores de variables, y las sentencias `{% ... %}` para estructuras de control como bucles y condicionales.

- **Estructura del Proyecto:** Es recomendable mantener una estructura organizada en el proyecto. Las plantillas HTML se almacenan en el directorio `templates/`, y los archivos estáticos (como CSS y JavaScript) en el directorio `static/`
*Para profundizar en el uso de plantillas en Flask, pueden consultar la [documentación oficial de Flask](https://flask.palletsprojects.com/en/stable/tutorial/templates/) Estas plantillas les servirán como base para desarrollar las vistas de su aplicación web, permitiendo una separación clara entre la lógica del servidor y la presentación en el cliente.
 
### Integración de Archivos CSS en un Proyecto Flask

#### 1. Estructura del Proyecto
Una estructura organizada es esencial para el mantenimiento y escalabilidad de nuestra aplicación A continuación, se presenta una estructura recomendada:

```
mi_proyecto_flask/
├── app.py
├── static/
│   └── css/
│       └── style.css
├── templates/
│   └── index.html
└── requirements.txt
```

- **`app.py`**: Archivo principal de la aplicación Flask
- **`static/`**: Directorio que contiene archivos estáticos como CSS, JavaScript e imágenes
- **`templates/`**: Carpeta que almacena las plantillas HTML
- **`requirements.txt`**: Archivo que lista las dependencias del proyecto
Esta estructura facilita la organización y el acceso a los diferentes componentes de la aplicación.

#### 2. Creación del Archivo CSS
Dentro del directorio `static/`, crearemos una subcarpeta `css/` para almacenar nuestras hojas de estilo

1. **Crear la carpeta `css/`**:

   ```bash
   mkdir -p static/css
   ```

2. **Crear el archivo `style.css`**:

   ```bash
   touch static/css/style.css
   ```

3. **Agregar estilos en `style.css`**:

   ```css
   /* static/css/style.css */

   body {
       font-family: Arial, sans-serif;
       margin: 0;
       padding: 0;
       background-color: #f4f4f4;
   }

   .container {
       width: 80%;
       margin: auto;
       overflow: hidden;
   }

   header {
       background: #35424a;
       color: #ffffff;
       padding-top: 30px;
       min-height: 70px;
       border-bottom: #e8491d 3px solid;
   }

   header a {
       color: #ffffff;
       text-decoration: none;
       text-transform: uppercase;
       font-size: 16px;
   }
   ```

Estos estilos proporcionarán una apariencia limpia y profesional a nuestra aplicación


#### 3. Consideraciones Adicionales

- **Archivos Estáticos en Flask**:Flask sirve automáticamente los archivos ubicados en la carpeta `static/`. Es importante mantener una organización coherente dentro de este directorio para facilitar el mantenimiento y escalabilidad del proyecto

- **Buenas Prácticas**: Es recomendable separar los archivos CSS, JavaScript e imágenes en subdirectorios dentro de `static/` (`css/`, `js/`, `images/`) para una mejor organización

- **Uso de Frameworks CSS**: Para agilizar el desarrollo y garantizar una apariencia consistente, pueden integrar frameworks CSS como Bootstrap. Esto les permitirá utilizar componentes predefinidos y estilos responsivos

 

## 3. Uso de Git y GitHub

### Inicialización del Repositorio Git

En la raíz del proyecto, inicialicen un repositorio Git:

```bash
git init
```

### Añadir y Confirmar Cambios

Agreguen los archivos y realicen una confirmación inicial:

```bash
git add .
git commit -m "Initial commit"
```

### Creación del Repositorio en GitHub

En GitHub, creen un nuevo repositorio y sigan las instrucciones para vincular el repositorio local con el remoto.

```bash
git remote add origin https://github.com/usuario/nombre_del_repositorio.git
git branch -M main
git push -u origin main
```

Para más detalles sobre cómo subir un proyecto Flask a GitHub, pueden consultar este video: [Python - Flask - Subir proyecto a GitHub](https://www.youtube.com/watch?v=2Moo4LSYBdc)

## 4. Gestión de Ambientes de Desarrollo

### Ambiente de Desarrollo

Utilicen el entorno virtual para instalar y gestionar dependencias.

### Ambiente de Pruebas

Configuren una base de datos de pruebas y utilicen herramientas como `pytest` para realizar pruebas unitarias.

### Ambiente de Producción

Para desplegar la aplicación, consideren el uso de servicios como [PythonAnywhere](https://www.pythonanywhere.com/) o [Heroku](https://www.heroku.com/). Asegúrense de configurar correctamente las variables de entorno y la base de datos de producción.

---
Fabio Hernandez 
Docente
Este ejercicio les permitirá adquirir experiencia práctica en el desarrollo de aplicaciones web con Flask, el uso de sistemas de control de versiones como Git y GitHub, y la gestión de diferentes ambientes de desarrollo. ¡Estoy seguro de que será una experiencia enriquecedora para todos! 🚀

**Fabio Andrés Hernández Rueda**

*Profesor de Ingeniería de Software* 
