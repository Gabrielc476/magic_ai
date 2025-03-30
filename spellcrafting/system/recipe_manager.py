# spellcrafting/system/recipe_manager.py
"""
Gerenciador de receitas para o sistema de crafting de magia.
Implementa o padrão Repository para armazenar e gerenciar receitas de magia.
"""
from typing import List, Dict, Any, Optional, Set
from collections import defaultdict

from spellcrafting.utils.observers import Subject


class RecipeManager(Subject):
    """
    Gerenciador de receitas para o sistema de crafting.
    Armazena e gerencia receitas de magia, permitindo consultas eficientes.
    """

    def __init__(self):
        """Inicializa o gerenciador de receitas."""
        super().__init__()
        self._recipes: Dict[str, Dict[str, Any]] = {}
        self._component_index: Dict[str, Set[str]] = defaultdict(set)
        self._effect_index: Dict[str, Set[str]] = defaultdict(set)

    def register_recipe(self, recipe_name: str, component_names: List[str], effect_name: str) -> None:
        """
        Registra uma nova receita de magia.

        Args:
            recipe_name: Nome único da receita
            component_names: Lista de nomes de componentes necessários
            effect_name: Nome do efeito produzido

        Raises:
            ValueError: Se o nome da receita já estiver em uso
        """
        if recipe_name in self._recipes:
            raise ValueError(f"Receita '{recipe_name}' já existe")

        # Registra a receita
        self._recipes[recipe_name] = {
            "name": recipe_name,
            "components": component_names,
            "effect": effect_name
        }

        # Atualiza os índices
        for component_name in component_names:
            self._component_index[component_name].add(recipe_name)

        self._effect_index[effect_name].add(recipe_name)

        # Notifica os observadores
        self.notify("recipe_registered", {
            "name": recipe_name,
            "components": component_names,
            "effect": effect_name
        })

    def get_recipe(self, recipe_name: str) -> Optional[Dict[str, Any]]:
        """
        Obtém uma receita pelo nome.

        Args:
            recipe_name: Nome da receita

        Returns:
            A receita, ou None se não encontrada
        """
        return self._recipes.get(recipe_name)

    def find_recipes_by_component(self, component_name: str) -> List[Dict[str, Any]]:
        """
        Encontra todas as receitas que usam um determinado componente.

        Args:
            component_name: Nome do componente

        Returns:
            Lista de receitas que usam o componente
        """
        recipe_names = self._component_index.get(component_name, set())
        return [self._recipes[name] for name in recipe_names]

    def find_recipes_by_effect(self, effect_name: str) -> List[Dict[str, Any]]:
        """
        Encontra todas as receitas que produzem um determinado efeito.

        Args:
            effect_name: Nome do efeito

        Returns:
            Lista de receitas que produzem o efeito
        """
        recipe_names = self._effect_index.get(effect_name, set())
        return [self._recipes[name] for name in recipe_names]

    def find_recipes_by_components(self, component_names: List[str], exact_match: bool = False) -> List[Dict[str, Any]]:
        """
        Encontra receitas que usam os componentes especificados.

        Args:
            component_names: Lista de nomes de componentes
            exact_match: Se True, encontra apenas receitas que usam exatamente os componentes especificados
                        Se False, encontra receitas para as quais os componentes são suficientes

        Returns:
            Lista de receitas que correspondem aos critérios
        """
        component_set = set(component_names)
        matching_recipes = []

        for recipe_name, recipe in self._recipes.items():
            recipe_components = set(recipe["components"])

            # Verifica correspondência
            if exact_match:
                if recipe_components == component_set:
                    matching_recipes.append(recipe)
            else:
                if recipe_components.issubset(component_set):
                    matching_recipes.append(recipe)

        return matching_recipes

    def get_all_recipes(self) -> List[Dict[str, Any]]:
        """
        Obtém todas as receitas registradas.

        Returns:
            Lista de todas as receitas
        """
        return list(self._recipes.values())

    def remove_recipe(self, recipe_name: str) -> bool:
        """
        Remove uma receita do gerenciador.

        Args:
            recipe_name: Nome da receita a ser removida

        Returns:
            True se a receita foi removida, False se não existia
        """
        if recipe_name not in self._recipes:
            return False

        recipe = self._recipes[recipe_name]

        # Remove dos índices
        for component_name in recipe["components"]:
            self._component_index[component_name].discard(recipe_name)

        self._effect_index[recipe["effect"]].discard(recipe_name)

        # Remove a receita
        del self._recipes[recipe_name]

        # Notifica os observadores
        self.notify("recipe_removed", recipe_name)

        return True

    def clear_recipes(self) -> None:
        """Remove todas as receitas."""
        self._recipes.clear()
        self._component_index.clear()
        self._effect_index.clear()
        self.notify("recipes_cleared", None)