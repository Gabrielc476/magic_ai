# spellcrafting/core/__init__.py
"""
Módulo central com as interfaces e classes base do sistema de crafting.
"""

# Importações principais para facilitar o acesso
from spellcrafting.core.interfaces import (
    MagicalElement,
    MagicalComponentInterface,
    MagicalEffectInterface,
    SpellInterface,
    PowerCalculatorInterface,
    LevelCalculatorInterface,
    ElementDominanceCalculatorInterface,
    ScalingCalculatorInterface,
    CombinationRuleInterface,
    CraftingSystemInterface,
    ObserverInterface,
    SubjectInterface,
    # Adicionando interfaces de fábrica
    ComponentFactoryInterface,
    EffectFactoryInterface,
    SpellFactoryInterface,
    AIModelInterface
)
from spellcrafting.core.component import MagicalComponent
from spellcrafting.core.effect import MagicalEffect
from spellcrafting.core.spell import Spell

# Define as classes que serão exportadas com `from spellcrafting.core import *`
__all__ = [
    'MagicalElement',
    'MagicalComponentInterface',
    'MagicalEffectInterface',
    'SpellInterface',
    'PowerCalculatorInterface',
    'LevelCalculatorInterface',
    'ElementDominanceCalculatorInterface',
    'ScalingCalculatorInterface',
    'CombinationRuleInterface',
    'CraftingSystemInterface',
    'ObserverInterface',
    'SubjectInterface',
    # Adicionando interfaces de fábrica ao __all__
    'ComponentFactoryInterface',
    'EffectFactoryInterface',
    'SpellFactoryInterface',
    'MagicalComponent',
    'MagicalEffect',
    'Spell',
    'AIModelInterface'
]