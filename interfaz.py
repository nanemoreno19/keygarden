
"""
===============================================================================
KEYGARDEN - INTERFAZ GRÁFICA
Archivo: interfaz.py

Este archivo crea la parte visual de KeyGarden.

Aquí se encuentran:
- La ventana principal.
- El generador de contraseñas.
- El campo para introducir el nombre de una página o servicio.
- El campo para guardar una contraseña.
- La tabla de contraseñas guardadas.
- Los botones para mostrar, ocultar, copiar y eliminar.

No se solicita ninguna contraseña maestra.
El cifrado y descifrado se realizan automáticamente.
===============================================================================
"""

# tkinter es la herramienta que permite crear ventanas y botones.
import tkinter as tk

# ttk proporciona elementos gráficos como tablas y barras de desplazamiento.
from tkinter import ttk

# messagebox permite mostrar avisos, errores y preguntas de confirmación.
from tkinter import messagebox

# Importamos nuestro generador y gestor de contraseñas.
from Generador import GeneradorContrasenas

# Importamos los errores que pueden aparecer al descifrar información.
from cryptography.fernet import InvalidToken


class InterfazGenerador:
    """
    Esta clase crea y controla toda la ventana de KeyGarden.
    """

    def __init__(self, ventana):
        """
        Prepara la ventana y construye todos sus elementos.
        """

        # Guardamos la ventana principal.
        self.ventana = ventana

        # Creamos el objeto que administra las contraseñas.
        self.generador = None

        # Aquí guardaremos la contraseña que se acaba de generar.
        self.contrasena_actual = ""

        # Indica si la contraseña generada está visible.
        self.mostrar_password = False

        # Guarda el estado de visibilidad de cada contraseña de la tabla.
        self.contrasenas_visibles = {}

        # Indica si ha ocurrido un error al cargar la bóveda.
        self.boveda_disponible = False

        # Definimos los colores de KeyGarden.
        self.color_fondo = "#F5F3FF"
        self.color_morado = "#6C4AB6"
        self.color_morado_oscuro = "#4B2E83"
        self.color_verde = "#A8D5BA"
        self.color_blanco = "#FFFFFF"
        self.color_texto = "#30264A"
        self.color_gris = "#E9E5F2"

        # Configuramos el título y el tamaño de la ventana.
        self.ventana.title("KeyGarden - Gestor de contraseñas")
        self.ventana.geometry("900x720")
        self.ventana.minsize(750, 620)
        self.ventana.configure(bg=self.color_fondo)

        # Esta función se ejecutará cuando se pulse la X de la ventana.
        self.ventana.protocol(
            "WM_DELETE_WINDOW",
            self.cerrar_aplicacion
        )

        # Configuramos el aspecto de las tablas.
        self.configurar_estilos()

        # Construimos los elementos de la ventana.
        self.crear_interfaz()

        # Intentamos cargar la bóveda automáticamente.
        self.cargar_boveda()

    # -------------------------------------------------------------------------
    # 1. CONFIGURAR LOS ESTILOS
    # -------------------------------------------------------------------------

    def configurar_estilos(self):
        """
        Establece los colores y las fuentes de la tabla.
        """

        estilo = ttk.Style()

        # Utilizamos un tema que permite personalizar los colores.
        estilo.theme_use("clam")

        # Aspecto general de las filas de la tabla.
        estilo.configure(
            "Treeview",
            background=self.color_blanco,
            foreground=self.color_texto,
            fieldbackground=self.color_blanco,
            rowheight=32,
            font=("Arial", 10)
        )

        # Aspecto de los títulos de las columnas.
        estilo.configure(
            "Treeview.Heading",
            background=self.color_morado,
            foreground=self.color_blanco,
            font=("Arial", 10, "bold")
        )

        # Aspecto de una fila cuando está seleccionada.
        estilo.map(
            "Treeview",
            background=[("selected", self.color_verde)],
            foreground=[("selected", self.color_texto)]
        )

    # -------------------------------------------------------------------------
    # 2. CREAR TODA LA INTERFAZ
    # -------------------------------------------------------------------------

    def crear_interfaz(self):
        """
        Coloca las diferentes secciones dentro de la ventana principal.
        """

        # Este marco sirve para agrupar todos los elementos.
        self.contenedor = tk.Frame(
            self.ventana,
            bg=self.color_fondo
        )

        self.contenedor.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=20
        )

        # Creamos las diferentes partes de la aplicación.
        self.crear_cabecera()
        self.crear_estado()
        self.crear_generador()
        self.crear_guardado()
        self.crear_tabla()
        self.crear_pie()

    # -------------------------------------------------------------------------
    # 3. CABECERA DE LA APLICACIÓN
    # -------------------------------------------------------------------------

    def crear_cabecera(self):
        """
        Muestra el nombre de la aplicación y una descripción.
        """

        cabecera = tk.Frame(
            self.contenedor,
            bg=self.color_fondo
        )

        cabecera.pack(
            fill="x",
            pady=(0, 15)
        )

        # Nombre de la aplicación.
        tk.Label(
            cabecera,
            text="KeyGarden",
            font=("Arial", 26, "bold"),
            bg=self.color_fondo,
            fg=self.color_morado_oscuro
        ).pack(anchor="w")

        # Pequeña explicación de para qué sirve el programa.
        tk.Label(
            cabecera,
            text="Tu espacio seguro para crear y guardar contraseñas",
            font=("Arial", 11),
            bg=self.color_fondo,
            fg=self.color_texto
        ).pack(anchor="w", pady=(2, 0))

    # -------------------------------------------------------------------------
    # 4. ESTADO DE LA BÓVEDA
    # -------------------------------------------------------------------------

    def crear_estado(self):
        """
        Muestra si KeyGarden ha podido cargar correctamente la bóveda.

        Ya no hay botón de desbloqueo ni contraseña maestra.
        """

        marco = tk.Frame(
            self.contenedor,
            bg=self.color_blanco,
            highlightbackground=self.color_verde,
            highlightthickness=1
        )

        marco.pack(
            fill="x",
            pady=(0, 15)
        )

        self.etiqueta_estado = tk.Label(
            marco,
            text="Preparando bóveda...",
            font=("Arial", 10, "bold"),
            bg=self.color_blanco,
            fg=self.color_morado_oscuro,
            padx=12,
            pady=10
        )

        self.etiqueta_estado.pack(side="left")

    # -------------------------------------------------------------------------
    # 5. ZONA DEL GENERADOR DE CONTRASEÑAS
    # -------------------------------------------------------------------------

    def crear_generador(self):
        """
        Crea los campos y botones necesarios para generar contraseñas.
        """

        marco = tk.LabelFrame(
            self.contenedor,
            text=" Generar contraseña ",
            font=("Arial", 11, "bold"),
            bg=self.color_blanco,
            fg=self.color_morado_oscuro,
            padx=15,
            pady=12
        )

        marco.pack(
            fill="x",
            pady=(0, 15)
        )

        # Fila que contiene la longitud y el botón de generar.
        fila = tk.Frame(
            marco,
            bg=self.color_blanco
        )

        fila.pack(fill="x")

        tk.Label(
            fila,
            text="Longitud:",
            font=("Arial", 10),
            bg=self.color_blanco,
            fg=self.color_texto
        ).pack(side="left")

        # Campo donde se escribe el número de caracteres.
        self.entrada_longitud = tk.Entry(
            fila,
            width=8,
            font=("Arial", 10),
            justify="center",
            relief="solid",
            bd=1
        )

        # Por defecto, las contraseñas tendrán 16 caracteres.
        self.entrada_longitud.insert(0, "16")

        self.entrada_longitud.pack(
            side="left",
            padx=10
        )

        # Botón que genera una contraseña nueva.
        self.boton_generar = tk.Button(
            fila,
            text="Generar contraseña",
            command=self.generar_contrasena,
            bg=self.color_morado,
            fg=self.color_blanco,
            activebackground=self.color_morado_oscuro,
            activeforeground=self.color_blanco,
            font=("Arial", 9, "bold"),
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=7
        )

        self.boton_generar.pack(
            side="left",
            padx=5
        )

        # Campo donde se muestra la contraseña generada.
        self.etiqueta_contrasena = tk.Entry(
            marco,
            font=("Consolas", 12),
            justify="center",
            relief="solid",
            bd=1,
            state="readonly"
        )

        self.etiqueta_contrasena.pack(
            fill="x",
            pady=(12, 8)
        )

        # Fila que contiene los botones Mostrar y Copiar.
        fila_botones = tk.Frame(
            marco,
            bg=self.color_blanco
        )

        fila_botones.pack(fill="x")

        self.boton_mostrar = tk.Button(
            fila_botones,
            text="Mostrar",
            command=self.alternar_visibilidad,
            bg=self.color_verde,
            fg=self.color_texto,
            activebackground="#8CC5A3",
            font=("Arial", 9, "bold"),
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=6
        )

        self.boton_mostrar.pack(side="left")

        self.boton_copiar = tk.Button(
            fila_botones,
            text="Copiar",
            command=self.copiar_contrasena,
            bg=self.color_morado,
            fg=self.color_blanco,
            activebackground=self.color_morado_oscuro,
            activeforeground=self.color_blanco,
            font=("Arial", 9, "bold"),
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=6
        )

        self.boton_copiar.pack(
            side="left",
            padx=8
        )

    # -------------------------------------------------------------------------
    # 6. ZONA PARA GUARDAR CONTRASEÑAS
    # -------------------------------------------------------------------------

    def crear_guardado(self):
        """
        Crea los campos donde se introducen el sitio y la contraseña.
        """

        marco = tk.LabelFrame(
            self.contenedor,
            text=" Guardar contraseña ",
            font=("Arial", 11, "bold"),
            bg=self.color_blanco,
            fg=self.color_morado_oscuro,
            padx=15,
            pady=12
        )

        marco.pack(
            fill="x",
            pady=(0, 15)
        )

        # Fila del nombre del sitio.
        fila_sitio = tk.Frame(
            marco,
            bg=self.color_blanco
        )

        fila_sitio.pack(
            fill="x",
            pady=4
        )

        tk.Label(
            fila_sitio,
            text="Sitio o servicio:",
            width=17,
            anchor="w",
            font=("Arial", 10),
            bg=self.color_blanco,
            fg=self.color_texto
        ).pack(side="left")

        self.entrada_sitio = tk.Entry(
            fila_sitio,
            font=("Arial", 10),
            relief="solid",
            bd=1
        )

        self.entrada_sitio.pack(
            side="left",
            fill="x",
            expand=True
        )

        # Fila de la contraseña.
        fila_password = tk.Frame(
            marco,
            bg=self.color_blanco
        )

        fila_password.pack(
            fill="x",
            pady=4
        )

        tk.Label(
            fila_password,
            text="Contraseña:",
            width=17,
            anchor="w",
            font=("Arial", 10),
            bg=self.color_blanco,
            fg=self.color_texto
        ).pack(side="left")

        # El parámetro show hace que la contraseña aparezca oculta.
        self.entrada_password = tk.Entry(
            fila_password,
            font=("Arial", 10),
            relief="solid",
            bd=1,
            show="•"
        )

        self.entrada_password.pack(
            side="left",
            fill="x",
            expand=True
        )

        # Botón que guarda los datos introducidos.
        self.boton_guardar = tk.Button(
            marco,
            text="Guardar contraseña",
            command=self.guardar_contrasena,
            bg=self.color_verde,
            fg=self.color_texto,
            activebackground="#8CC5A3",
            font=("Arial", 9, "bold"),
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=7
        )

        self.boton_guardar.pack(
            anchor="e",
            pady=(8, 0)
        )

    # -------------------------------------------------------------------------
    # 7. TABLA DE CONTRASEÑAS GUARDADAS
    # -------------------------------------------------------------------------

    def crear_tabla(self):
        """
        Crea la tabla donde aparecen los sitios y sus contraseñas.
        """

        marco = tk.LabelFrame(
            self.contenedor,
            text=" Contraseñas guardadas ",
            font=("Arial", 11, "bold"),
            bg=self.color_blanco,
            fg=self.color_morado_oscuro,
            padx=12,
            pady=10
        )

        marco.pack(
            fill="both",
            expand=True,
            pady=(0, 15)
        )

        # Definimos las dos columnas de la tabla.
        columnas = ("sitio", "contrasena")

        self.tabla = ttk.Treeview(
            marco,
            columns=columnas,
            show="headings",
            selectmode="browse"
        )

        # Configuramos la primera columna.
        self.tabla.heading(
            "sitio",
            text="Sitio o servicio"
        )

        self.tabla.column(
            "sitio",
            width=250,
            anchor="w"
        )

        # Configuramos la segunda columna.
        self.tabla.heading(
            "contrasena",
            text="Contraseña"
        )

        self.tabla.column(
            "contrasena",
            width=350,
            anchor="center"
        )

        # Creamos una barra para desplazarnos por la tabla.
        barra = ttk.Scrollbar(
            marco,
            orient="vertical",
            command=self.tabla.yview
        )

        self.tabla.configure(
            yscrollcommand=barra.set
        )

        self.tabla.pack(
            side="left",
            fill="both",
            expand=True
        )

        barra.pack(
            side="right",
            fill="y"
        )

        # Fila de botones que aparece debajo de la tabla.
        fila_botones = tk.Frame(
            marco,
            bg=self.color_blanco
        )

        fila_botones.pack(
            side="bottom",
            fill="x",
            pady=(10, 0)
        )

        # Botón para mostrar u ocultar una contraseña seleccionada.
        self.boton_mostrar_seleccionada = tk.Button(
            fila_botones,
            text="Mostrar / ocultar seleccionada",
            command=self.alternar_contrasena_seleccionada,
            bg=self.color_morado,
            fg=self.color_blanco,
            activebackground=self.color_morado_oscuro,
            activeforeground=self.color_blanco,
            font=("Arial", 9, "bold"),
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=6
        )

        self.boton_mostrar_seleccionada.pack(side="left")

        # Botón para eliminar la contraseña seleccionada.
        self.boton_eliminar = tk.Button(
            fila_botones,
            text="Eliminar seleccionada",
            command=self.eliminar_contrasena,
            bg="#E8A0A0",
            fg="#4A2020",
            activebackground="#D98787",
            font=("Arial", 9, "bold"),
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=6
        )

        self.boton_eliminar.pack(side="right")

    # -------------------------------------------------------------------------
    # 8. BOTÓN PARA CERRAR LA APLICACIÓN
    # -------------------------------------------------------------------------

    def crear_pie(self):
        """
        Coloca el botón para cerrar KeyGarden.
        """

        marco = tk.Frame(
            self.contenedor,
            bg=self.color_fondo
        )

        marco.pack(fill="x")

        self.boton_cerrar = tk.Button(
            marco,
            text="Cerrar KeyGarden",
            command=self.cerrar_aplicacion,
            bg=self.color_morado_oscuro,
            fg=self.color_blanco,
            activebackground=self.color_morado,
            activeforeground=self.color_blanco,
            font=("Arial", 9, "bold"),
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=7
        )

        self.boton_cerrar.pack(side="right")

    # -------------------------------------------------------------------------
    # 9. CARGAR LA BÓVEDA AUTOMÁTICAMENTE
    # -------------------------------------------------------------------------

    def cargar_boveda(self):
        """
        Abre la bóveda automáticamente al iniciar KeyGarden.

        No se solicita ninguna contraseña al usuario.
        """

        try:
            # Creamos el gestor de contraseñas.
            # Su inicialización comprueba y prepara los archivos necesarios.
            self.generador = GeneradorContrasenas()

            # Si llegamos aquí, la bóveda se ha podido cargar.
            self.boveda_disponible = True

            self.etiqueta_estado.config(
                text="Bóveda cargada correctamente",
                fg="#287A45"
            )

            # Mostramos los registros guardados.
            self.mostrar_contrasenas()

        except (
            FileNotFoundError,
            InvalidToken,
            ValueError,
            KeyError,
            OSError,
            TypeError
        ) as error:

            # Si ocurre un error, no intentamos crear otra clave
            # ni modificar la bóveda que ya existe.
            self.boveda_disponible = False

            self.etiqueta_estado.config(
                text="No se ha podido cargar la bóveda",
                fg="#B3261E"
            )

            # Desactivamos los botones que necesitan acceder a la bóveda.
            self.boton_guardar.config(state="disabled")
            self.boton_eliminar.config(state="disabled")
            self.boton_mostrar_seleccionada.config(state="disabled")

            messagebox.showerror(
                "Error al cargar",
                "No se han podido mostrar las contraseñas.\n\n"
                f"Detalles: {error}\n\n"
                "No borres vault.json ni clave.key. "
                "Comprueba que ambos archivos están en la misma carpeta."
            )

    # -------------------------------------------------------------------------
    # 10. GENERAR UNA CONTRASEÑA
    # -------------------------------------------------------------------------

    def generar_contrasena(self):
        """
        Lee la longitud elegida y genera una contraseña nueva.
        """

        try:
            # Convertimos el contenido del campo en un número entero.
            longitud = int(self.entrada_longitud.get())

            # Solicitamos al generador una contraseña de esa longitud.
            self.contrasena_actual = self.generador.generar_contrasena(
                longitud
            )

            # Al generar una contraseña nueva, empieza oculta.
            self.mostrar_password = False

            # Actualizamos el campo donde aparece.
            self.actualizar_resultado()

        except ValueError as error:
            messagebox.showerror(
                "Longitud no válida",
                "Introduce un número entero entre 8 y 128.\n\n"
                f"Detalles: {error}"
            )

    # -------------------------------------------------------------------------
    # 11. MOSTRAR LA CONTRASEÑA GENERADA
    # -------------------------------------------------------------------------

    def actualizar_resultado(self):
        """
        Actualiza el campo que muestra la contraseña generada.

        Si está oculta, se muestran puntos.
        Si está visible, se muestran sus caracteres reales.
        """

        if self.mostrar_password:
            texto = self.contrasena_actual
            self.boton_mostrar.config(text="Ocultar")

        else:
            texto = "•" * len(self.contrasena_actual)
            self.boton_mostrar.config(text="Mostrar")

        # Habilitamos temporalmente el campo para modificar su contenido.
        self.etiqueta_contrasena.config(state="normal")

        # Borramos el texto anterior.
        self.etiqueta_contrasena.delete(0, "end")

        # Escribimos la contraseña o los puntos.
        self.etiqueta_contrasena.insert(0, texto)

        # Volvemos a dejar el campo en modo solo lectura.
        self.etiqueta_contrasena.config(state="readonly")

    # -------------------------------------------------------------------------
    # 12. ALTERNAR ENTRE MOSTRAR Y OCULTAR
    # -------------------------------------------------------------------------

    def alternar_visibilidad(self):
        """
        Cambia la contraseña generada de visible a oculta o al revés.
        """

        if not self.contrasena_actual:
            messagebox.showwarning(
                "Sin contraseña",
                "Primero tienes que generar una contraseña."
            )
            return

        # Cambiamos el estado de visibilidad.
        self.mostrar_password = not self.mostrar_password

        # Actualizamos el campo de resultado.
        self.actualizar_resultado()

    # -------------------------------------------------------------------------
    # 13. COPIAR LA CONTRASEÑA GENERADA
    # -------------------------------------------------------------------------

    def copiar_contrasena(self):
        """
        Copia la contraseña generada al portapapeles del ordenador.
        """

        if not self.contrasena_actual:
            messagebox.showwarning(
                "Sin contraseña",
                "Primero tienes que generar una contraseña."
            )
            return

        # Borramos el contenido anterior del portapapeles.
        self.ventana.clipboard_clear()

        # Copiamos la contraseña actual.
        self.ventana.clipboard_append(self.contrasena_actual)

        messagebox.showinfo(
            "Contraseña copiada",
            "La contraseña se ha copiado correctamente."
        )

    # -------------------------------------------------------------------------
    # 14. GUARDAR UNA CONTRASEÑA
    # -------------------------------------------------------------------------

    def guardar_contrasena(self):
        """
        Guarda el sitio y la contraseña que ha escrito el usuario.
        """

        if not self.boveda_disponible:
            messagebox.showerror(
                "Bóveda no disponible",
                "No se puede guardar porque la bóveda no se ha podido cargar."
            )
            return

        # Recuperamos el nombre del sitio.
        sitio = self.entrada_sitio.get().strip()

        # Recuperamos la contraseña.
        contrasena = self.entrada_password.get()

        # Comprobamos que los dos campos estén completos.
        if not sitio or not contrasena:
            messagebox.showwarning(
                "Datos incompletos",
                "Debes escribir el sitio y la contraseña."
            )
            return

        try:
            # Guardamos el registro mediante Generador.py.
            self.generador.guardar_contrasena(
                sitio,
                contrasena
            )

            # Limpiamos los campos para que se puedan introducir otros datos.
            self.entrada_sitio.delete(0, "end")
            self.entrada_password.delete(0, "end")

            # Actualizamos la tabla.
            self.mostrar_contrasenas()

            messagebox.showinfo(
                "Contraseña guardada",
                "La contraseña se ha guardado correctamente."
            )

        except (
            OSError,
            PermissionError,
            InvalidToken,
            ValueError
        ) as error:

            messagebox.showerror(
                "Error al guardar",
                f"No se ha podido guardar la contraseña.\n\n{error}"
            )

    # -------------------------------------------------------------------------
    # 15. MOSTRAR LAS CONTRASEÑAS GUARDADAS EN LA TABLA
    # -------------------------------------------------------------------------

    def mostrar_contrasenas(self):
        """
        Carga las contraseñas guardadas en la tabla.

        Por seguridad, las contraseñas aparecen ocultas inicialmente.
        """

        if not self.boveda_disponible:
            return

        try:
            # Recuperamos los registros descifrados.
            contrasenas = self.generador.leer_contrasenas()

            # Eliminamos las filas antiguas de la tabla.
            for elemento in self.tabla.get_children():
                self.tabla.delete(elemento)

            # Al actualizar la tabla, todas las contraseñas vuelven a ocultarse.
            self.contrasenas_visibles.clear()

            # Recorremos todos los registros.
            for indice, registro in enumerate(contrasenas):

                # Recuperamos el nombre del sitio.
                sitio = registro["sitio"]

                # Recuperamos la contraseña.
                contrasena = registro["contrasena"]

                # Creamos una fila con la contraseña oculta.
                self.tabla.insert(
                    "",
                    "end",
                    iid=str(indice),
                    values=(
                        sitio,
                        "•" * len(contrasena)
                    )
                )

        except (
            OSError,
            ValueError,
            KeyError,
            InvalidToken,
            TypeError
        ) as error:

            messagebox.showerror(
                "Error",
                f"No se pudieron mostrar las contraseñas.\n\n{error}"
            )

    # -------------------------------------------------------------------------
    # 16. MOSTRAR U OCULTAR UNA CONTRASEÑA DE LA TABLA
    # -------------------------------------------------------------------------

    def alternar_contrasena_seleccionada(self):
        """
        Permite ver la contraseña de la fila seleccionada.

        Si estaba oculta, se muestra.
        Si estaba visible, vuelve a ocultarse.
        """

        if not self.boveda_disponible:
            return

        # Comprobamos qué fila ha seleccionado el usuario.
        seleccion = self.tabla.selection()

        if not seleccion:
            messagebox.showwarning(
                "Selecciona una contraseña",
                "Primero debes seleccionar una fila de la tabla."
            )
            return

        # El identificador de la fila representa su posición en la lista.
        indice = int(seleccion[0])

        try:
            # Recuperamos las contraseñas descifradas.
            contrasenas = self.generador.leer_contrasenas()

            if not 0 <= indice < len(contrasenas):
                return

            # Consultamos si la contraseña ya estaba visible.
            visible = self.contrasenas_visibles.get(indice, False)

            # Cambiamos su estado.
            self.contrasenas_visibles[indice] = not visible

            # Recuperamos el registro seleccionado.
            registro = contrasenas[indice]

            # Obtenemos la contraseña real.
            contrasena = registro["contrasena"]

            # Decidimos qué texto debe aparecer en la tabla.
            if self.contrasenas_visibles[indice]:
                texto = contrasena
            else:
                texto = "•" * len(contrasena)

            # Actualizamos la fila seleccionada.
            self.tabla.item(
                str(indice),
                values=(
                    registro["sitio"],
                    texto
                )
            )

            # Mantenemos seleccionada la misma fila.
            self.tabla.selection_set(str(indice))

        except (
            OSError,
            ValueError,
            KeyError,
            InvalidToken
        ) as error:

            messagebox.showerror(
                "Error",
                f"No se pudo mostrar la contraseña.\n\n{error}"
            )

    # -------------------------------------------------------------------------
    # 17. ELIMINAR UNA CONTRASEÑA
    # -------------------------------------------------------------------------

    def eliminar_contrasena(self):
        """
        Elimina permanentemente de la bóveda la contraseña seleccionada.
        """

        if not self.boveda_disponible:
            return

        # Averiguamos qué fila está seleccionada.
        seleccion = self.tabla.selection()

        if not seleccion:
            messagebox.showwarning(
                "Selecciona una contraseña",
                "Primero debes seleccionar una fila de la tabla."
            )
            return

        # Preguntamos si realmente quiere eliminarla.
        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Seguro que quieres eliminar esta contraseña?\n\n"
            "Esta acción no se puede deshacer."
        )

        # Si pulsa No, no hacemos nada.
        if not confirmar:
            return

        # Obtenemos la posición del registro seleccionado.
        indice = int(seleccion[0])

        try:
            # Eliminamos el registro y guardamos la bóveda actualizada.
            eliminada = self.generador.eliminar_contrasena(indice)

            if eliminada:

                # Actualizamos la tabla para que desaparezca el registro.
                self.contrasenas_visibles.clear()
                self.mostrar_contrasenas()

                messagebox.showinfo(
                    "Contraseña eliminada",
                    "La contraseña se ha eliminado correctamente."
                )

            else:
                messagebox.showwarning(
                    "No encontrada",
                    "No se ha encontrado la contraseña seleccionada."
                )

        except (
            OSError,
            PermissionError,
            ValueError,
            InvalidToken
        ) as error:

            messagebox.showerror(
                "Error al eliminar",
                f"No se pudo eliminar la contraseña.\n\n{error}"
            )

    # -------------------------------------------------------------------------
    # 18. CERRAR KEYGARDEN
    # -------------------------------------------------------------------------

    def cerrar_aplicacion(self):
        """
        Cierra el programa y elimina de la memoria la clave de cifrado.

        Los archivos no se borran.
        Las contraseñas siguen guardadas y cifradas.
        """

        # Si el generador se ha creado correctamente, bloqueamos su acceso.
        if self.generador is not None:
            self.generador.bloquear()

        # Cerramos la ventana principal.
        self.ventana.destroy()
