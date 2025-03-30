# spellcrafting/utils/enums.py
"""
Enumerações utilizadas no sistema de crafting de magia.
"""
from enum import Enum, auto


class ElementType(Enum):
    """Tipos de elementos mágicos."""
    FIRE = "fogo"
    WATER = "água"
    EARTH = "terra"
    AIR = "ar"
    LIGHT = "luz"
    DARKNESS = "trevas"

    def __str__(self) -> str:
        """Retorna a representação em string do elemento."""
        return self.value

    @classmethod
    def from_string(cls, element_name: str) -> 'ElementType':
        """
        Converte uma string para um elemento.

        Args:
            element_name: Nome do elemento

        Returns:
            O elemento correspondente

        Raises:
            ValueError: Se o elemento não for reconhecido
        """
        for element in cls:
            if element.value == element_name:
                return element
        raise ValueError(f"Elemento desconhecido: {element_name}")


class RarityType(Enum):
    """Tipos de raridade de componentes."""
    COMMON = "comum"
    UNCOMMON = "incomum"
    RARE = "raro"
    EPIC = "épico"
    LEGENDARY = "lendário"

    def __str__(self) -> str:
        """Retorna a representação em string da raridade."""
        return self.value

    @classmethod
    def from_string(cls, rarity_name: str) -> 'RarityType':
        """
        Converte uma string para uma raridade.

        Args:
            rarity_name: Nome da raridade

        Returns:
            A raridade correspondente

        Raises:
            ValueError: Se a raridade não for reconhecida
        """
        for rarity in cls:
            if rarity.value == rarity_name:
                return rarity
        raise ValueError(f"Raridade desconhecida: {rarity_name}")

    @property
    def multiplier(self) -> float:
        """
        Retorna o multiplicador de poder associado à raridade.

        Returns:
            Multiplicador de poder
        """
        multipliers = {
            RarityType.COMMON: 1.0,
            RarityType.UNCOMMON: 1.2,
            RarityType.RARE: 1.5,
            RarityType.EPIC: 2.0,
            RarityType.LEGENDARY: 3.0
        }
        return multipliers[self]

    @property
    def points(self) -> int:
        """
        Retorna os pontos de nível associados à raridade.

        Returns:
            Pontos de nível
        """
        points = {
            RarityType.COMMON: 0,
            RarityType.UNCOMMON: 2,
            RarityType.RARE: 5,
            RarityType.EPIC: 10,
            RarityType.LEGENDARY: 20
        }
        return points[self]


class SpellSchool(Enum):
    """Escolas de magia."""
    ABJURATION = "abjuração"
    CONJURATION = "conjuração"
    DIVINATION = "adivinhação"
    ENCHANTMENT = "encantamento"
    EVOCATION = "evocação"
    ILLUSION = "ilusão"
    NECROMANCY = "necromancia"
    TRANSMUTATION = "transmutação"

    def __str__(self) -> str:
        """Retorna a representação em string da escola."""
        return self.value

    @classmethod
    def from_string(cls, school_name: str) -> 'SpellSchool':
        """
        Converte uma string para uma escola.

        Args:
            school_name: Nome da escola

        Returns:
            A escola correspondente

        Raises:
            ValueError: Se a escola não for reconhecida
        """
        for school in cls:
            if school.value == school_name:
                return school
        raise ValueError(f"Escola desconhecida: {school_name}")

    @classmethod
    def get_school_for_element(cls, element: ElementType) -> 'SpellSchool':
        """
        Retorna a escola de magia mais associada a um elemento.

        Args:
            element: O elemento

        Returns:
            A escola de magia correspondente
        """
        element_to_school = {
            ElementType.FIRE: SpellSchool.EVOCATION,
            ElementType.WATER: SpellSchool.TRANSMUTATION,
            ElementType.EARTH: SpellSchool.ABJURATION,
            ElementType.AIR: SpellSchool.CONJURATION,
            ElementType.LIGHT: SpellSchool.DIVINATION,
            ElementType.DARKNESS: SpellSchool.NECROMANCY
        }
        return element_to_school.get(element, SpellSchool.EVOCATION)


