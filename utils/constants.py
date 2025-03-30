# spellcrafting/utils/constants.py
"""
Constantes utilizadas no sistema de crafting de magia.
"""
from typing import Dict, List, Tuple

# Constantes relacionadas a componentes
MIN_COMPONENTS_FOR_SPELL = 3
MAX_COMPONENT_POWER = 10
DEFAULT_COMPONENT_POWER = 5

# Constantes relacionadas a níveis de magia
MAX_SPELL_LEVEL = 9
CANTRIP_LEVEL = 0

# Limiares de nível de magia baseados em pontuação total
SPELL_LEVEL_THRESHOLDS = [
    (10, 0),  # Cantrip
    (15, 1),  # Nível 1
    (25, 2),  # Nível 2
    (35, 3),  # Nível 3
    (50, 4),  # Nível 4
    (65, 5),  # Nível 5
    (80, 6),  # Nível 6
    (100, 7),  # Nível 7
    (125, 8),  # Nível 8
    (float('inf'), 9)  # Nível 9
]

# Descrições de níveis de magia
SPELL_LEVEL_DESCRIPTIONS = {
    0: "Truque (Cantrip)",
    1: "Nível 1 (Básica)",
    2: "Nível 2 (Aprendiz)",
    3: "Nível 3 (Adepto)",
    4: "Nível 4 (Avançada)",
    5: "Nível 5 (Superior)",
    6: "Nível 6 (Arcana)",
    7: "Nível 7 (Arcana Superior)",
    8: "Nível 8 (Mística)",
    9: "Nível 9 (Lendária)"
}

# Multiplicadores de raridade para cálculo de poder
RARITY_MULTIPLIERS = {
    "comum": 1.0,
    "incomum": 1.2,
    "raro": 1.5,
    "épico": 2.0,
    "lendário": 3.0
}

# Pontos por raridade para cálculo de nível
RARITY_POINTS = {
    "comum": 0,
    "incomum": 2,
    "raro": 5,
    "épico": 10,
    "lendário": 20
}

# Elementos principais
PRIMARY_ELEMENTS = ["fogo", "água", "terra", "ar", "luz", "trevas"]

# Combinações elementais poderosas (para cálculo de nível)
POWERFUL_ELEMENT_COMBINATIONS = [
    {"fogo", "ar"},  # Tempestade de fogo
    {"água", "trevas"},  # Magia negra aquática
    {"luz", "ar"},  # Magias celestiais
    {"terra", "fogo"},  # Magias vulcânicas
    {"trevas", "fogo"},  # Magia demoníaca
    {"luz", "trevas"}  # Magias de dualidade (muito raras)
]

# Elementos opostos que se anulam parcialmente
OPPOSING_ELEMENTS = [
    {"fogo", "água"},
    {"terra", "ar"},
    {"luz", "trevas"}
]

# Elementos compatíveis por elemento
ELEMENT_COMPATIBILITIES = {
    "fogo": ["ar", "terra"],
    "água": ["ar", "terra"],
    "terra": ["fogo", "água"],
    "ar": ["fogo", "água"],
    "luz": ["ar", "fogo"],
    "trevas": ["terra", "água"]
}

# Templates de efeitos de escalonamento por elemento
ELEMENT_SCALING_EFFECTS = {
    "fogo": "Dano adicional de {magnitude} de fogo por rodada",
    "água": "Reduz a velocidade do alvo em {magnitude} pés",
    "terra": "Cria terreno difícil num raio de {magnitude} pés",
    "ar": "Empurra alvos até {magnitude} pés",
    "luz": "Cura aliados em {magnitude} pontos de vida",
    "trevas": "Causa condição de cegueira por {magnitude} rodadas"
}

# Palavras-chave associadas a cada elemento (para análise de texto)
ELEMENT_KEYWORDS = {
    "fogo": ["fogo", "flam", "queim", "calor", "incendi", "combustão", "brasas", "ardente"],
    "água": ["água", "gelo", "congel", "aquá", "fluido", "líquido", "marítimo", "oceano"],
    "terra": ["terra", "rocha", "escudo", "proteç", "barreira", "montanha", "pedra", "cristal"],
    "ar": ["ar", "vento", "tempestade", "furacão", "brisa", "céu", "atmosfera", "tornado"],
    "luz": ["luz", "cura", "restau", "iluminaç", "brilho", "radiante", "solar", "divino"],
    "trevas": ["trevas", "escurid", "sombra", "corrupç", "veneno", "negro", "noite", "sombrio"]
}

# Palavras-chave associadas a cada tipo de efeito
EFFECT_KEYWORDS = {
    "dano": ["dano", "ferimento", "destrui", "queima", "congela", "explode", "ataque"],
    "cura": ["cura", "restaura", "recupera", "regenera", "vida", "vitalidade", "saúde"],
    "controle": ["controle", "imobiliza", "prende", "restringe", "paralisa", "domina"],
    "proteção": ["proteção", "escudo", "barreira", "defesa", "armadura", "resiste"],
    "ilusão": ["ilusão", "invisível", "disfarça", "enganar", "falso", "miragem"],
    "invocação": ["invoca", "conjura", "convoca", "chama", "traz", "manifesta"]
}

# Nome de efeitos genéricos por elemento
GENERIC_EFFECT_NAMES = {
    "fogo": "Manifestação de Fogo",
    "água": "Manifestação Aquática",
    "terra": "Manifestação Terrestre",
    "ar": "Manifestação Eólica",
    "luz": "Manifestação Luminosa",
    "trevas": "Manifestação Sombria"
}

# Descrições genéricas de efeitos por elemento
GENERIC_EFFECT_DESCRIPTIONS = {
    "fogo": "Cria uma manifestação flamejante de energia mágica",
    "água": "Invoca uma onda de energia aquática mágica",
    "terra": "Forma uma barreira sólida de energia terrestre",
    "ar": "Libera uma rajada de energia eólica concentrada",
    "luz": "Emite um feixe de energia luminosa purificadora",
    "trevas": "Envolve o alvo em sombras místicas corrosivas"
}


# Requisitos de conjurador por nível
def get_caster_requirement(spell_level: int) -> str:
    """Retorna o requisito de nível de conjurador para um determinado nível de magia."""
    if spell_level == 0:
        return "Qualquer conjurador iniciante pode usar esta magia."

    caster_level = max(1, spell_level * 2 - 1)
    return f"Requer um conjurador de nível {caster_level} ou superior."


# Parâmetros padrão de escalonamento
DEFAULT_BASE_RANGE = 10  # pés
DEFAULT_BASE_DURATION = 1  # rodadas/minutos

# Parâmetros para a IA
DEFAULT_VECTOR_SIZE = 14  # Tamanho do vetor de características para componentes
DEFAULT_ELEMENT_VECTOR_SIZE = 6  # Tamanho do vetor de codificação one-hot para elementos