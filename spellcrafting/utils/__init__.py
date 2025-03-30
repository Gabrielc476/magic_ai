# spellcrafting/utils/__init__.py
"""
Módulo com utilitários, ferramentas e classes auxiliares para o sistema de crafting.
"""

# Importações principais para facilitar o acesso
from spellcrafting.utils.enums import (
    ElementType,
    RarityType,
    SpellLevel,
    EffectType,
    SpellSchool,
    ElementInteraction,
    EventType
)
from spellcrafting.utils.observers import Subject, LoggingObserver, SpellCreationObserver
from spellcrafting.utils.config_manager import ConfigManager
from spellcrafting.utils.enum_converters import (
    EnumConverter,
    ElementConverter,
    RarityConverter,
    EffectTypeConverter,
    SpellLevelConverter
)
from spellcrafting.utils.constants import (
    MIN_COMPONENTS_FOR_SPELL,
    MAX_COMPONENT_POWER,
    SPELL_LEVEL_THRESHOLDS,
    RARITY_MULTIPLIERS
)

# Define as classes que serão exportadas com `from spellcrafting.utils import *`
__all__ = [
    'ElementType',
    'RarityType',
    'SpellLevel',
    'EffectType',
    'SpellSchool',
    'ElementInteraction',
    'EventType',
    'Subject',
    'LoggingObserver',
    'SpellCreationObserver',
    'ConfigManager',
    'EnumConverter',
    'ElementConverter',
    'RarityConverter',
    'EffectTypeConverter',
    'SpellLevelConverter'
]