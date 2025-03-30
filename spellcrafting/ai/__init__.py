# spellcrafting/ai/__init__.py
"""
Componentes de IA para o sistema de crafting de magias.
"""

# Importações principais para facilitar o acesso
from spellcrafting.ai.ai_manager import AIManager
from spellcrafting.ai.recommendation_engine import ComponentRecommendationEngine
from spellcrafting.ai.effect_predictor import EffectPredictor, ElementalAffinityPredictor
from spellcrafting.ai.name_generator import SpellNameGenerator
from spellcrafting.ai.vector_converter import VectorConverter

# Define as classes que serão exportadas com `from spellcrafting.ai import *`
__all__ = [
    'AIManager',
    'ComponentRecommendationEngine',
    'EffectPredictor',
    'ElementalAffinityPredictor',
    'SpellNameGenerator',
    'VectorConverter'
]