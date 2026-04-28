def build_dashboard_blocks():
    """
    Builds the block content for the Master Dashboard.
    """
    return [
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": "🏛️ Hummus Hub Master Dashboard"}}]
            }
        },
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "rich_text": [{"type": "text", "text": {"content": "Bienvenido al centro de mando de Hummus. Aquí puedes navegar hacia los espacios de equipo y ver la salud general de la agencia."}}],
                "icon": {"emoji": "🚀"},
                "color": "blue_background"
            }
        },
        {"object": "block", "type": "divider", "divider": {}},
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "👥 Espacios de Equipo"}}]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": "Selecciona un equipo para ver sus tareas y clientes asignados."}}]
            }
        },
        # These will be populated with sub-page links during setup_dashboard.py
        {"object": "block", "type": "divider", "divider": {}},
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "🛠️ Administración y Datos"}}]
            }
        },
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "rich_text": [{"type": "text", "text": {"content": "Acceso restringido a Owners (Cami & Yae). Aquí se gestionan las bases de datos maestras."}}],
                "icon": {"emoji": "🔐"},
                "color": "red_background"
            }
        }
    ]

def build_team_page_blocks(team_name: str):
    """
    Builds the block content for a specific team page.
    """
    return [
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": f"⚡ Workspace: {team_name}"}}]
            }
        },
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "rich_text": [{"type": "text", "text": {"content": f"Espacio de trabajo para {team_name}. Aquí encontrarán sus tareas pendientes y el acceso directo a sus clientes."}}],
                "icon": {"emoji": "🔥"},
                "color": "orange_background"
            }
        },
        {"object": "block", "type": "divider", "divider": {}},
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "📋 Tareas del Equipo (Board View)"}}]
            }
        },
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "rich_text": [
                    {"type": "text", "text": {"content": "💡 Instrucción para Setup:\n", "link": None}, "annotations": {"bold": True}},
                    {"type": "text", "text": {"content": "1. Haz clic en '+' para añadir una vista.\n2. Selecciona 'Board'.\n3. Filtra por 'Assigned To' contiene tu nombre.\n4. Agrupa por 'Status'."}}
                ],
                "icon": {"emoji": "ℹ️"},
                "color": "gray_background"
            }
        },
        {"object": "block", "type": "divider", "divider": {}},
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "📂 Clientes Asignados"}}]
            }
        }
    ]

def build_client_second_brain_blocks(data: dict):
    """
    Builds the block content for a client's Second Brain page with a Premium look.
    """
    blocks = [
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": "🧠 Second Brain: " + data.get("name", "")}}]
            }
        },
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "rich_text": [{"type": "text", "text": {"content": "Esta es la central de inteligencia estratégica. Todo lo que aquí se edite actualizará la base de datos para que los Agentes de IA generen contenido alineado."}}],
                "icon": {"emoji": "💡"},
                "color": "blue_background"
            }
        },
        {"object": "block", "type": "divider", "divider": {}},
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "🎯 Pilares Estratégicos"}}]
            }
        }
    ]

    # Strategic Pillars using premium callouts
    pillars = [
        ("✨ Propuesta de Valor", "value_prop", "No definida todavía. Es el 'por qué' nos eligen.", "gray_background"),
        ("🎯 Público Objetivo", "target_audience", "No definido. ¿A quién le hablamos?", "gray_background"),
        ("📢 Tono de Voz", "brand_voice", "No definido. ¿Cómo suena la marca?", "gray_background"),
        ("🏷️ Rubro / Industria", "industry", "No definido.", "gray_background")
    ]

    for title, key, placeholder, color in pillars:
        blocks.append({
            "object": "block",
            "type": "callout",
            "callout": {
                "rich_text": [
                    {"type": "text", "text": {"content": f"{title}\n", "link": None}, "annotations": {"bold": True}},
                    {"type": "text", "text": {"content": data.get(key) or placeholder, "link": None}}
                ],
                "icon": {"emoji": title.split()[0]},
                "color": color
            }
        })

    blocks.extend([
        {"object": "block", "type": "divider", "divider": {}},
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "✅ Guía de Estilo (DOs)"}}]
            }
        }
    ])
    
    # Add DOs
    dos = data.get("dos", []) or ["Seguir el manual de marca", "Usar emojis acordes", "Mantener la estética"]
    for do in dos:
        blocks.append({
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": do}}]
            }
        })
            
    blocks.append({
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "rich_text": [{"type": "text", "text": {"content": "❌ Restricciones (DONTs)"}}]
        }
    })

    # Add DONTs
    donts = data.get("donts", []) or ["No usar tipografías no oficiales", "Evitar lenguaje demasiado formal", "No publicar sin review"]
    for dont in donts:
        blocks.append({
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": dont}}]
            }
        })

    blocks.extend([
        {"object": "block", "type": "divider", "divider": {}},
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "📂 Assets Visuales y Briefing"}}]
            }
        },
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "rich_text": [
                    {"type": "text", "text": {"content": "📖 Manual de Marca: ", "link": None}, "annotations": {"bold": True}},
                    {"type": "text", "text": {"content": "Abrir archivo", "link": {"url": data.get("brand_manual_url")}}} if data.get("brand_manual_url") else {"type": "text", "text": {"content": "Pendiente de carga"}}
                ],
                "icon": {"emoji": "🎨"},
                "color": "yellow_background"
            }
        },
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "rich_text": [
                    {"type": "text", "text": {"content": "📝 Briefing Inicial: ", "link": None}, "annotations": {"bold": True}},
                    {"type": "text", "text": {"content": "Abrir archivo", "link": {"url": data.get("briefing_url")}}} if data.get("briefing_url") else {"type": "text", "text": {"content": "Pendiente de carga"}}
                ],
                "icon": {"emoji": "📄"},
                "color": "yellow_background"
            }
        },
        {"object": "block", "type": "divider", "divider": {}},
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "🔐 Configuración Técnica (Admin Only)"}}]
            }
        },
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "rich_text": [
                    {"type": "text", "text": {"content": "⚙️ Client ID (Supabase): ", "link": None}, "annotations": {"bold": True}},
                    {"type": "text", "text": {"content": data.get("id", "N/A"), "link": None}, "annotations": {"code": True}}
                ],
                "icon": {"emoji": "🛠️"},
                "color": "red_background"
            }
        }
    ])

    return blocks


