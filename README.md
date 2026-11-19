# KeyGarden 🌱

**KeyGarden** es una aplicación de escritorio desarrollada en Python cuyo objetivo es facilitar la creación, el almacenamiento y la gestión de contraseñas de forma sencilla e intuitiva.

El proyecto nace como una herramienta personal para ayudar a los usuarios a generar contraseñas seguras sin tener que inventarlas manualmente y almacenarlas en una bóveda digital cifrada.

La aplicación cuenta con una interfaz gráfica que permite realizar las operaciones principales desde una única ventana, sin necesidad de utilizar comandos en la terminal para gestionar las contraseñas.

## ✨ Características principales

- **Generación automática de contraseñas:** crea contraseñas aleatorias para evitar tener que inventarlas manualmente.
- **Caracteres personalizables:** utiliza exclusivamente letras mayúsculas, letras minúsculas y números, sin incluir símbolos especiales.
- **Longitud configurable:** permite elegir la longitud de la contraseña dentro del rango establecido por la aplicación.
- **Contraseñas más robustas:** garantiza que cada contraseña generada incluya al menos una letra mayúscula, una minúscula y un número.
- **Mostrar y ocultar contraseñas:** permite visualizar las contraseñas guardadas cuando sea necesario y ocultarlas para proteger su privacidad.
- **Copiar al portapapeles:** facilita copiar una contraseña para utilizarla en otras aplicaciones o páginas web.
- **Guardar contraseñas:** permite almacenar las contraseñas generadas en una bóveda local.
- **Eliminar contraseñas:** permite retirar de la bóveda aquellas entradas que ya no se necesiten.
- **Cifrado automático:** protege el contenido de la bóveda mediante cifrado Fernet.

## 🛠️ Tecnologías utilizadas

El proyecto utiliza diferentes herramientas y bibliotecas de Python. Cada una cumple una función concreta dentro del funcionamiento de KeyGarden.

### 1. Python

**Python** es el lenguaje de programación principal utilizado para desarrollar toda la aplicación.

Se encarga de gestionar la lógica del programa, generar las contraseñas, guardar y recuperar los datos, realizar las operaciones de cifrado y coordinar los diferentes componentes.

Se ha elegido Python por su sintaxis sencilla, su versatilidad y la gran cantidad de bibliotecas disponibles, lo que permite desarrollar aplicaciones de escritorio sin necesidad de utilizar varios lenguajes de programación.

### 2. Tkinter

**Tkinter** es la biblioteca estándar de Python para crear interfaces gráficas de usuario (GUI).

Su función en KeyGarden es proporcionar la ventana y los elementos visuales con los que interactúa el usuario.

Gracias a Tkinter, la aplicación puede incorporar:

- Ventanas y paneles.
- Botones para generar, guardar y eliminar contraseñas.
- Campos de texto para introducir información.
- Tablas para mostrar las contraseñas almacenadas.
- Elementos para mostrar u ocultar las contraseñas.

La principal ventaja de Tkinter es que permite desarrollar interfaces gráficas utilizando Python, sin tener que recurrir a tecnologías web.

### 3. Cryptography

**Cryptography** es una biblioteca de Python que proporciona herramientas criptográficas para proteger información.

En KeyGarden se utiliza para implementar el cifrado y descifrado de los datos almacenados en la bóveda.

Su función es evitar que las contraseñas se guarden directamente como texto legible en el archivo de almacenamiento.

Esta biblioteca proporciona los mecanismos necesarios para transformar los datos originales en información cifrada y recuperarlos posteriormente cuando la aplicación necesita utilizarlos.

### 4. Fernet

**Fernet** es una herramienta criptográfica proporcionada por la biblioteca Cryptography.

Se utiliza para cifrar y descifrar la información de la bóveda de KeyGarden.

Cuando se guarda una contraseña, los datos se cifran antes de almacenarse. Cuando se vuelve a abrir la aplicación, se utiliza la clave correspondiente para descifrar la información y mostrarla al usuario.

Fernet también incorpora mecanismos de autenticación que permiten detectar si los datos cifrados han sido modificados o manipulados.

### 5. Secrets

**Secrets** es un módulo incluido en la biblioteca estándar de Python que permite generar valores aleatorios adecuados para aplicaciones relacionadas con la seguridad.

En KeyGarden se utiliza para generar las contraseñas.

A diferencia de los generadores aleatorios habituales destinados a tareas generales, `secrets` está diseñado para generar valores impredecibles mediante fuentes de aleatoriedad adecuadas para usos criptográficos.

