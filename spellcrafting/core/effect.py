# spellcrafting/core/effect.py
"""
Implementação de efeitos mágicos.
"""
from typing import Dict, Any
from .interfaces import MagicalEffectInterface


class MagicalEffect(MagicalEffectInterface):
    """
    Efeito mágico que pode ser aplicado por uma magia.
    """

    def __init__(self, name: str, description: str, base_power: int):
        """
        Inicializa um efeito mágico.

        Args:
            name: Nome do efeito
            description: Descrição do que o efeito faz
            base_power: Poder base do efeito
        """
        self._name = name
        self._description = description
        self._base_power = base_power

        # Validação
        if base_power < 1:
            raise ValueError("O poder base do efeito deve ser pelo menos 1")

    @property
    def name(self) -> str:
        """Retorna o nome do efeito."""
        return self._name

    @property
    def description(self) -> str:
        """Retorna a descrição do efeito."""
        return self._description

    @property
    def base_power(self) -> int:
        """Retorna o poder base do efeito."""
        return self._base_power

    def to_dict(self) -> Dict[str, Any]:
        """Converte o efeito para um dicionário."""
        return {
            "name": self._name,
            "description": self._description,
            "base_power": self._base_power
        }

    def __str__(self) -> str:
        """Retorna uma representação em string do efeito."""
        return f"{self._name}: {self._description} (Poder base: {self._base_power})"

    def __repr__(self) -> str:
        """Retorna uma representação em string do efeito para debugging."""
        return f"MagicalEffect('{self._name}', '{self._description}', {self._base_power})"