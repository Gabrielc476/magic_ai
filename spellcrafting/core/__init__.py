# spellcrafting/core/__init__.py
"""
Módulo central com as interfaces e classes base do sistema de crafting.
"""

# Importações principais para facilitar o acesso
from spellcrafting.core.interfaces import (
    MagicalComponentInterface,
    MagicalEffectInterface,
    SpellInterface,
    PowerCalculatorInterface,
    LevelCalculatorInterface,
    ElementDominanceCalculatorInterface,
    ScalingCalculatorInterface,
    CombinationRuleInterface,
    CraftingSystemInterface,  # Adicionando a interface que faltava
    ObserverInterface,        # Outras interfaces importantes
    SubjectInterface          # Outras interfaces importantes
)
from spellcrafting.core.component import MagicalComponent
from spellcrafting.core.effect import MagicalEffect
from spellcrafting.core.spell import Spell

# Define as classes que serão exportadas com `from spellcrafting.core import *`
__all__ = [
    'MagicalComponentInterface',
    'MagicalEffectInterface',
    'SpellInterface',
    'PowerCalculatorInterface',
    'LevelCalculatorInterface',
    'ElementDominanceCalculatorInterface',
    'ScalingCalculatorInterface',
    'CombinationRuleInterface',
    'CraftingSystemInterface',  # Adicionado à lista de exportações
    'ObserverInterface',        # Adicionado à lista de exportações
    'SubjectInterface',         # Adicionado à lista de exportações
    'MagicalComponent',
    'MagicalEffect',
    'Spell'
]