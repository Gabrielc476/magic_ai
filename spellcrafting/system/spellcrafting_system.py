# spellcrafting/system/spellcrafting_system.py
"""
Classe principal que integra todos os componentes do sistema de crafting.
Fornece uma interface unificada para criar e gerenciar magias.
"""
from typing import List, Optional

from spellcrafting.core import (
    MagicalComponentInterface,
    MagicalEffectInterface,
    SpellInterface,
    CombinationRuleInterface
)
from ..system.crafting_system import CraftingSystem
from ..system.element_manager import ElementManager
from ..system.recipe_manager import RecipeManager
from ..system.persistence_manager import PersistenceManager
from spellcrafting.ai import AIManager
from spellcrafting.utils.config_manager import ConfigManager
from spellcrafting.utils.observers import LoggingObserver
from spellcrafting.factories import ComponentFactory, EffectFactory, SpellFactory
from spellcrafting.calculators import DefaultPowerCalculator
from spellcrafting.calculators.level_calculator import DefaultLevelCalculator
from spellcrafting.calculators.scaling_calculator import DefaultScalingCalculator


class SpellcraftingSystem:
    """
    Classe principal que integra todos os componentes do sistema de crafting.
    Fornece uma interface unificada para criar e gerenciar magias.
    """

    def __init__(self, config_file: Optional[str] = None, data_directory: str = "data"):
        """
        Inicializa o sistema de crafting integrado.

        Args:
            config_file: Caminho para o arquivo de configuração (opcional)
            data_directory: Diretório para armazenar dados persistentes
        """
        # Inicializa o gerenciador de configuração
        self._config = ConfigManager(config_file)

        # Inicializa os gerenciadores
        self._element_manager = ElementManager()
        self._recipe_manager = RecipeManager()

        # Inicializa as calculadoras padrão
        self._power_calculator = DefaultPowerCalculator()
        self._level_calculator = DefaultLevelCalculator()
        self._scaling_calculator = DefaultScalingCalculator()

        # Inicializa o sistema de crafting principal
        self._crafting_system = CraftingSystem(
            power_calculator=self._power_calculator,
            level_calculator=self._level_calculator,
            scaling_calculator=self._scaling_calculator,
            recipe_manager=self._recipe_manager,
            element_manager=self._element_manager
        )

        # Inicializa as fábricas
        self._component_factory = ComponentFactory()
        self._effect_factory = EffectFactory()
        self._spell_factory = SpellFactory(
            self._power_calculator,
            self._level_calculator,
            None,  # Usa o padrão do Spell para elemento dominante
            self._scaling_calculator
        )

        # Inicializa o gerenciador de persistência
        self._persistence_manager = PersistenceManager(data_directory)

        # Inicializa o gerenciador de IA
        self._ai_manager = AIManager(self._crafting_system)

        # Configura o sistema de logging
        if self._config.get("logging.enabled", True):
            log_file = self._config.get("logging.log_file", "spellcrafting.log")
            self._logger = LoggingObserver(log_file)
            self._crafting_system.attach(self._logger)
            self._recipe_manager.attach(self._logger)

    def register_component(self, name: str, element: str, power: int, rarity: str) -> MagicalComponentInterface:
        """
        Cria e registra um novo componente mágico.

        Args:
            name: Nome do componente
            element: Elemento do componente
            power: Potência do componente
            rarity: Raridade do componente

        Returns:
            O componente criado
        """
        component = self._component_factory.create_component(name, element, power, rarity)
        self._crafting_system.register_component(component)
        return component

    def register_effect(self, name: str, description: str, base_power: int) -> MagicalEffectInterface:
        """
        Cria e registra um novo efeito mágico.

        Args:
            name: Nome do efeito
            description: Descrição do efeito
            base_power: Poder base do efeito

        Returns:
            O efeito criado
        """
        effect = self._effect_factory.create_effect(name, description, base_power)
        self._crafting_system.register_effect(effect)
        return effect

    def register_recipe(self, recipe_name: str, component_names: List[str], effect_name: str) -> None:
        """
        Registra uma nova receita de magia.

        Args:
            recipe_name: Nome da receita
            component_names: Lista de nomes de componentes necessários
            effect_name: Nome do efeito produzido
        """
        self._crafting_system.register_recipe(recipe_name, component_names, effect_name)

    def add_combination_rule(self, rule: CombinationRuleInterface) -> None:
        """
        Adiciona uma nova regra de combinação.

        Args:
            rule: A regra de combinação a ser adicionada
        """
        self._crafting_system.add_combination_rule(rule)

    def create_spell(self, spell_name: str, component_names: List[str]) -> SpellInterface:
        """
        Cria uma nova magia a partir de componentes.

        Args:
            spell_name: Nome da magia
            component_names: Lista de nomes de componentes

        Returns:
            A magia criada
        """
        return self._crafting_system.create_spell(spell_name, component_names)

    def get_component(self, name: str) -> Optional[MagicalComponentInterface]:
        """
        Obtém um componente pelo nome.

        Args:
            name: Nome do componente

        Returns:
            O componente, ou None se não encontrado
        """
        return self._crafting_system.get_component(name)

    def get_effect(self, name: str) -> Optional[MagicalEffectInterface]:
        """
        Obtém um efeito pelo nome.

        Args:
            name: Nome do efeito

        Returns:
            O efeito, ou None se não encontrado
        """
        return self._crafting_system.get_effect(name)

    def get_all_components(self) -> List[MagicalComponentInterface]:
        """
        Obtém todos os componentes registrados.

        Returns:
            Lista de todos os componentes
        """
        return list(self._crafting_system.registered_components.values())

    def get_all_effects(self) -> List[MagicalEffectInterface]:
        """
        Obtém todos os efeitos registrados.

        Returns:
            Lista de todos os efeitos
        """
        return list(self._crafting_system.registered_effects.values())

    def get_components_by_element(self, element: str) -> List[MagicalComponentInterface]:
        """
        Obtém todos os componentes de um determinado elemento.

        Args:
            element: Nome do elemento

        Returns:
            Lista de componentes do elemento especificado
        """
        return self._crafting_system.get_components_by_element(element)

    def get_compatible_elements(self, element: str) -> List[str]:
        """
        Obtém os elementos compatíveis com um determinado elemento.

        Args:
            element: Nome do elemento

        Returns:
            Lista de elementos compatíveis
        """
        return self._element_manager.get_compatible_elements(element)

    def recommend_components(self, components: List[MagicalComponentInterface], count: int = 3) -> List[
        MagicalComponentInterface]:
        """
        Recomenda componentes adicionais compatíveis.

        Args:
            components: Lista atual de componentes
            count: Número de recomendações a retornar

        Returns:
            Lista de componentes recomendados
        """
        return self._ai_manager.get_component_recommendations(components, count)

    def predict_effect(self, components: List[MagicalComponentInterface]) -> MagicalEffectInterface:
        """
        Prevê o efeito mais provável para uma combinação de componentes.

        Args:
            components: Lista de componentes

        Returns:
            Efeito mágico previsto
        """
        return self._ai_manager.predict_effect(components)

    def generate_spell_name(
            self,
            components: List[MagicalComponentInterface],
            effect: Optional[MagicalEffectInterface] = None
    ) -> str:
        """
        Gera um nome para uma magia.

        Args:
            components: Lista de componentes
            effect: Efeito da magia (opcional)

        Returns:
            Nome gerado para a magia
        """
        return self._ai_manager.generate_spell_name(components, effect)[0]

    def save_all_data(self) -> bool:
        """
        Salva todos os dados do sistema.

        Returns:
            True se todos os dados foram salvos com sucesso, False caso contrário
        """
        components = self.get_all_components()
        effects = self.get_all_effects()
        recipes = self._recipe_manager.get_all_recipes()

        recipes_dict = {recipe["name"]: recipe for recipe in recipes}

        components_saved = self._persistence_manager.save_components(components)
        effects_saved = self._persistence_manager.save_effects(effects)
        recipes_saved = self._persistence_manager.save_recipes(recipes_dict)

        return components_saved and effects_saved and recipes_saved

    def load_all_data(self) -> bool:
        """
        Carrega todos os dados salvos.

        Returns:
            True se todos os dados foram carregados com sucesso, False caso contrário
        """
        try:
            # Carrega componentes
            components = self._persistence_manager.load_components()
            for component in components:
                self._crafting_system.register_component(component)

            # Carrega efeitos
            effects = self._persistence_manager.load_effects()
            for effect in effects:
                self._crafting_system.register_effect(effect)

            # Carrega receitas
            recipes = self._persistence_manager.load_recipes()
            for recipe_name, recipe in recipes.items():
                self._crafting_system.register_recipe(
                    recipe_name,
                    recipe["components"],
                    recipe["effect"]
                )

            return True
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
            return False

    def save_spell(self, spell: SpellInterface) -> bool:
        """
        Salva uma magia em um arquivo.

        Args:
            spell: A magia a ser salva

        Returns:
            True se a magia foi salva com sucesso, False caso contrário
        """
        return self._persistence_manager.save_spell(spell)

    def train_ai_models(self) -> bool:
        """
        Treina todos os modelos de IA.

        Returns:
            True se todos os modelos foram treinados com sucesso, False caso contrário
        """
        return self._ai_manager.train_all_models()