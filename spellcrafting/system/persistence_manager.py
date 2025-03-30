# spellcrafting/system/persistence_manager.py
"""
Sistema de persistência para salvar e carregar dados do sistema de crafting.
"""
from typing import List, Dict, Any, Optional
import json
import os
from spellcrafting.core import MagicalComponentInterface, MagicalEffectInterface, SpellInterface
from spellcrafting.factories import ComponentFactory, EffectFactory


class PersistenceManager:
    """
    Gerenciador de persistência para salvar e carregar componentes, efeitos e magias.
    """

    def __init__(self, data_directory: str = "data"):
        """
        Inicializa o gerenciador de persistência.

        Args:
            data_directory: Diretório onde os dados serão salvos
        """
        self._data_directory = data_directory
        self._component_factory = ComponentFactory()
        self._effect_factory = EffectFactory()

        # Cria o diretório de dados se não existir
        os.makedirs(self._data_directory, exist_ok=True)

    def save_components(self, components: List[MagicalComponentInterface], file_name: str = "components.json") -> bool:
        """
        Salva uma lista de componentes em um arquivo JSON.

        Args:
            components: Lista de componentes a serem salvos
            file_name: Nome do arquivo

        Returns:
            True se salvou com sucesso, False caso contrário
        """
        file_path = os.path.join(self._data_directory, file_name)

        try:
            component_data = [component.to_dict() for component in components]

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(component_data, f, indent=4, ensure_ascii=False)

            return True
        except Exception as e:
            print(f"Erro ao salvar componentes: {e}")
            return False

    def load_components(self, file_name: str = "components.json") -> List[MagicalComponentInterface]:
        """
        Carrega componentes de um arquivo JSON.

        Args:
            file_name: Nome do arquivo

        Returns:
            Lista de componentes carregados
        """
        file_path = os.path.join(self._data_directory, file_name)

        if not os.path.exists(file_path):
            return []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                component_data = json.load(f)

            components = []
            for data in component_data:
                component = self._component_factory.create_component(
                    data["name"],
                    data["element"],
                    data["power"],
                    data["rarity"]
                )
                components.append(component)

            return components
        except Exception as e:
            print(f"Erro ao carregar componentes: {e}")
            return []

    def save_effects(self, effects: List[MagicalEffectInterface], file_name: str = "effects.json") -> bool:
        """
        Salva uma lista de efeitos em um arquivo JSON.

        Args:
            effects: Lista de efeitos a serem salvos
            file_name: Nome do arquivo

        Returns:
            True se salvou com sucesso, False caso contrário
        """
        file_path = os.path.join(self._data_directory, file_name)

        try:
            effect_data = [effect.to_dict() for effect in effects]

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(effect_data, f, indent=4, ensure_ascii=False)

            return True
        except Exception as e:
            print(f"Erro ao salvar efeitos: {e}")
            return False

    def load_effects(self, file_name: str = "effects.json") -> List[MagicalEffectInterface]:
        """
        Carrega efeitos de um arquivo JSON.

        Args:
            file_name: Nome do arquivo

        Returns:
            Lista de efeitos carregados
        """
        file_path = os.path.join(self._data_directory, file_name)

        if not os.path.exists(file_path):
            return []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                effect_data = json.load(f)

            effects = []
            for data in effect_data:
                effect = self._effect_factory.create_effect(
                    data["name"],
                    data["description"],
                    data["base_power"]
                )
                effects.append(effect)

            return effects
        except Exception as e:
            print(f"Erro ao carregar efeitos: {e}")
            return []

    def save_recipes(self, recipes: Dict[str, Dict[str, Any]], file_name: str = "recipes.json") -> bool:
        """
        Salva receitas em um arquivo JSON.

        Args:
            recipes: Dicionário de receitas a serem salvas
            file_name: Nome do arquivo

        Returns:
            True se salvou com sucesso, False caso contrário
        """
        file_path = os.path.join(self._data_directory, file_name)

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(recipes, f, indent=4, ensure_ascii=False)

            return True
        except Exception as e:
            print(f"Erro ao salvar receitas: {e}")
            return False

    def load_recipes(self, file_name: str = "recipes.json") -> Dict[str, Dict[str, Any]]:
        """
        Carrega receitas de um arquivo JSON.

        Args:
            file_name: Nome do arquivo

        Returns:
            Dicionário de receitas carregadas
        """
        file_path = os.path.join(self._data_directory, file_name)

        if not os.path.exists(file_path):
            return {}

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Erro ao carregar receitas: {e}")
            return {}

    def save_spell(self, spell: SpellInterface, file_name: Optional[str] = None) -> bool:
        """
        Salva uma magia em um arquivo JSON.

        Args:
            spell: Magia a ser salva
            file_name: Nome do arquivo (usa o nome da magia se não especificado)

        Returns:
            True se salvou com sucesso, False caso contrário
        """
        if file_name is None:
            # Cria um nome de arquivo baseado no nome da magia
            safe_name = spell.name.lower().replace(" ", "_").replace("/", "_")
            file_name = f"spell_{safe_name}.json"

        file_path = os.path.join(self._data_directory, file_name)

        try:
            spell_data = spell.to_dict()

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(spell_data, f, indent=4, ensure_ascii=False)

            return True
        except Exception as e:
            print(f"Erro ao salvar magia: {e}")
            return False