class EffectType(Enum):
    """Tipos de efeitos mágicos."""
    DAMAGE = "dano"
    HEALING = "cura"
    CONTROL = "controle"
    PROTECTION = "proteção"
    ILLUSION = "ilusão"
    SUMMONING = "invocação"
    UTILITY = "utilidade"
    MOVEMENT = "movimento"
    TRANSFORMATION = "transformação"
    DIVINATION = "adivinhação"
    ENCHANTMENT = "encantamento"
    CURSE = "maldição"

    def __str__(self) -> str:
        """Retorna a representação em string do tipo de efeito."""
        return self.value

    @classmethod
    def from_string(cls, effect_name: str) -> 'EffectType':
        """
        Converte uma string para um tipo de efeito.

        Args:
            effect_name: Nome do tipo de efeito

        Returns:
            O tipo de efeito correspondente

        Raises:
            ValueError: Se o tipo de efeito não for reconhecido
        """
        for effect_type in cls:
            if effect_type.value == effect_name:
                return effect_type
        raise ValueError(f"Tipo de efeito desconhecido: {effect_name}")

    @classmethod
    def get_effect_for_element(cls, element: ElementType) -> 'EffectType':
        """
        Retorna o tipo de efeito mais associado a um elemento.

        Args:
            element: O elemento

        Returns:
            O tipo de efeito correspondente
        """
        element_to_effect = {
            ElementType.FIRE: EffectType.DAMAGE,
            ElementType.WATER: EffectType.CONTROL,
            ElementType.EARTH: EffectType.PROTECTION,
            ElementType.AIR: EffectType.MOVEMENT,
            ElementType.LIGHT: EffectType.HEALING,
            ElementType.DARKNESS: EffectType.CURSE
        }
        return element_to_effect.get(element, EffectType.UTILITY)


class SpellLevel(Enum):
    """Níveis de magia."""
    CANTRIP = 0
    FIRST = 1
    SECOND = 2
    THIRD = 3
    FOURTH = 4
    FIFTH = 5
    SIXTH = 6
    SEVENTH = 7
    EIGHTH = 8
    NINTH = 9

    def __str__(self) -> str:
        """Retorna a representação em string do nível de magia."""
        descriptions = {
            SpellLevel.CANTRIP: "Truque (Cantrip)",
            SpellLevel.FIRST: "Nível 1 (Básica)",
            SpellLevel.SECOND: "Nível 2 (Aprendiz)",
            SpellLevel.THIRD: "Nível 3 (Adepto)",
            SpellLevel.FOURTH: "Nível 4 (Avançada)",
            SpellLevel.FIFTH: "Nível 5 (Superior)",
            SpellLevel.SIXTH: "Nível 6 (Arcana)",
            SpellLevel.SEVENTH: "Nível 7 (Arcana Superior)",
            SpellLevel.EIGHTH: "Nível 8 (Mística)",
            SpellLevel.NINTH: "Nível 9 (Lendária)"
        }
        return descriptions[self]

    @property
    def value(self) -> int:
        """Retorna o valor numérico do nível de magia."""
        return super().value

    @classmethod
    def from_int(cls, level: int) -> 'SpellLevel':
        """
        Converte um inteiro para um nível de magia.

        Args:
            level: Valor numérico do nível

        Returns:
            O nível de magia correspondente

        Raises:
            ValueError: Se o nível não for reconhecido
        """
        if not 0 <= level <= 9:
            raise ValueError(f"Nível de magia inválido: {level}")

        for spell_level in cls:
            if spell_level.value == level:
                return spell_level

        raise ValueError(f"Nível de magia não encontrado: {level}")


class ElementInteraction(Enum):
    """Tipos de interação entre elementos."""
    SYNERGY = auto()  # Elementos que trabalham bem juntos
    OPPOSITION = auto()  # Elementos opostos que se enfraquecem
    NEUTRAL = auto()  # Elementos sem interação especial
    RARE_COMBINATION = auto()  # Combinações raras e poderosas

    def __str__(self) -> str:
        """Retorna a representação em string do tipo de interação."""
        descriptions = {
            ElementInteraction.SYNERGY: "Sinergia",
            ElementInteraction.OPPOSITION: "Oposição",
            ElementInteraction.NEUTRAL: "Neutra",
            ElementInteraction.RARE_COMBINATION: "Combinação Rara"
        }
        return descriptions[self]


class AIModelType(Enum):
    """Tipos de modelos de IA usados no sistema."""
    RECOMMENDATION = auto()  # Recomendação de componentes
    EFFECT_PREDICTION = auto()  # Predição de efeitos
    NAME_GENERATION = auto()  # Geração de nomes
    ELEMENTAL_AFFINITY = auto()  # Predição de afinidades elementais

    def __str__(self) -> str:
        """Retorna a representação em string do tipo de modelo de IA."""
        descriptions = {
            AIModelType.RECOMMENDATION: "Recomendação de Componentes",
            AIModelType.EFFECT_PREDICTION: "Predição de Efeitos",
            AIModelType.NAME_GENERATION: "Geração de Nomes",
            AIModelType.ELEMENTAL_AFFINITY: "Afinidade Elemental"
        }
        return descriptions[self]


class EventType(Enum):
    """Tipos de eventos do sistema."""
    COMPONENT_REGISTERED = "component_registered"
    EFFECT_REGISTERED = "effect_registered"
    RECIPE_REGISTERED = "recipe_registered"
    RECIPE_REMOVED = "recipe_removed"
    RECIPES_CLEARED = "recipes_cleared"
    RULE_ADDED = "rule_added"
    SPELL_CREATED = "spell_created"
    ELEMENT_REGISTERED = "element_registered"
    INTERACTION_REGISTERED = "interaction_registered"

    def __str__(self) -> str:
        """Retorna a representação em string do tipo de evento."""
        return self.value