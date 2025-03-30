# spellcrafting/utils/enum_converters.py
"""
Utilitários para conversão entre enumerações e valores de string.
Facilita a transição para o uso de enumerações em vez de strings.
"""
from typing import Union, List, Dict, Any, Optional, TypeVar, Callable
from .enums import ElementType, RarityType, EffectType, SpellLevel

# Tipos genéricos para converter
T = TypeVar('T')
EnumType = TypeVar('EnumType')


class EnumConverter:
    """
    Classe utilitária para converter entre enumerações e strings.
    """

    @staticmethod
    def to_enum(value: str, enum_class, default: Optional[EnumType] = None) -> EnumType:
        """
        Converte uma string para um valor de enumeração.

        Args:
            value: String a ser convertida
            enum_class: Classe de enumeração (ElementType, RarityType, etc.)
            default: Valor padrão se a conversão falhar

        Returns:
            Valor da enumeração ou o valor padrão
        """
        try:
            return enum_class.from_string(value)
        except ValueError:
            return default

    @staticmethod
    def to_string(enum_value) -> str:
        """
        Converte um valor de enumeração para string.

        Args:
            enum_value: Valor da enumeração

        Returns:
            String correspondente
        """
        return str(enum_value)

    @staticmethod
    def convert_dict_keys(
            data: Dict[str, T],
            converter: Callable[[str], EnumType]
    ) -> Dict[EnumType, T]:
        """
        Converte as chaves de um dicionário de strings para enumerações.

        Args:
            data: Dicionário com chaves string
            converter: Função para converter string para enumeração

        Returns:
            Dicionário com chaves enum
        """
        return {converter(k): v for k, v in data.items()}

    @staticmethod
    def convert_dict_values(
            data: Dict[T, str],
            converter: Callable[[str], EnumType]
    ) -> Dict[T, EnumType]:
        """
        Converte os valores de um dicionário de strings para enumerações.

        Args:
            data: Dicionário com valores string
            converter: Função para converter string para enumeração

        Returns:
            Dicionário com valores enum
        """
        return {k: converter(v) for k, v in data.items()}


class ElementConverter:
    """
    Conversor específico para elementos.
    """

    @staticmethod
    def to_enum(element_name: str) -> ElementType:
        """
        Converte um nome de elemento para a enumeração ElementType.

        Args:
            element_name: Nome do elemento

        Returns:
            Enumeração ElementType correspondente

        Raises:
            ValueError: Se o elemento não for reconhecido
        """
        return ElementType.from_string(element_name)

    @staticmethod
    def to_string(element_type: ElementType) -> str:
        """
        Converte uma enumeração ElementType para string.

        Args:
            element_type: Enumeração do elemento

        Returns:
            Nome do elemento
        """
        return element_type.value

    @staticmethod
    def convert_list(elements: List[str]) -> List[ElementType]:
        """
        Converte uma lista de nomes de elementos para enumerações.

        Args:
            elements: Lista de nomes de elementos

        Returns:
            Lista de enumerações ElementType
        """
        return [ElementConverter.to_enum(elem) for elem in elements]


class RarityConverter:
    """
    Conversor específico para raridades.
    """

    @staticmethod
    def to_enum(rarity_name: str) -> RarityType:
        """
        Converte um nome de raridade para a enumeração RarityType.

        Args:
            rarity_name: Nome da raridade

        Returns:
            Enumeração RarityType correspondente

        Raises:
            ValueError: Se a raridade não for reconhecida
        """
        return RarityType.from_string(rarity_name)

    @staticmethod
    def to_string(rarity_type: RarityType) -> str:
        """
        Converte uma enumeração RarityType para string.

        Args:
            rarity_type: Enumeração da raridade

        Returns:
            Nome da raridade
        """
        return rarity_type.value

    @staticmethod
    def get_multiplier(rarity: Union[str, RarityType]) -> float:
        """
        Obtém o multiplicador de poder associado à raridade.

        Args:
            rarity: Nome da raridade ou enumeração RarityType

        Returns:
            Multiplicador de poder
        """
        if isinstance(rarity, str):
            rarity = RarityConverter.to_enum(rarity)
        return rarity.multiplier

    @staticmethod
    def get_points(rarity: Union[str, RarityType]) -> int:
        """
        Obtém os pontos de nível associados à raridade.

        Args:
            rarity: Nome da raridade ou enumeração RarityType

        Returns:
            Pontos de nível
        """
        if isinstance(rarity, str):
            rarity = RarityConverter.to_enum(rarity)
        return rarity.points


class EffectTypeConverter:
    """
    Conversor específico para tipos de efeito.
    """

    @staticmethod
    def to_enum(effect_name: str) -> EffectType:
        """
        Converte um nome de efeito para a enumeração EffectType.

        Args:
            effect_name: Nome do tipo de efeito

        Returns:
            Enumeração EffectType correspondente

        Raises:
            ValueError: Se o tipo de efeito não for reconhecido
        """
        return EffectType.from_string(effect_name)

    @staticmethod
    def to_string(effect_type: EffectType) -> str:
        """
        Converte uma enumeração EffectType para string.

        Args:
            effect_type: Enumeração do tipo de efeito

        Returns:
            Nome do tipo de efeito
        """
        return effect_type.value

    @staticmethod
    def get_effect_for_element(element: Union[str, ElementType]) -> EffectType:
        """
        Retorna o tipo de efeito mais associado a um elemento.

        Args:
            element: Nome do elemento ou enumeração ElementType

        Returns:
            Tipo de efeito correspondente
        """
        if isinstance(element, str):
            element = ElementConverter.to_enum(element)
        return EffectType.get_effect_for_element(element)


class SpellLevelConverter:
    """
    Conversor específico para níveis de magia.
    """

    @staticmethod
    def to_enum(level: int) -> SpellLevel:
        """
        Converte um valor numérico para a enumeração SpellLevel.

        Args:
            level: Valor numérico do nível

        Returns:
            Enumeração SpellLevel correspondente

        Raises:
            ValueError: Se o nível não for válido
        """
        return SpellLevel.from_int(level)

    @staticmethod
    def to_int(spell_level: SpellLevel) -> int:
        """
        Converte uma enumeração SpellLevel para um inteiro.

        Args:
            spell_level: Enumeração do nível

        Returns:
            Valor numérico do nível
        """
        return spell_level.value

    @staticmethod
    def get_description(level: Union[int, SpellLevel]) -> str:
        """
        Obtém a descrição textual do nível de magia.

        Args:
            level: Valor numérico ou enumeração SpellLevel

        Returns:
            Descrição do nível
        """
        if isinstance(level, int):
            level = SpellLevelConverter.to_enum(level)
        return str(level)