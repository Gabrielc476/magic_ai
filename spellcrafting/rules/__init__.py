# spellcrafting/rules/__init__.py
"""
Implementações de regras de combinação para o sistema de crafting.
"""

# Importações principais para facilitar o acesso
from spellcrafting.rules.combination_rules import (
    ElementalCombinationRule,
    ExplosionRule,
    HealingRule,
    ShieldRule,
    DualityRule,
    ElementalStormRule,
    fire_tornado_rule
)

# Define as classes que serão exportadas com `from spellcrafting.rules import *`
__all__ = [
    'ElementalCombinationRule',
    'ExplosionRule',
    'HealingRule',
    'ShieldRule',
    'DualityRule',
    'ElementalStormRule',
    'fire_tornado_rule'
]