Esto permite crear contraseñas aleatorias de forma más apropiada para un gestor de contraseñas.

### 6. JSON

**JSON** es un formato ligero de intercambio y almacenamiento de datos.

En KeyGarden se utiliza para organizar la información de la bóveda antes de guardarla en el archivo `vault.json`.

Permite estructurar los datos de manera ordenada para que la aplicación pueda almacenarlos, recuperarlos y gestionarlos posteriormente.

Es importante destacar que el contenido de la bóveda se cifra antes de almacenarse, por lo que el archivo no debería contener las contraseñas en texto legible.

### 7. Pathlib

**Pathlib** es un módulo de Python que facilita el trabajo con rutas y archivos del sistema.

En KeyGarden se utiliza para localizar los archivos necesarios para el funcionamiento de la aplicación, como la bóveda y la clave de cifrado.

Su uso permite gestionar las rutas de una forma más clara y compatible con diferentes sistemas operativos.

## 📁 Estructura del proyecto

El proyecto está organizado en varios archivos, cada uno con una responsabilidad diferente:

```text
KeyGarden/
│
├── main.py
├── interfaz.py
├── Generador.py
├── requirements.txt
└── README.md
```

**Descripción de los archivos:**

- `main.py`: es el punto de entrada de la aplicación. Se encarga de iniciar el programa y abrir la interfaz gráfica.
- `interfaz.py`: contiene la interfaz gráfica desarrollada con Tkinter. Gestiona los botones, campos de texto, tablas y las acciones del usuario.
- `Generador.py`: contiene la lógica principal del generador y gestor de contraseñas. Se encarga de generar, guardar, recuperar y eliminar contraseñas, además de gestionar el cifrado de la bóveda.
- `requirements.txt`: contiene las dependencias externas necesarias para ejecutar el proyecto.
- `README.md`: contiene la documentación del proyecto.
- `.gitignore`: indica qué archivos y carpetas deben excluirse del repositorio de Git.

## ⚙️ Instalación y ejecución

Para utilizar KeyGarden, sigue estos pasos:

**1. Instalar Python**

Descarga e instala Python desde su página oficial:

https://www.python.org/

**2. Descargar el proyecto**

Clona el repositorio desde GitHub:

```bash
git clone https://github.com/nanemoreno19/keygarden.git
```

También puedes descargarlo directamente como archivo ZIP desde GitHub.

**3. Acceder a la carpeta**

```bash
cd KeyGarden
```

**4. Instalar las dependencias**

Ejecuta el siguiente comando para instalar la biblioteca necesaria:

```bash
pip install -r cryptography
```

**5. Ejecutar la aplicación**

Inicia KeyGarden con:

```bash
python main.py
```

Una vez ejecutado el programa, se abrirá la interfaz gráfica y podrás comenzar a generar y gestionar tus contraseñas.

## 🔐 Seguridad y almacenamiento

KeyGarden utiliza cifrado Fernet para proteger la información almacenada en su bóveda local.

Los archivos principales relacionados con el almacenamiento son:

- **`vault.json`:** contiene los datos de la bóveda en formato cifrado.
- **`clave.key`:** almacena la clave necesaria para descifrar la información.

La aplicación utiliza ambos elementos para recuperar las contraseñas cuando se necesitan.

**Recomendaciones importantes:**

- No compartas `clave.key` ni `vault.json`.
- No subas estos archivos a GitHub.
- Mantén copias de seguridad de ambos archivos en un lugar privado y seguro.
- No elimines la clave de cifrado si quieres conservar el acceso a la bóveda.
- Protege el acceso al equipo donde se almacenan estos archivos.

**Importante:** el cifrado de la bóveda no sustituye la seguridad del dispositivo. Si una persona consigue tanto el archivo `vault.json` como la clave `clave.key`, podría acceder a la información almacenada.

## 🎯 Objetivo del proyecto

KeyGarden es un proyecto personal desarrollado con el objetivo de poner en práctica conocimientos de programación en Python, desarrollo de interfaces gráficas, gestión de archivos y fundamentos de criptografía.

Además de ofrecer una utilidad práctica para generar y gestionar contraseñas, el proyecto permite trabajar con diferentes tecnologías y comprender cómo se pueden integrar para desarrollar una aplicación de escritorio funcional.

## 👨‍💻 Autor

Desarrollado como proyecto personal de Python.

**KeyGarden — Cultiva la seguridad de tus contraseñas. 🌱**
