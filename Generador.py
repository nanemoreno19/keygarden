
"""
===============================================================================
KEYGARDEN - GENERADOR Y ALMACENAMIENTO DE CONTRASEÑAS
Archivo: Generador.py

Este archivo se ocupa de la parte interna de KeyGarden.

Sus tareas son:
1. Generar contraseñas aleatorias.
2. Crear una clave de cifrado automáticamente.
3. Guardar las contraseñas cifradas en vault.json.
4. Leer y descifrar las contraseñas cuando sea necesario.
5. Guardar nuevas contraseñas.
6. Eliminar contraseñas.
7. Mantener la clave de cifrado durante el uso del programa.

IMPORTANTE:
- No se necesita una contraseña maestra.
- La clave de cifrado se guarda en el archivo clave.key.
- Las contraseñas se guardan cifradas en vault.json.
- Para poder leer la bóveda se necesitan los dos archivos.
===============================================================================
"""

# os permite realizar operaciones con archivos y carpetas.
import os

# json permite guardar y leer información organizada.
import json

# secrets permite generar caracteres aleatorios de forma segura.
import secrets

# string contiene letras y números preparados para utilizar.
import string

# Path permite localizar los archivos en la carpeta de este programa.
from pathlib import Path

# Fernet es la herramienta que cifra y descifra las contraseñas.
from cryptography.fernet import Fernet, InvalidToken


