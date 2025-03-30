# spellcrafting/system/__init__.py
"""
Módulo que contém os principais sistemas e gerenciadores do sistema de crafting.
"""

# Importações principais para facilitar o acesso
from spellcrafting.system.spellcrafting_system import SpellcraftingSystem
from spellcrafting.system.crafting_system import CraftingSystem
from spellcrafting.system.element_manager import ElementManager, Element
from spellcrafting.system.recipe_manager import RecipeManager
from spellcrafting.system.persistence_manager import PersistenceManager

# Define as classes que serão exportadas com `from spellcrafting.system import *`
__all__ = [
    'SpellcraftingSystem',
    'CraftingSystem',
    'ElementManager',
    'Element',
    'RecipeManager',
    'PersistenceManager'
]