# spellcrafting/calculators/__init__.py
"""
Implementações de calculadoras para determinar propriedades das magias.
"""

# Importações principais para facilitar o acesso
from spellcrafting.calculators.power_calculator import (
    DefaultPowerCalculator,
    LinearPowerCalculator,
    ElementalSynergyPowerCalculator
)
from spellcrafting.calculators.level_calculator import (
    DefaultLevelCalculator,
    ProgressiveLevelCalculator,
    ElementalBalanceLevelCalculator
)
from spellcrafting.calculators.scaling_calculator import (
    DefaultScalingCalculator,
    EnhancedScalingCalculator,
    ElementalSpecialistScalingCalculator
)

# Define as classes que serão exportadas com `from spellcrafting.calculators import *`
__all__ = [
    'DefaultPowerCalculator',
    'LinearPowerCalculator',
    'ElementalSynergyPowerCalculator',
    'DefaultLevelCalculator',
    'ProgressiveLevelCalculator',
    'ElementalBalanceLevelCalculator',
    'DefaultScalingCalculator',
    'EnhancedScalingCalculator',
    'ElementalSpecialistScalingCalculator'
]