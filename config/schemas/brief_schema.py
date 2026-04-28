from pydantic import BaseModel, Field
from typing import Optional, List

class BriefSchema(BaseModel):
    # Identidad
    client_name:         str
    industry:            str
    country:             str = 'AR'

    # Contacto
    email:               Optional[str] = None
    whatsapp:            Optional[str] = None
    website:             Optional[str] = None
    instagram:           Optional[str] = None

    # Perfil de marca — campos críticos para los agentes
    brand_voice:         str   # Cómo habla la marca
    five_brand_words:    List[str]   # 5 palabras que definen la marca
    communication_objectives: List[str]   # mínimo 3
    target_audience:     str   # a quién le habla
    target_opportunity:  Optional[str] = None   # target potencial
    value_proposition:   str   # qué la diferencia
    competitors:         List[str] = []

    # Reglas de contenido — las más consultadas por agentes
    dos:                 List[str] = []
    donts:               List[str] = []

    # Estética
    brand_colors:        List[str] = []   # hex
    fonts:               List[str] = []
    has_brand_manual:    bool = False
    brand_manual_url:    Optional[str] = None
    aesthetic_references: List[str] = []
    content_references:  List[str] = []

    # Operacional
    stories_frequency:   Optional[str] = None
    posts_per_week:      int = 3
    most_important_event: Optional[str] = None
    client_expectations: Optional[str] = None

    # Extra — cualquier campo que no encaje arriba
    extra:               dict = {}
