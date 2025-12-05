"""
Módulo de Transcripción de Audio con Whisper API
=================================================

Este módulo proporciona una interfaz gráfica (GUI) para transcribir archivos de audio
a texto utilizando la API de Whisper de OpenAI. Incluye funcionalidades adicionales
como visualización de datos RAW y encriptación de texto.

Características principales:
    - Transcripción de audio a texto con Whisper API
    - Soporte para múltiples formatos de audio (MP3, WAV, M4A, OGG)
    - Visualización automática de datos RAW del archivo de audio
    - Encriptación de texto con Fernet (cryptography)
    - Interfaz gráfica moderna con tema oscuro y 3 secciones
    - Procesamiento asíncrono para no bloquear la UI

Requisitos:
    - Python 3.7+
    - openai
    - python-dotenv
    - cryptography
    - tkinter (incluido en Python)

Configuración:
    Crear un archivo .env en el directorio raíz con:
    OPENAI_API_KEY=tu_clave_api_aqui

Autor: Jesus Diaz
Fecha: 12/04/2025
Versión: 2.0.0
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from openai import OpenAI
import threading

# =============================
#   CARGAR API KEY DESDE .env
# =============================

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    raise Exception("No se encontró la API KEY en .env")

client = OpenAI(api_key=API_KEY)
"""OpenAI: Cliente configurado para interactuar con la API de OpenAI."""

# =============================
#   VARIABLES GLOBALES
# =============================

selected_file = None
"""str: Ruta del archivo de audio seleccionado actualmente. None si no hay archivo."""


# =============================
#   FUNCIÓN PARA ENCRIPTAR TEXTO
# =============================

def encrypt_text(text):
    """
    Encripta un texto utilizando el algoritmo Fernet (AES-128).
    
    Esta función genera una clave de encriptación única cada vez que se ejecuta
    y utiliza esa clave para encriptar el texto proporcionado. La clave NO se
    devuelve ni se almacena, por lo que el texto encriptado no puede ser
    desencriptado posteriormente (encriptación de un solo uso).
    
    Args:
        text (str): Texto plano que se desea encriptar.
    
    Returns:
        str: Texto encriptado en formato base64 como string.
    
    Example:
        >>> texto_original = "Hola mundo"
        >>> texto_encriptado = encrypt_text(texto_original)
        >>> print(texto_encriptado)
        'gAAAAABh...'
    
    Note:
        La clave de encriptación se genera aleatoriamente y se descarta después
        de la encriptación, lo que hace imposible recuperar el texto original.
        Esto es por diseño de seguridad.
    
    Warning:
        No utilizar esta función para datos que necesiten ser desencriptados
        posteriormente, ya que la clave se pierde.
    """
    key = Fernet.generate_key()  
    f = Fernet(key)
    encrypted = f.encrypt(text.encode())
    return encrypted.decode()


# =============================
#   FUNCIONES DE LA APLICACIÓN
# =============================

def seleccionar_archivo():
    """
    Abre un diálogo para seleccionar un archivo de audio y muestra su contenido RAW.
    
    Permite al usuario seleccionar archivos con extensiones de audio comunes,
    actualiza la variable global selected_file con la ruta del archivo elegido
    y automáticamente carga y muestra el contenido RAW del archivo en el primer
    cuadro de texto.
    
    Formatos soportados:
        - MP3 (.mp3)
        - WAV (.wav)
        - M4A (.m4a)
        - OGG (.ogg)
    
    Globals:
        selected_file (str): Se actualiza con la ruta del archivo seleccionado.
        text_raw (tk.Text): Se actualiza con el contenido RAW del archivo.
    
    Returns:
        None
    
    Side Effects:
        - Actualiza la variable global selected_file
        - Lee el archivo del disco
        - Muestra el contenido RAW en text_raw automáticamente
        - Muestra un messagebox con la confirmación
    
    Example:
        >>> seleccionar_archivo()
        # Abre diálogo de selección de archivo
        # Si se selecciona: selected_file = "/ruta/al/audio.mp3"
        # Y muestra el contenido RAW automáticamente
    """
    global selected_file
    file = filedialog.askopenfilename(
        title="Seleccionar audio",
        filetypes=[("Audio files", "*.mp3 *.wav *.m4a *.ogg")]
    )
    if file:
        selected_file = file
        
        # Cargar y mostrar RAW automáticamente
        with open(selected_file, "rb") as f:
            raw = f.read()
        
        # Convertir bytes a string mostrando caracteres RAW (primeros 3000 bytes)
        raw_text = raw[:3000].decode('latin-1')
        
        text_raw.delete("1.0", tk.END)
        text_raw.insert(tk.END, raw_text)
        
        messagebox.showinfo("Archivo cargado", f"Archivo cargado:\n{file}\n\nVista RAW mostrada arriba.")


def transcribir():
    """
    Transcribe el archivo de audio seleccionado a texto usando Whisper API.
    
    Esta función ejecuta la transcripción en un hilo separado para evitar
    bloquear la interfaz gráfica. Utiliza el modelo gpt-4o-transcribe de OpenAI
    para realizar la conversión de audio a texto y muestra el resultado en el
    cuadro de texto de transcripción.
    
    Proceso:
        1. Valida que haya un archivo seleccionado
        2. Inicia la barra de progreso
        3. Envía el archivo a la API de Whisper
        4. Muestra el resultado en text_transcripcion
        5. Detiene la barra de progreso
    
    Globals:
        selected_file (str): Ruta del archivo de audio a transcribir.
        progress (ttk.Progressbar): Barra de progreso de la interfaz.
        text_transcripcion (tk.Text): Cuadro donde se muestra la transcripción.
    
    Returns:
        None
    
    Raises:
        messagebox.showerror: Si no hay archivo seleccionado o si ocurre un error
                             durante la transcripción.
    
    Side Effects:
        - Lee el archivo de audio del disco
        - Realiza una llamada a la API de OpenAI (consume créditos)
        - Actualiza el contenido de text_transcripcion
        - Inicia/detiene la barra de progreso
        - Crea un hilo de ejecución separado
    
    Example:
        >>> transcribir()
        # Después de procesar:
        # text_transcripcion muestra: "Este es el texto transcrito del audio..."
    
    Note:
        - La transcripción se ejecuta de forma asíncrona
        - Requiere conexión a internet
        - El tiempo de procesamiento depende del tamaño del archivo
        - Consume créditos de la API de OpenAI
    
    API Reference:
        Utiliza: client.audio.transcriptions.create()
        Modelo: gpt-4o-transcribe
    """
    if not selected_file:
        return messagebox.showerror("Error", "Seleccione un archivo de audio primero")

    def run():
        """
        Función interna que ejecuta la transcripción en un hilo separado.
        
        Esta función se ejecuta en segundo plano para no bloquear la UI principal.
        """
        progress.start()

        try:
            with open(selected_file, "rb") as audio:
                result = client.audio.transcriptions.create(
                    model="gpt-4o-transcribe",
                    file=audio
                )

            text_transcripcion.delete("1.0", tk.END)
            text_transcripcion.insert(tk.END, result.text)

        except Exception as e:
            messagebox.showerror("Error", str(e))

        progress.stop()

    thread = threading.Thread(target=run)
    thread.start()


def encriptar():
    """
    Encripta el contenido del cuadro de texto de transcripción.
    
    Toma el texto transcrito del cuadro text_transcripcion, lo encripta
    usando el algoritmo Fernet y muestra el resultado en el cuadro de
    texto de encriptación. La clave de encriptación NO se muestra ni se almacena.
    
    Globals:
        text_transcripcion (tk.Text): Cuadro con el texto a encriptar.
        text_encriptado (tk.Text): Cuadro donde se muestra el resultado.
    
    Returns:
        None
    
    Raises:
        messagebox.showerror: Si el cuadro de transcripción está vacío.
    
    Side Effects:
        - Lee el contenido de text_transcripcion
        - Actualiza text_encriptado con el texto encriptado
    
    Example:
        >>> # text_transcripcion contiene: "Hola mundo"
        >>> encriptar()
        # text_encriptado ahora muestra: "gAAAAABh..."
    
    Warning:
        El texto encriptado NO puede ser desencriptado porque la clave
        se descarta inmediatamente después de la encriptación.
    
    See Also:
        encrypt_text(): Función que realiza la encriptación real.
    """
    contenido = text_transcripcion.get("1.0", tk.END).strip()

    if not contenido:
        return messagebox.showerror("Error", "No hay texto transcrito para encriptar")

    encrypted = encrypt_text(contenido)

    text_encriptado.delete("1.0", tk.END)
    text_encriptado.insert(tk.END, encrypted)


# =============================
#   CONFIGURACIÓN DE LA GUI
# =============================

# Ventana principal
window = tk.Tk()
window.title("Transcriptor de Audio - Whisper API")

# Configuración de tamaño: 60% ancho x 80% alto de la pantalla
screen_w = window.winfo_screenwidth()
screen_h = window.winfo_screenheight()

window_w = int(screen_w * 0.6)
window_h = int(screen_h * 0.8)
window.geometry(f"{window_w}x{window_h}")

window.configure(bg="#121212")  # Tema oscuro

# =============================
#   ESTILOS (TEMA OSCURO)
# =============================

style = ttk.Style()
style.theme_use("clam")

# Configuración de estilos para tema oscuro
style.configure("TFrame", background="#1e1e1e")
style.configure("TLabel", background="#1e1e1e", foreground="white", font=("Comic Sans MS", 10))
style.configure("Header.TLabel", background="#1e1e1e", foreground="#00d9ff", font=("Comic Sans MS", 12, "bold"))
style.configure("TButton", background="#2d2d2d", foreground="white", font=("Comic Sans MS", 10))
style.configure("TProgressbar", troughcolor="#2d2d2d", background="#007bff")

# =============================
#   LAYOUT DE LA INTERFAZ
# =============================

# Frame principal con scroll
main_frame = ttk.Frame(window)
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Canvas para scroll
canvas = tk.Canvas(main_frame, bg="#1e1e1e", highlightthickness=0)
scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# =============================
#   TÍTULO PRINCIPAL
# =============================

title = ttk.Label(scrollable_frame, text="🎤 Transcriptor de Audio a Texto",
                  font=("Comic Sans MS", 20, "bold"), foreground="#00d9ff")
title.pack(pady=15)

# =============================
#   BOTÓN SELECCIONAR ARCHIVO
# =============================

btn_seleccionar = ttk.Button(scrollable_frame, text="📂 Seleccionar Archivo de Audio", 
                              command=seleccionar_archivo)
btn_seleccionar.pack(pady=10)

# =============================
#   SECCIÓN 1: VISTA RAW
# =============================

frame_raw = ttk.Frame(scrollable_frame)
frame_raw.pack(fill="both", expand=True, pady=10, padx=20)

label_raw = ttk.Label(frame_raw, text="📄 VISTA RAW DEL ARCHIVO", style="Header.TLabel")
label_raw.pack(anchor="w", pady=(0, 5))

text_raw = tk.Text(frame_raw, height=8, wrap="word",
                   bg="#181818", fg="#00ff00",
                   insertbackground="white",
                   font=("Courier New", 9))
text_raw.pack(fill="both", expand=True)
"""tk.Text: Cuadro de texto que muestra el contenido RAW del archivo de audio."""

# =============================
#   SECCIÓN 2: TRANSCRIPCIÓN
# =============================

frame_transcripcion = ttk.Frame(scrollable_frame)
frame_transcripcion.pack(fill="both", expand=True, pady=10, padx=20)

label_transcripcion = ttk.Label(frame_transcripcion, text="✨ TRANSCRIPCIÓN", style="Header.TLabel")
label_transcripcion.pack(anchor="w", pady=(0, 5))

btn_transcribir = ttk.Button(frame_transcripcion, text="🎯 Transcribir Audio", 
                              command=transcribir)
btn_transcribir.pack(pady=5)

# Barra de progreso
progress = ttk.Progressbar(frame_transcripcion, length=300, mode="indeterminate")
progress.pack(pady=5)
"""ttk.Progressbar: Barra de progreso que se activa durante la transcripción."""

text_transcripcion = tk.Text(frame_transcripcion, height=8, wrap="word",
                             bg="#181818", fg="white",
                             insertbackground="white",
                             font=("Comic Sans MS", 10))
text_transcripcion.pack(fill="both", expand=True, pady=(5, 0))
"""tk.Text: Cuadro de texto donde se muestra la transcripción del audio."""

# =============================
#   SECCIÓN 3: ENCRIPTACIÓN
# =============================

frame_encriptado = ttk.Frame(scrollable_frame)
frame_encriptado.pack(fill="both", expand=True, pady=10, padx=20)

label_encriptado = ttk.Label(frame_encriptado, text="🔐 TEXTO ENCRIPTADO", style="Header.TLabel")
label_encriptado.pack(anchor="w", pady=(0, 5))

btn_encriptar = ttk.Button(frame_encriptado, text="🔒 Encriptar Transcripción", 
                            command=encriptar)
btn_encriptar.pack(pady=5)

text_encriptado = tk.Text(frame_encriptado, height=8, wrap="word",
                          bg="#181818", fg="#ff6b6b",
                          insertbackground="white",
                          font=("Courier New", 9))
text_encriptado.pack(fill="both", expand=True, pady=(5, 0))
"""tk.Text: Cuadro de texto donde se muestra el texto encriptado."""

# Nota de seguridad
nota_encriptado = ttk.Label(frame_encriptado, 
                            text="⚠️ La clave de encriptación NO se guarda (seguridad de un solo uso)",
                            foreground="#ff9800", font=("Comic Sans MS", 8))
nota_encriptado.pack(pady=5)

# =============================
#   INICIAR APLICACIÓN
# =============================

if __name__ == "__main__":
    """
    Punto de entrada principal de la aplicación.
    
    Inicia el bucle principal de eventos de tkinter, que mantiene
    la ventana abierta y responde a las interacciones del usuario.
    """
    window.mainloop()