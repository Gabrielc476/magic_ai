# spellcrafting/factories/__init__.py
"""
Implementações de fábricas para criação de componentes, efeitos e magias.
"""
from typing import List, Optional

from spellcrafting.core import (
    ComponentFactoryInterface,
    EffectFactoryInterface,
    SpellFactoryInterface,
    MagicalComponentInterface,
    MagicalEffectInterface,
    SpellInterface,
    PowerCalculatorInterface,
    LevelCalculatorInterface,
    ElementDominanceCalculatorInterface,
    ScalingCalculatorInterface
)
from spellcrafting.core import MagicalComponent
from spellcrafting.core import MagicalEffect
from spellcrafting.core import Spell


class ComponentFactory(ComponentFactoryInterface):
    """
    Fábrica para criação de componentes mágicos.
    """

    def create_component(self, name: str, element: str, power: int, rarity: str) -> MagicalComponentInterface:
        """
        Cria um componente mágico.

        Args:
            name: Nome do componente
            element: Elemento do componente
            power: Potência do componente (1-10)
            rarity: Raridade do componente

        Returns:
            O componente criado
        """
        return MagicalComponent(name, element, power, rarity)


class EffectFactory(EffectFactoryInterface):
    """
    Fábrica para criação de efeitos mágicos.
    """

    def create_effect(self, name: str, description: str, base_power: int) -> MagicalEffectInterface:
        """
        Cria um efeito mágico.

        Args:
            name: Nome do efeito
            description: Descrição do efeito
            base_power: Poder base do efeito

        Returns:
            O efeito criado
        """
        return MagicalEffect(name, description, base_power)


class SpellFactory(SpellFactoryInterface):
    """
    Fábrica para criação de magias.
    """

    def __init__(
            self,
            power_calculator: Optional[PowerCalculatorInterface] = None,
            level_calculator: Optional[LevelCalculatorInterface] = None,
            element_calculator: Optional[ElementDominanceCalculatorInterface] = None,
            scaling_calculator: Optional[ScalingCalculatorInterface] = None
    ):
        """
        Inicializa a fábrica de magias.

        Args:
            power_calculator: Calculadora de poder
            level_calculator: Calculadora de nível
            element_calculator: Calculadora de elemento dominante
            scaling_calculator: Calculadora de escalonamento
        """
        self._power_calculator = power_calculator
        self._level_calculator = level_calculator
        self._element_calculator = element_calculator
        self._scaling_calculator = scaling_calculator

    def create_spell(
            self,
            name: str,
            components: List[MagicalComponentInterface],
            primary_effect: Optional[MagicalEffectInterface] = None,
            secondary_effects: Optional[List[MagicalEffectInterface]] = None
    ) -> SpellInterface:
        """
        Cria uma magia.

        Args:
            name: Nome da magia
            components: Lista de componentes mágicos
            primary_effect: Efeito primário da magia
            secondary_effects: Efeitos secundários da magia

        Returns:
            A magia criada
        """
        return Spell(
            name,
            components,
            primary_effect,
            secondary_effects,
            self._power_calculator,
            self._level_calculator,
            self._element_calculator,
            self._scaling_calculator
        )