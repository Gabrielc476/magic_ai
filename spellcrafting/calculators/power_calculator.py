# spellcrafting/calculators/power_calculator.py
"""
Implementação de calculadoras de poder de magia.
"""
from typing import List, Dict
from spellcrafting.core import PowerCalculatorInterface, MagicalComponentInterface


class DefaultPowerCalculator(PowerCalculatorInterface):
    """
    Calculadora padrão para o poder de uma magia.
    Considera a potência e raridade dos componentes.
    """

    def __init__(self, rarity_multipliers: Dict[str, float] = None):
        """
        Inicializa a calculadora de poder.

        Args:
            rarity_multipliers: Multiplicadores por raridade
        """
        self._rarity_multipliers = rarity_multipliers or {
            "comum": 1.0,
            "incomum": 1.2,
            "raro": 1.5,
            "épico": 2.0,
            "lendário": 3.0
        }

    def calculate(self, components: List[MagicalComponentInterface]) -> int:
        """
        Calcula o poder da magia com base nos componentes.

        Args:
            components: Lista de componentes mágicos

        Returns:
            O poder calculado da magia
        """
        base_power = sum(component.power for component in components)
        rarity_multiplier = 1.0

        for component in components:
            rarity_multiplier *= self._rarity_multipliers.get(component.rarity, 1.0)

        return round(base_power * rarity_multiplier)


class LinearPowerCalculator(PowerCalculatorInterface):
    """
    Calculadora de poder que usa uma fórmula linear.
    Soma a potência base e adiciona bônus por raridade.
    """

    def __init__(self, rarity_bonuses: Dict[str, int] = None):
        """
        Inicializa a calculadora de poder linear.

        Args:
            rarity_bonuses: Bônus por raridade
        """
        self._rarity_bonuses = rarity_bonuses or {
            "comum": 0,
            "incomum": 2,
            "raro": 5,
            "épico": 10,
            "lendário": 20
        }

    def calculate(self, components: List[MagicalComponentInterface]) -> int:
        """
        Calcula o poder da magia usando uma fórmula linear.

        Args:
            components: Lista de componentes mágicos

        Returns:
            O poder calculado da magia
        """
        base_power = sum(component.power for component in components)
        rarity_bonus = sum(self._rarity_bonuses.get(component.rarity, 0) for component in components)

        return base_power + rarity_bonus


class ElementalSynergyPowerCalculator(PowerCalculatorInterface):
    """
    Calculadora de poder que considera sinergias entre elementos.
    Soma a potência base e adiciona bônus por combinações de elementos.
    """

    def __init__(self, synergy_combinations=None):
        """
        Inicializa a calculadora de poder com sinergias elementais.

        Args:
            synergy_combinations: Definições de combinações sinérgicas
        """
        self._synergy_combinations = synergy_combinations or [
            ({"fogo", "ar"}, 1.3),  # Tempestade de fogo
            ({"água", "trevas"}, 1.3),  # Magia negra aquática
            ({"luz", "ar"}, 1.3),  # Magias celestiais
            ({"terra", "fogo"}, 1.3),  # Magias vulcânicas
            ({"trevas", "fogo"}, 1.3),  # Magia demoníaca
            ({"luz", "trevas"}, 1.5)  # Magias de dualidade (muito raras)
        ]

    def calculate(self, components: List[MagicalComponentInterface]) -> int:
        """
        Calcula o poder da magia considerando sinergias elementais.

        Args:
            components: Lista de componentes mágicos

        Returns:
            O poder calculado da magia
        """
        base_power = sum(component.power for component in components)

        # Calcula o multiplicador de raridade
        rarity_multiplier = 1.0
        for component in components:
            if component.rarity == "comum":
                rarity_multiplier *= 1.0
            elif component.rarity == "incomum":
                rarity_multiplier *= 1.1
            elif component.rarity == "raro":
                rarity_multiplier *= 1.2
            elif component.rarity == "épico":
                rarity_multiplier *= 1.3
            elif component.rarity == "lendário":
                rarity_multiplier *= 1.5

        # Verifica sinergias elementais
        elements_present = set(component.element for component in components)
        synergy_multiplier = 1.0

        for elements, multiplier in self._synergy_combinations:
            if elements.issubset(elements_present):
                synergy_multiplier *= multiplier

        # Bônus adicional para grande diversidade elemental
        if len(elements_present) >= 4:
            synergy_multiplier *= 1.2
        if len(elements_present) >= 5:
            synergy_multiplier *= 1.3

        return round(base_power * rarity_multiplier * synergy_multiplier)