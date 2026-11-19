
"""
===============================================================================
KEYGARDEN - ARCHIVO PRINCIPAL
Archivo: main.py

Este es el archivo que inicia la aplicación.

Su trabajo es:
1. Crear la ventana principal.
2. Cargar la interfaz gráfica.
3. Mantener el programa abierto mientras se utiliza.

Para iniciar KeyGarden, solo hay que ejecutar este archivo.
===============================================================================
"""

# Importamos tkinter para poder crear la ventana principal.
import tkinter as tk

# Importamos la clase que contiene toda la interfaz de KeyGarden.
from interfaz import InterfazGenerador


def iniciar_aplicacion():
    """
    Función que pone en marcha todo el programa.
    """

    # Creamos la ventana principal.
    ventana = tk.Tk()

    # Construimos la interfaz dentro de esa ventana.
    # Aquí se crean los botones, campos de texto y tabla.
    aplicacion = InterfazGenerador(ventana)

    # Mantenemos la ventana abierta.
    # Este bucle permite que el programa responda a los clics y al teclado.
    ventana.mainloop()


# Esta condición significa que el programa se inicia cuando ejecutamos
# directamente el archivo main.py.
if __name__ == "__main__":
    iniciar_aplicacion()
