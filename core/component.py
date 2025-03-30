# spellcrafting/core/component.py
"""
Implementação de componentes mágicos.
"""
from typing import Dict, Any
from .interfaces import MagicalComponentInterface


class MagicalComponent(MagicalComponentInterface):
    """
    Componente mágico usado para criar magias.
    """

    def __init__(self, name: str, element: str, power: int, rarity: str):
        """
        Inicializa um componente mágico.

        Args:
            name: Nome do componente
            element: Elemento do componente (fogo, água, terra, ar, luz, trevas, etc.)
            power: Potência do componente (1-10)
            rarity: Raridade do componente (comum, incomum, raro, épico, lendário)
        """
        self._name = name
        self._element = element
        self._power = power
        self._rarity = rarity

        # Validação
        if power < 1 or power > 10:
            raise ValueError("A potência do componente deve estar entre 1 e 10")

        valid_rarities = ["comum", "incomum", "raro", "épico", "lendário"]
        if rarity not in valid_rarities:
            raise ValueError(f"Raridade inválida. Deve ser uma de: {', '.join(valid_rarities)}")

    @property
    def name(self) -> str:
        """Retorna o nome do componente."""
        return self._name

    @property
    def element(self) -> str:
        """Retorna o elemento do componente."""
        return self._element

    @property
    def power(self) -> int:
        """Retorna a potência do componente."""
        return self._power

    @property
    def rarity(self) -> str:
        """Retorna a raridade do componente."""
        return self._rarity

    def to_dict(self) -> Dict[str, Any]:
        """Converte o componente para um dicionário."""
        return {
            "name": self._name,
            "element": self._element,
            "power": self._power,
            "rarity": self._rarity
        }

    def __str__(self) -> str:
        """Retorna uma representação em string do componente."""
        return f"{self._name} ({self._element}, Potência: {self._power}, Raridade: {self._rarity})"

    def __repr__(self) -> str:
        """Retorna uma representação em string do componente para debugging."""
        return f"MagicalComponent('{self._name}', '{self._element}', {self._power}, '{self._rarity}')"