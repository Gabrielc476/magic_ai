# spellcrafting/rules/combination_rules.py
"""
Implementação de regras de combinação para o sistema de crafting.
"""
from typing import List, Optional, Dict, Any
from ..core.interfaces import CombinationRuleInterface, MagicalComponentInterface, MagicalEffectInterface
from ..core.effect import MagicalEffect


class ElementalCombinationRule(CombinationRuleInterface):
    """
    Regra de combinação baseada em quantidades mínimas de elementos específicos.
    """

    def __init__(self, element_requirements: Dict[str, int], effect_generator):
        """
        Inicializa a regra de combinação elemental.

        Args:
            element_requirements: Dicionário com os elementos requeridos e suas quantidades mínimas
            effect_generator: Função que gera o efeito apropriado com base nos componentes
        """
        self._element_requirements = element_requirements
        self._effect_generator = effect_generator

    def apply(self, components: List[MagicalComponentInterface]) -> Optional[MagicalEffectInterface]:
        """
        Aplica a regra de combinação aos componentes.

        Args:
            components: Lista de componentes mágicos

        Returns:
            Um efeito mágico se a regra for aplicável, None caso contrário
        """
        # Conta os elementos presentes na combinação
        element_counts = {}
        for component in components:
            element = component.element
            element_counts[element] = element_counts.get(element, 0) + 1

        # Verifica se os requisitos de elementos são atendidos
        for element, min_count in self._element_requirements.items():
            if element_counts.get(element, 0) < min_count:
                return None  # Requisito não atendido

        # Todos os requisitos foram atendidos, gera o efeito
        return self._effect_generator(components)


class ExplosionRule(CombinationRuleInterface):
    """
    Regra para criar efeitos de explosão com fogo e ar.
    """

    def apply(self, components: List[MagicalComponentInterface]) -> Optional[MagicalEffectInterface]:
        """
        Aplica a regra de explosão aos componentes.

        Args:
            components: Lista de componentes mágicos

        Returns:
            Um efeito de explosão se houver pelo menos 2 componentes de fogo e 1 de ar
        """
        # Conta os elementos presentes
        fire_count = sum(1 for comp in components if comp.element == "fogo")
        air_count = sum(1 for comp in components if comp.element == "ar")

        # Verifica se os requisitos são atendidos
        if fire_count >= 2 and air_count >= 1:
            # Calcula potência total dos componentes relevantes
            total_power = sum(comp.power for comp in components if comp.element in ["fogo", "ar"])

            # Cria o efeito de explosão
            return MagicalEffect("Explosão", "Cria uma explosão de fogo", total_power)

        return None


class HealingRule(CombinationRuleInterface):
    """
    Regra para criar efeitos de cura com luz.
    """

    def apply(self, components: List[MagicalComponentInterface]) -> Optional[MagicalEffectInterface]:
        """
        Aplica a regra de cura aos componentes.

        Args:
            components: Lista de componentes mágicos

        Returns:
            Um efeito de cura se houver pelo menos 2 componentes de luz
        """
        # Conta os elementos presentes
        light_count = sum(1 for comp in components if comp.element == "luz")

        # Verifica se os requisitos são atendidos
        if light_count >= 2:
            # Calcula potência total dos componentes relevantes
            total_power = sum(comp.power for comp in components if comp.element == "luz")

            # Cria o efeito de cura
            return MagicalEffect("Cura", "Restaura saúde ao alvo", total_power)

        return None


class ShieldRule(CombinationRuleInterface):
    """
    Regra para criar efeitos de escudo com terra.
    """

    def apply(self, components: List[MagicalComponentInterface]) -> Optional[MagicalEffectInterface]:
        """
        Aplica a regra de escudo aos componentes.

        Args:
            components: Lista de componentes mágicos

        Returns:
            Um efeito de escudo se houver pelo menos 2 componentes de terra
        """
        # Conta os elementos presentes
        earth_count = sum(1 for comp in components if comp.element == "terra")

        # Verifica se os requisitos são atendidos
        if earth_count >= 2:
            # Calcula potência total dos componentes relevantes
            total_power = sum(comp.power for comp in components if comp.element == "terra")

            # Cria o efeito de escudo
            return MagicalEffect("Escudo", "Cria uma barreira protetora", total_power)

        return None


class DualityRule(CombinationRuleInterface):
    """
    Regra para criar efeitos baseados na dualidade de luz e trevas.
    """

    def apply(self, components: List[MagicalComponentInterface]) -> Optional[MagicalEffectInterface]:
        """
        Aplica a regra de dualidade aos componentes.

        Args:
            components: Lista de componentes mágicos

        Returns:
            Um efeito baseado na dualidade se houver pelo menos 1 componente de luz e 1 de trevas
        """
        # Conta os elementos presentes
        light_count = sum(1 for comp in components if comp.element == "luz")
        darkness_count = sum(1 for comp in components if comp.element == "trevas")

        # Verifica se os requisitos são atendidos
        if light_count >= 1 and darkness_count >= 1:
            # Calcula potência total dos componentes relevantes
            total_power = sum(comp.power for comp in components if comp.element in ["luz", "trevas"])

            # Aplica um multiplicador para representar a potência especial desta combinação
            adjusted_power = int(total_power * 1.5)

            # Cria o efeito de dualidade
            return MagicalEffect(
                "Dualidade Arcana",
                "Manipula o equilíbrio entre luz e trevas criando efeitos místicos poderosos",
                adjusted_power
            )

        return None


class ElementalStormRule(CombinationRuleInterface):
    """
    Regra para criar tempestades elementais quando há vários elementos diferentes.
    """

    def apply(self, components: List[MagicalComponentInterface]) -> Optional[MagicalEffectInterface]:
        """
        Aplica a regra de tempestade elemental aos componentes.

        Args:
            components: Lista de componentes mágicos

        Returns:
            Um efeito de tempestade elemental se houver pelo menos 4 elementos diferentes
        """
        # Conta os elementos únicos presentes
        unique_elements = set(comp.element for comp in components)

        # Verifica se os requisitos são atendidos
        if len(unique_elements) >= 4:
            # Calcula potência total dos componentes
            total_power = sum(comp.power for comp in components)

            # Aplica um multiplicador para representar a potência especial desta combinação
            adjusted_power = int(total_power * 1.3)

            # Cria o efeito de tempestade elemental
            return MagicalEffect(
                "Tempestade Elemental",
                "Conjura uma tempestade caótica de energia elemental combinada",
                adjusted_power
            )

        return None


# Exemplo de instanciação de uma regra usando a classe ElementalCombinationRule

def fire_tornado_effect_generator(components):
    """Gera um efeito de tornado de fogo."""
    total_power = sum(comp.power for comp in components if comp.element in ["fogo", "ar"])
    return MagicalEffect(
        "Tornado de Fogo",
        "Cria um tornado giratório de chamas que causa dano em área",
        total_power
    )


# Cria uma regra de tornado de fogo usando a classe base ElementalCombinationRule
fire_tornado_rule = ElementalCombinationRule(
    {"fogo": 1, "ar": 2},  # Requer pelo menos 1 componente de fogo e 2 de ar
    fire_tornado_effect_generator
)