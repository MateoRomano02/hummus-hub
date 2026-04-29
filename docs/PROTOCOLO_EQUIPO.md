# 📋 Protocolo de Sincronización: Hummus Hub

Este documento explica cómo usar la base de datos de Clientes en Notion para que la información esté siempre lista para la IA.

## 🚀 Cómo Cargar un Cliente Nuevo

1.  **Crear Fila**: Agrega una nueva fila en la base de datos de Clientes.
2.  **Usar Plantilla**: Haz clic en el botón "Nuevo Cliente" dentro de la página para cargar la estructura recomendada.
3.  **Completar Campos Críticos**: Para que la IA pueda trabajar, **estos campos son obligatorios**:
    *   **Name**: Nombre comercial de la marca.
    *   **📋 Rubro**: Selecciona el sector.
    *   **🗣️ Tono de Voz**: Describe cómo habla la marca.
    *   **🎯 Público Objetivo**: Quién es el cliente ideal.
    *   **✨ Propuesta de Valor**: Qué los hace únicos.
4.  **Sincronizar**: Una vez que termines de cargar todo, cambia la columna **🔄 Estado de Sync** a `Pendiente`.

## ⚖️ El "Juez" de Validación

Nuestro sistema revisará automáticamente los datos. Observa la columna **🔄 Estado de Sync**:

*   **✅ Sincronizado**: ¡Todo listo! La IA ya conoce a este cliente y puede trabajar con él.
*   **❌ Error**: Algo salió mal. Revisa la columna **📝 Notas del Sistema** para ver qué falta o qué corregir.
*   **⌛ Last Sync**: Indica cuándo fue la última vez que el "cerebro" (Supabase) recibió una actualización de esta fila.

## ⚠️ Reglas de Oro (Para no romper nada)

1.  **No cambies el nombre de las columnas**: El sistema las busca por su nombre exacto (incluyendo los emojis). Si necesitas renombrar algo, avísanos para actualizar el "Schema Guardian".
2.  **ID de Supabase**: No toques la columna `🆔 Supabase ID`. Es el ancla que une Notion con nuestra base de datos.
3.  **Links**: Asegúrate de que los links de Drive o Manuales de Marca empiecen con `https://`.

---
*Cualquier duda o error persistente, contactar con el soporte técnico de Hummus Hub.*