class GeneradorContrasenas:
    """
    Esta clase reúne todas las funciones relacionadas con las contraseñas.

    Una clase es como una caja de herramientas: contiene diferentes funciones
    que trabajan juntas para realizar una tarea.
    """

    def __init__(self):
        """
        Se ejecuta automáticamente cuando se crea el generador.
        """

        # Averiguamos dónde está guardado este archivo Generador.py.
        # Así evitamos que KeyGarden busque los archivos en otra carpeta
        # dependiendo de cómo se haya abierto el programa.
        carpeta_programa = Path(__file__).resolve().parent

        # Ruta completa del archivo que contiene las contraseñas cifradas.
        self.archivo_boveda = carpeta_programa / "vault.json"

        # Ruta completa del archivo que contiene la clave de cifrado.
        self.archivo_clave = carpeta_programa / "clave.key"

        # Aquí guardaremos temporalmente la herramienta de cifrado.
        # Al principio todavía no está cargada.
        self.cifrador = None

        # Preparamos la clave y la bóveda.
        self.preparar_boveda()

    # -------------------------------------------------------------------------
    # 1. PREPARAR LA BÓVEDA Y LA CLAVE
    # -------------------------------------------------------------------------

    def preparar_boveda(self):
        """
        Comprueba si existen los archivos necesarios y prepara la bóveda.

        Hay cuatro situaciones posibles:

        1. No existe ningún archivo:
           Se crea una clave nueva y una bóveda vacía.

        2. Existe la clave, pero no la bóveda:
           Se utiliza la clave existente y se crea una bóveda vacía.

        3. Existe la bóveda, pero no la clave:
           Se muestra un error. No se crea una clave nueva porque no serviría
           para descifrar las contraseñas anteriores.

        4. Existen los dos archivos:
           Se carga la clave y se comprueba que puede abrir la bóveda.
        """

        existe_clave = self.archivo_clave.exists()
        existe_boveda = self.archivo_boveda.exists()

        # CASO 1: todavía no existe ningún archivo.
        if not existe_clave and not existe_boveda:

            # Generamos una clave aleatoria.
            clave = Fernet.generate_key()

            # Guardamos la clave en el archivo clave.key.
            with open(self.archivo_clave, "wb") as archivo:
                archivo.write(clave)

            # Creamos el objeto que utilizará esa clave.
            self.cifrador = Fernet(clave)

            # Creamos una bóveda vacía.
            self.guardar_datos([])

        # CASO 2: existe la clave, pero todavía no existe la bóveda.
        elif existe_clave and not existe_boveda:

            # Leemos la clave que ya estaba guardada.
            with open(self.archivo_clave, "rb") as archivo:
                clave = archivo.read()

            # Cargamos la clave.
            self.cifrador = Fernet(clave)

            # Creamos una bóveda vacía utilizando esa misma clave.
            self.guardar_datos([])

        # CASO 3: existe la bóveda, pero falta la clave.
        elif not existe_clave and existe_boveda:

            # No generamos una clave nueva.
            # Una clave nueva no permitiría recuperar los datos antiguos.
            raise FileNotFoundError(
                "Existe vault.json, pero falta clave.key. "
                "No se ha creado una clave nueva para evitar perder "
                "el acceso a las contraseñas anteriores."
            )

        # CASO 4: existen los dos archivos.
        else:

            # Leemos la clave guardada.
            with open(self.archivo_clave, "rb") as archivo:
                clave = archivo.read()

            try:
                # Comprobamos que la clave tiene un formato válido.
                self.cifrador = Fernet(clave)

                # Intentamos leer la bóveda para comprobar que la clave
                # realmente corresponde a ese archivo.
                self.leer_contrasenas()

            except (InvalidToken, ValueError, TypeError) as error:

                # Si la clave no sirve para abrir la bóveda, avisamos.
                self.cifrador = None

                raise ValueError(
                    "No se puede descifrar la bóveda. "
                    "Comprueba que clave.key y vault.json pertenecen "
                    "a la misma instalación de KeyGarden."
                ) from error

    # -------------------------------------------------------------------------
    # 2. GUARDAR LOS DATOS CIFRADOS EN EL ARCHIVO
    # -------------------------------------------------------------------------

    def guardar_datos(self, contrasenas):
        """
        Recibe una lista de contraseñas, la cifra y la guarda en vault.json.

        El archivo no contendrá las contraseñas directamente legibles.
        """

        # Comprobamos que el cifrador esté preparado.
        if self.cifrador is None:
            raise PermissionError("No se ha podido cargar la clave de cifrado.")

        # Convertimos la lista de contraseñas en un texto JSON.
        texto = json.dumps(
            contrasenas,
            ensure_ascii=False
        )

        # Convertimos el texto en bytes, que es el formato que necesita Fernet.
        contenido = texto.encode("utf-8")

        # Ciframos toda la información.
        contenido_cifrado = self.cifrador.encrypt(contenido)

        # Preparamos el contenido que tendrá el archivo.
        datos_archivo = {
            "datos": contenido_cifrado.decode("utf-8")
        }

        # Guardamos primero en un archivo temporal.
        archivo_temporal = str(self.archivo_boveda) + ".tmp"

        try:
            with open(archivo_temporal, "w", encoding="utf-8") as archivo:
                json.dump(datos_archivo, archivo, indent=4)

            # Sustituimos el archivo anterior por el nuevo.
            os.replace(archivo_temporal, self.archivo_boveda)

        except Exception:

            # Si ocurre un error, intentamos eliminar el archivo temporal.
            if os.path.exists(archivo_temporal):
                os.remove(archivo_temporal)

            # Volvemos a comunicar el error.
            raise

    # -------------------------------------------------------------------------
    # 3. LEER Y DESCIFRAR LAS CONTRASEÑAS
    # -------------------------------------------------------------------------

    def leer_contrasenas(self):
        """
        Lee vault.json y devuelve las contraseñas descifradas.

        Este proceso ocurre automáticamente cuando KeyGarden necesita mostrar
        la lista de contraseñas o trabajar con ella.
        """

        if self.cifrador is None:
            raise PermissionError("No hay una clave de cifrado disponible.")

        # Abrimos el archivo de la bóveda.
        with open(self.archivo_boveda, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        # Recuperamos el contenido cifrado.
        contenido_cifrado = datos["datos"].encode("utf-8")

        # Desciframos el contenido utilizando la clave.
        contenido = self.cifrador.decrypt(contenido_cifrado)

        # Convertimos el texto descifrado en una lista de Python.
        contrasenas = json.loads(contenido.decode("utf-8"))

        # Comprobamos que el contenido sea una lista.
        if not isinstance(contrasenas, list):
            raise ValueError("El contenido de la bóveda no tiene un formato válido.")

        return contrasenas

    # -------------------------------------------------------------------------
    # 4. GENERAR UNA CONTRASEÑA ALEATORIA
    # -------------------------------------------------------------------------

    def generar_contrasena(self, longitud=16):
        """
        Crea una contraseña aleatoria.

        SOLO utiliza:
        - Letras minúsculas: abcdef...
        - Letras mayúsculas: ABCDEF...
        - Números: 0123456789

        No utiliza símbolos como !, #, $, %, &, / o @.

        Además, garantiza que cada contraseña tenga al menos:
        - Una letra minúscula.
        - Una letra mayúscula.
        - Un número.
        """

        # Comprobamos que la longitud esté dentro del intervalo permitido.
        if not 8 <= longitud <= 128:
            raise ValueError(
                "La longitud debe estar entre 8 y 128 caracteres."
            )

        # Grupo de letras minúsculas.
        minusculas = string.ascii_lowercase

        # Grupo de letras mayúsculas.
        mayusculas = string.ascii_uppercase

        # Grupo de números.
        numeros = string.digits

        # Unimos los tres grupos.
        # Estos serán los únicos caracteres permitidos.
        caracteres = minusculas + mayusculas + numeros

        # Elegimos primero un carácter de cada grupo.
        contrasena = [
            secrets.choice(minusculas),
            secrets.choice(mayusculas),
            secrets.choice(numeros)
        ]

        # Completamos el resto de la contraseña con caracteres aleatorios.
        for _ in range(longitud - 3):
            contrasena.append(secrets.choice(caracteres))

        # Mezclamos todos los caracteres para que no aparezcan siempre
        # la minúscula, la mayúscula y el número en las primeras posiciones.
        secrets.SystemRandom().shuffle(contrasena)

        # Unimos los caracteres y devolvemos la contraseña final.
        return "".join(contrasena)

    # -------------------------------------------------------------------------
    # 5. GUARDAR UNA CONTRASEÑA NUEVA
    # -------------------------------------------------------------------------

    def guardar_contrasena(self, sitio, contrasena):
        """
        Añade una contraseña nueva a la bóveda.

        Por ejemplo:
        Sitio: Mi correo
        Contraseña: Abc12345
        """

        # Leemos primero todas las contraseñas existentes.
        contrasenas = self.leer_contrasenas()

        # Creamos un nuevo registro con el sitio y la contraseña.
        nuevo_registro = {
            "sitio": sitio,
            "contrasena": contrasena
        }

        # Añadimos el nuevo registro a la lista.
        contrasenas.append(nuevo_registro)

        # Guardamos toda la lista cifrada.
        self.guardar_datos(contrasenas)

    # -------------------------------------------------------------------------
    # 6. ELIMINAR UNA CONTRASEÑA
    # -------------------------------------------------------------------------

    def eliminar_contrasena(self, indice):
        """
        Elimina una contraseña utilizando su posición en la lista.

        El índice indica qué registro queremos eliminar:
        - 0 significa el primero.
        - 1 significa el segundo.
        - 2 significa el tercero.

        Después de eliminarlo, guardamos la bóveda actualizada.
        """

        # Recuperamos la lista actual.
        contrasenas = self.leer_contrasenas()

        # Comprobamos que el número de registro exista.
        if not 0 <= indice < len(contrasenas):
            return False

        # Eliminamos el registro seleccionado.
        del contrasenas[indice]

        # Guardamos la lista sin el registro eliminado.
        self.guardar_datos(contrasenas)

        return True

    # -------------------------------------------------------------------------
    # 7. CERRAR EL ACCESO A LA CLAVE
    # -------------------------------------------------------------------------

    def bloquear(self):
        """
        Elimina de la memoria del programa el objeto de cifrado.

        No borra los archivos ni las contraseñas.
        """

        self.cifrador = None
