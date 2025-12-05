# 🎤 Transcriptor de Audio a Texto

Aplicación de escritorio desarrollada en Python con Tkinter que permite transcribir archivos de audio a texto utilizando la API de Whisper de OpenAI.


##  Características

-  **Transcripción de audio**: Convierte archivos de audio a texto usando Whisper API
-  **Vista RAW**: Visualiza el contenido binario del archivo de audio automáticamente al cargarlo
-  **Encriptación**: Encripta el texto transcrito con algoritmo Fernet (AES-128)
-  **Interfaz moderna**: Tema oscuro con diseño vertical limpio e intuitivo
-  **Procesamiento asíncrono**: No bloquea la interfaz durante la transcripción
-  **Tres secciones independientes**: RAW, Transcripción y Encriptación en una sola vista

##  Capturas de Pantalla

La interfaz muestra tres secciones verticales:
1. **Vista RAW** - Se muestra automáticamente al cargar el archivo
2. **Transcripción** - Con botón y área de resultado
3. **Encriptación** - Para proteger el texto transcrito

## Requisitos

- Python 3.7 o superior
- Cuenta de OpenAI con API Key activa
- Sistema operativo: Windows, macOS o Linux

##  Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/jesusdiazitla-lang/Transcriptor.git
cd Transcriptor
```

### 2. Crear entorno virtual (recomendado)
```bash
python -m venv venv
```

**Activar el entorno:**
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install openai python-dotenv cryptography
```

O usando el archivo de requisitos:
```bash
pip install -r requirements.txt
```

### 4. Configurar API Key

Crear un archivo `.env` en la raíz del proyecto con el siguiente contenido:
```env
OPENAI_API_KEY=tu_clave_api_aqui
```

>  **Importante**: 
> - Obtén tu API Key en: https://platform.openai.com/api-keys
> - Nunca compartas tu API Key públicamente
> - El archivo `.env` está protegido por `.gitignore` y NO se sube al repositorio

##  Uso

### Ejecutar la aplicación
```bash
python transcriptor_gui.py
```

### Flujo de trabajo
1. **Seleccionar archivo**: Haz clic en **"📂 Seleccionar Archivo de Audio"**
2. **Vista RAW automática**: El contenido binario del archivo se muestra inmediatamente
3. **Transcribir**: Haz clic en **"🎯 Transcribir Audio"** y espera el resultado
4. **Encriptar** (opcional): Haz clic en **"🔒 Encriptar Transcripción"** para proteger el texto

##  Estructura del Proyecto

```
Transcriptor/
│
├── transcriptor_gui.py    # Aplicación principal con interfaz gráfica (completo y documentado)
├── .env                    # Configuración de API Key (NO incluido en repo)
├── .gitignore             # Archivos ignorados por Git
├── LICENSE                # Licencia MIT
├── README.md              # Este archivo
└── requirements.txt       # Dependencias del proyecto
```

##  Formatos de Audio Soportados

| Formato | Extensión | Estado |
|---------|-----------|--------|
| MP3 | `.mp3` | ✅ Soportado |
| WAV | `.wav` | ✅ Soportado |
| M4A | `.m4a` | ✅ Soportado |
| OGG | `.ogg` | ✅ Soportado |

##  Tecnologías Utilizadas

| Tecnología | Propósito | Versión |
|------------|-----------|---------|
| **Python** | Lenguaje de programación | 3.7+ |
| **Tkinter** | Interfaz gráfica nativa | Built-in |
| **OpenAI API** | Transcripción de audio con Whisper | Latest |
| **Cryptography** | Encriptación Fernet (AES-128) | 41.0+ |
| **python-dotenv** | Gestión de variables de entorno | 1.0+ |

##  Seguridad

-  La API Key se almacena en archivo `.env` (no versionado en Git)
-  La encriptación utiliza **Fernet (AES-128)** - estándar de la industria
-  La clave de encriptación se genera aleatoriamente para cada operación
-  La clave de encriptación **NO se almacena** (seguridad de un solo uso)
-  El archivo `.gitignore` protege datos sensibles

##  Notas Importantes

### Sobre la API de OpenAI
- La transcripción **consume créditos** de tu cuenta de OpenAI
- Modelo utilizado: `gpt-4o-transcribe`
- Requiere conexión a internet activa
- El tiempo de procesamiento depende del tamaño del archivo

### Sobre la Vista RAW
- Muestra los primeros **3000 bytes** del archivo
- Útil para identificar el formato y estructura del audio
- Los caracteres no imprimibles se muestran como símbolos especiales
- Usa codificación `latin-1` para preservar todos los bytes

### Sobre la Encriptación
- El texto encriptado **NO puede ser desencriptado**
- La clave se descarta inmediatamente después de encriptar
- Diseñado para demostración de seguridad, no para uso en producción
- Para uso real, implementar un sistema de gestión de claves

##  Solución de Problemas

### Error: "No se encontró la API KEY en .env"
**Solución**: Verifica que el archivo `.env` existe y contiene `OPENAI_API_KEY=tu_clave`

### Error durante la transcripción
**Posibles causas**:
- API Key inválida o expirada
- Sin créditos en la cuenta de OpenAI
- Archivo de audio corrupto
- Sin conexión a internet

### La interfaz se congela
**Solución**: Espera a que termine el proceso. La barra de progreso indica que está trabajando.

##  Contribuciones

Las contribuciones son bienvenidas. Para cambios imprtantes:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

##  Autor

**Jesús Díaz**
- GitHub: [@jesusdiazitla-lang](https://github.com/jesusdiazitla-lang)

##  Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.



**Si te ha gustado este proyecto, considera darle una estrella en GitHub **

[Reportar un Bug](https://github.com/jesusdiazitla-lang/Transcriptor/issues) • [Solicitar Feature](https://github.com/jesusdiazitla-lang/Transcriptor/issues)

</div>
