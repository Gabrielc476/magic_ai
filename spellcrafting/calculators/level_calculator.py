# spellcrafting/calculators/level_calculator.py
"""
Implementação de calculadoras de nível de magia.
"""
from typing import List
from spellcrafting.core import LevelCalculatorInterface, MagicalComponentInterface


class DefaultLevelCalculator(LevelCalculatorInterface):
    """
    Calculadora padrão para o nível de uma magia.
    Considera a pontuação total baseada no poder, raridade,
    número de componentes e combinações elementais.
    """

    def __init__(self):
        """Inicializa a calculadora de nível padrão."""
        # Combinações elementais poderosas
        self._powerful_combinations = [
            {"fogo", "ar"},  # Tempestade de fogo
            {"água", "trevas"},  # Magia negra aquática
            {"luz", "ar"},  # Magias celestiais
            {"terra", "fogo"},  # Magias vulcânicas
            {"trevas", "fogo"},  # Magia demoníaca
            {"luz", "trevas"}  # Magias de dualidade (muito raras)
        ]

        # Pontos de raridade
        self._rarity_points = {
            "comum": 0,
            "incomum": 2,
            "raro": 5,
            "épico": 10,
            "lendário": 20
        }

        # Limiares de nível
        self._level_thresholds = [
            (10, 0),  # Cantrip
            (15, 1),  # Nível 1
            (25, 2),  # Nível 2
            (35, 3),  # Nível 3
            (50, 4),  # Nível 4
            (65, 5),  # Nível 5
            (80, 6),  # Nível 6
            (100, 7),  # Nível 7
            (125, 8),  # Nível 8
            (float('inf'), 9)  # Nível 9
        ]

    def calculate(self, power: int, components: List[MagicalComponentInterface]) -> int:
        """
        Calcula o nível da magia com base no poder e componentes.

        Args:
            power: Poder calculado da magia
            components: Lista de componentes mágicos

        Returns:
            O nível calculado da magia (0-9)
        """
        # Base de pontuação a partir do poder
        base_score = power

        # Adiciona pontos por componentes de raridade superior
        rarity_points = sum(self._rarity_points.get(component.rarity, 0) for component in components)

        # Adiciona pontos pelo número de componentes além do mínimo (3)
        component_points = max(0, (len(components) - 3) * 3)

        # Adiciona pontos por combinações de elementos específicas
        element_points = self._calculate_element_points(components)

        # Calcula a pontuação total
        total_score = base_score + rarity_points + component_points + element_points

        # Determina o nível com base nos limiares
        for threshold, level in self._level_thresholds:
            if total_score < threshold:
                return level

        return 9  # Padrão para magias extremamente poderosas

    def _calculate_element_points(self, components: List[MagicalComponentInterface]) -> int:
        """
        Calcula pontos adicionais baseados em combinações de elementos.

        Args:
            components: Lista de componentes mágicos

        Returns:
            Pontos de elemento calculados
        """
        element_points = 0
        present_elements = set(component.element for component in components)

        # Verifica combinações elementais poderosas
        for combo in self._powerful_combinations:
            if combo.issubset(present_elements):
                element_points += 5

        # Bônus por diversidade de elementos
        if len(present_elements) >= 4:
            element_points += 10
        if len(present_elements) >= 5:
            element_points += 20

        return element_points


class ProgressiveLevelCalculator(LevelCalculatorInterface):
    """
    Calculadora de nível que usa uma escala progressiva para determinar o nível.
    Mais adequada para sistemas com curva de poder progressiva.
    """

    def __init__(self, base_progression: float = 1.5):
        """
        Inicializa a calculadora de nível progressiva.

        Args:
            base_progression: Fator de progressão entre níveis
        """
        self._base_progression = base_progression
        self._base_power_threshold = 10  # Poder mínimo para nível 1

    def calculate(self, power: int, components: List[MagicalComponentInterface]) -> int:
        """
        Calcula o nível da magia usando uma escala progressiva.

        Args:
            power: Poder calculado da magia
            components: Lista de componentes mágicos

        Returns:
            O nível calculado da magia (0-9)
        """
        # Calcula pontos de raridade
        rarity_points = 0
        for component in components:
            if component.rarity == "comum":
                rarity_points += 0
            elif component.rarity == "incomum":
                rarity_points += 1
            elif component.rarity == "raro":
                rarity_points += 3
            elif component.rarity == "épico":
                rarity_points += 6
            elif component.rarity == "lendário":
                rarity_points += 10

        # Calcula o poder ajustado
        adjusted_power = power + rarity_points

        # Aplica a escala progressiva
        if adjusted_power < self._base_power_threshold:
            return 0  # Cantrip

        for level in range(1, 10):
            # Cada nível requer progressivamente mais poder
            threshold = self._base_power_threshold * (self._base_progression ** (level - 1))
            if adjusted_power < threshold:
                return level - 1

        return 9  # Nível máximo


class ElementalBalanceLevelCalculator(LevelCalculatorInterface):
    """
    Calculadora de nível que considera principalmente o equilíbrio entre elementos.
    Favorece combinações balanceadas de elementos opostos.
    """

    def __init__(self):
        """Inicializa a calculadora de nível baseada em equilíbrio elemental."""
        # Elementos opostos que criam equilíbrio quando combinados
        self._opposing_elements = [
            {"fogo", "água"},
            {"terra", "ar"},
            {"luz", "trevas"}
        ]

        # Limiares de nível
        self._level_thresholds = [
            (10, 0),  # Cantrip
            (20, 1),  # Nível 1
            (35, 2),  # Nível 2
            (50, 3),  # Nível 3
            (70, 4),  # Nível 4
            (90, 5),  # Nível 5
            (115, 6),  # Nível 6
            (140, 7),  # Nível 7
            (170, 8),  # Nível 8
            (float('inf'), 9)  # Nível 9
        ]

    def calculate(self, power: int, components: List[MagicalComponentInterface]) -> int:
        """
        Calcula o nível da magia baseado no equilíbrio elemental.

        Args:
            power: Poder calculado da magia
            components: Lista de componentes mágicos

        Returns:
            O nível calculado da magia (0-9)
        """
        # Pontuação base a partir do poder
        base_score = power

        # Analisa o equilíbrio de elementos
        elements_present = set(component.element for component in components)
        element_balance_points = 0

        # Verifica por pares de elementos opostos
        for opposing_pair in self._opposing_elements:
            if opposing_pair.issubset(elements_present):
                element_balance_points += 15  # Alto bônus para equilíbrio perfeito

        # Verifica a presença de elementos específicos
        if "luz" in elements_present and "trevas" in elements_present:
            element_balance_points += 10  # Bônus especial para a dualidade luz/trevas

        # Adiciona pontos pela diversidade de elementos
        element_count = len(elements_present)
        diversity_points = element_count * 5

        # Calcula pontos por raridade
        rarity_points = sum(self._get_rarity_points(component.rarity) for component in components)

        # Calcula a pontuação total
        total_score = base_score + element_balance_points + diversity_points + rarity_points

        # Determina o nível com base nos limiares
        for threshold, level in self._level_thresholds:
            if total_score < threshold:
                return level

        return 9  # Nível máximo

    def _get_rarity_points(self, rarity: str) -> int:
        """Retorna pontos baseados na raridade."""
        rarity_points = {
            "comum": 0,
            "incomum": 1,
            "raro": 3,
            "épico": 6,
            "lendário": 10
        }
        return rarity_points.get(rarity, 0)