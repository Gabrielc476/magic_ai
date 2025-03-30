# spellcrafting/system/crafting_system.py
"""
Sistema principal de crafting de magias, atualizado para eliminar duplicação.
"""
from typing import List, Dict, Any, Optional, Tuple
from collections import Counter

from spellcrafting.core import (
    CraftingSystemInterface,
    MagicalComponentInterface,
    MagicalEffectInterface,
    SpellInterface,
    CombinationRuleInterface,
    PowerCalculatorInterface,
    LevelCalculatorInterface,
    ElementDominanceCalculatorInterface,
    ScalingCalculatorInterface,
    ObserverInterface
)
from spellcrafting.core import MagicalEffect
from spellcrafting.utils.observers import Subject
from ..system.element_manager import ElementManager
from ..system.recipe_manager import RecipeManager


class CraftingSystem(CraftingSystemInterface, Subject, ObserverInterface):
    """
    Sistema de crafting que gerencia componentes, efeitos, receitas
    e criação de magias. Integrado com ElementManager e RecipeManager.
    """

    def __init__(
            self,
            power_calculator: Optional[PowerCalculatorInterface] = None,
            level_calculator: Optional[LevelCalculatorInterface] = None,
            element_calculator: Optional[ElementDominanceCalculatorInterface] = None,
            scaling_calculator: Optional[ScalingCalculatorInterface] = None,
            recipe_manager: Optional[RecipeManager] = None,
            element_manager: Optional[ElementManager] = None
    ):
        """
        Inicializa o sistema de crafting.

        Args:
            power_calculator: Calculadora de poder das magias
            level_calculator: Calculadora de nível das magias
            element_calculator: Calculadora de elemento dominante
            scaling_calculator: Calculadora de escalonamento
            recipe_manager: Gerenciador de receitas
            element_manager: Gerenciador de elementos
        """
        # Inicializa a classe base Subject para o padrão Observer
        Subject.__init__(self)

        # Armazéns de dados
        self._registered_components: Dict[str, MagicalComponentInterface] = {}
        self._registered_effects: Dict[str, MagicalEffectInterface] = {}
        self._combination_rules: List[CombinationRuleInterface] = []
        self._spell_history: List[Tuple[List[MagicalComponentInterface], MagicalEffectInterface]] = []

        # Gerenciadores
        self._recipe_manager = recipe_manager or RecipeManager()
        self._element_manager = element_manager or ElementManager()

        # Registra este sistema como observador do gerenciador de receitas
        self._recipe_manager.attach(self)

        # Calculadoras de estratégia
        self._power_calculator = power_calculator
        self._level_calculator = level_calculator
        self._element_calculator = element_calculator
        self._scaling_calculator = scaling_calculator

    @property
    def registered_components(self) -> Dict[str, MagicalComponentInterface]:
        """Retorna um dicionário com os componentes registrados."""
        return self._registered_components.copy()

    @property
    def registered_effects(self) -> Dict[str, MagicalEffectInterface]:
        """Retorna um dicionário com os efeitos registrados."""
        return self._registered_effects.copy()

    @property
    def spell_history(self) -> List[Tuple[List[MagicalComponentInterface], MagicalEffectInterface]]:
        """Retorna o histórico de magias criadas."""
        return self._spell_history.copy()

    def register_component(self, component: MagicalComponentInterface) -> None:
        """
        Registra um componente no sistema.

        Args:
            component: O componente a ser registrado
        """
        self._registered_components[component.name] = component
        self.notify("component_registered", component)

    def register_effect(self, effect: MagicalEffectInterface) -> None:
        """
        Registra um efeito no sistema.

        Args:
            effect: O efeito a ser registrado
        """
        self._registered_effects[effect.name] = effect
        self.notify("effect_registered", effect)

    def register_recipe(self, recipe_name: str, component_names: List[str], effect_name: str) -> None:
        """
        Registra uma receita de magia, delegando ao RecipeManager.

        Args:
            recipe_name: Nome da receita
            component_names: Lista de nomes de componentes necessários
            effect_name: Nome do efeito produzido
        """
        # Verifica se os componentes estão registrados
        for name in component_names:
            if name not in self._registered_components:
                raise ValueError(f"Componente '{name}' não está registrado")

        # Verifica se o efeito está registrado
        if effect_name not in self._registered_effects:
            raise ValueError(f"Efeito '{effect_name}' não está registrado")

        # Delega ao gerenciador de receitas
        self._recipe_manager.register_recipe(recipe_name, component_names, effect_name)

    def add_combination_rule(self, rule: CombinationRuleInterface) -> None:
        """
        Adiciona uma regra de combinação ao sistema.

        Args:
            rule: A regra de combinação a ser adicionada
        """
        self._combination_rules.append(rule)
        self.notify("rule_added", rule)

    def create_spell(self, spell_name: str, component_names: List[str]) -> SpellInterface:
        """
        Cria uma magia a partir de componentes.

        Args:
            spell_name: Nome da magia
            component_names: Lista de nomes de componentes

        Returns:
            A magia criada

        Raises:
            ValueError: Se o número de componentes for insuficiente ou algum componente não estiver registrado
        """
        # Verifica se existem pelo menos 3 componentes
        if len(component_names) < 3:
            raise ValueError("Uma magia precisa de pelo menos 3 componentes")

        # Obtém os objetos de componente
        components = []
        for name in component_names:
            if name in self._registered_components:
                components.append(self._registered_components[name])
            else:
                raise ValueError(f"Componente '{name}' não está registrado")

        # Verifica se a combinação corresponde a uma receita específica
        primary_effect = None
        secondary_effects = []

        # Usa o RecipeManager para encontrar uma receita correspondente
        recipe_match = self._recipe_manager.find_matching_recipe(component_names)
        if recipe_match:
            recipe_name, effect_name = recipe_match
            primary_effect = self._registered_effects[effect_name]
            self.notify("recipe_matched", recipe_name)

        # Se não corresponder a uma receita, aplica as regras de combinação
        if not primary_effect:
            for rule in self._combination_rules:
                result = rule.apply(components)
                if result:
                    if not primary_effect:
                        primary_effect = result
                        self.notify("rule_applied", {
                            "rule": rule,
                            "effect": primary_effect
                        })
                    else:
                        secondary_effects.append(result)

        # Se nenhuma regra se aplicar, cria um efeito genérico
        if not primary_effect:
            # Determina o elemento dominante
            element_counts = Counter(comp.element for comp in components)
            dominant_element = element_counts.most_common(1)[0][0]

            # Calcula o poder total
            total_power = sum(comp.power for comp in components)

            description = f"Produz uma manifestação genérica de {dominant_element}"
            primary_effect = MagicalEffect(
                f"Manifestação de {dominant_element.capitalize()}",
                description,
                total_power
            )

            self.notify("generic_effect_created", primary_effect)

        # Importamos aqui para evitar importação circular
        from spellcrafting.core import Spell

        # Cria a magia usando as calculadoras específicas
        spell = Spell(
            spell_name,
            components,
            primary_effect,
            secondary_effects,
            self._power_calculator,
            self._level_calculator,
            self._element_calculator,
            self._scaling_calculator
        )

        # Registra no histórico para aprendizado
        self._spell_history.append((components, primary_effect))

        # Notifica os observadores
        self.notify("spell_created", spell)

        return spell

    def get_component(self, name: str) -> Optional[MagicalComponentInterface]:
        """
        Obtém um componente pelo nome.

        Args:
            name: Nome do componente

        Returns:
            O componente, ou None se não encontrado
        """
        return self._registered_components.get(name)

    def get_effect(self, name: str) -> Optional[MagicalEffectInterface]:
        """
        Obtém um efeito pelo nome.

        Args:
            name: Nome do efeito

        Returns:
            O efeito, ou None se não encontrado
        """
        return self._registered_effects.get(name)

    def get_components_by_element(self, element: str) -> List[MagicalComponentInterface]:
        """
        Obtém todos os componentes de um determinado elemento.

        Args:
            element: Nome do elemento

        Returns:
            Lista de componentes do elemento especificado
        """
        return [comp for comp in self._registered_components.values() if comp.element == element]

    def get_components_by_rarity(self, rarity: str) -> List[MagicalComponentInterface]:
        """
        Obtém todos os componentes de uma determinada raridade.

        Args:
            rarity: Nome da raridade

        Returns:
            Lista de componentes da raridade especificada
        """
        return [comp for comp in self._registered_components.values() if comp.rarity == rarity]

    def get_compatible_elements(self, element: str) -> List[str]:
        """
        Retorna elementos compatíveis com o elemento dado, utilizando o ElementManager.

        Args:
            element: Nome do elemento

        Returns:
            Lista de elementos compatíveis
        """
        return self._element_manager.get_compatible_elements(element)

    # Implementação da interface ObserverInterface
    def update(self, event_type: str, data: Any) -> None:
        """
        Recebe atualizações de outros componentes do sistema.

        Args:
            event_type: Tipo do evento
            data: Dados do evento
        """
        # Propaga as notificações recebidas do RecipeManager para os próprios observadores
        if event_type.startswith("recipe_"):
            self.notify(event_type, data)