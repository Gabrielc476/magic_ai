# spellcrafting/core/interfaces.py
"""
Interfaces e classes abstratas para o sistema de crafting de magia.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Tuple, Set, Callable


class MagicalElement(ABC):
    """Interface para elementos mágicos."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Retorna o nome do elemento."""
        pass

    @property
    @abstractmethod
    def compatible_elements(self) -> List[str]:
        """Retorna uma lista de elementos compatíveis."""
        pass

    @property
    @abstractmethod
    def properties(self) -> Dict[str, Any]:
        """Retorna propriedades específicas do elemento."""
        pass


class MagicalComponentInterface(ABC):
    """Interface para componentes mágicos."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Retorna o nome do componente."""
        pass

    @property
    @abstractmethod
    def element(self) -> str:
        """Retorna o elemento do componente."""
        pass

    @property
    @abstractmethod
    def power(self) -> int:
        """Retorna a potência do componente."""
        pass

    @property
    @abstractmethod
    def rarity(self) -> str:
        """Retorna a raridade do componente."""
        pass

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Converte componente para dicionário."""
        pass


class MagicalEffectInterface(ABC):
    """Interface para efeitos mágicos."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Retorna o nome do efeito."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Retorna a descrição do efeito."""
        pass

    @property
    @abstractmethod
    def base_power(self) -> int:
        """Retorna o poder base do efeito."""
        pass

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Converte efeito para dicionário."""
        pass


class SpellInterface(ABC):
    """Interface para magias."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Retorna o nome da magia."""
        pass

    @property
    @abstractmethod
    def components(self) -> List[MagicalComponentInterface]:
        """Retorna os componentes da magia."""
        pass

    @property
    @abstractmethod
    def primary_effect(self) -> Optional[MagicalEffectInterface]:
        """Retorna o efeito primário da magia."""
        pass

    @property
    @abstractmethod
    def secondary_effects(self) -> List[MagicalEffectInterface]:
        """Retorna efeitos secundários da magia."""
        pass

    @property
    @abstractmethod
    def power(self) -> int:
        """Retorna o poder calculado da magia."""
        pass

    @property
    @abstractmethod
    def dominant_element(self) -> str:
        """Retorna o elemento dominante da magia."""
        pass

    @property
    @abstractmethod
    def level(self) -> int:
        """Retorna o nível da magia."""
        pass

    @abstractmethod
    def add_component(self, component: MagicalComponentInterface) -> None:
        """Adiciona um componente à magia."""
        pass

    @abstractmethod
    def scale(self, casting_level: int) -> Dict[str, Any]:
        """Retorna a versão escalonada da magia."""
        pass

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Converte magia para dicionário."""
        pass


class PowerCalculatorInterface(ABC):
    """Interface para cálculo de poder de magia."""

    @abstractmethod
    def calculate(self, components: List[MagicalComponentInterface]) -> int:
        """Calcula o poder da magia."""
        pass


class LevelCalculatorInterface(ABC):
    """Interface para cálculo de nível de magia."""

    @abstractmethod
    def calculate(self, power: int, components: List[MagicalComponentInterface]) -> int:
        """Calcula o nível da magia."""
        pass


class ElementDominanceCalculatorInterface(ABC):
    """Interface para cálculo de elemento dominante."""

    @abstractmethod
    def calculate(self, components: List[MagicalComponentInterface]) -> str:
        """Calcula o elemento dominante da magia."""
        pass


class ScalingCalculatorInterface(ABC):
    """Interface para cálculo de escalonamento de magia."""

    @abstractmethod
    def calculate(self, spell: SpellInterface) -> Dict[int, Dict[str, Any]]:
        """Calcula os efeitos de escalonamento da magia."""
        pass


class CombinationRuleInterface(ABC):
    """Interface para regras de combinação de componentes."""

    @abstractmethod
    def apply(self, components: List[MagicalComponentInterface]) -> Optional[MagicalEffectInterface]:
        """Aplica a regra aos componentes e retorna um efeito se aplicável."""
        pass


class ComponentFactoryInterface(ABC):
    """Interface para fábrica de componentes."""

    @abstractmethod
    def create_component(self, name: str, element: str, power: int, rarity: str) -> MagicalComponentInterface:
        """Cria um componente mágico."""
        pass


class EffectFactoryInterface(ABC):
    """Interface para fábrica de efeitos."""

    @abstractmethod
    def create_effect(self, name: str, description: str, base_power: int) -> MagicalEffectInterface:
        """Cria um efeito mágico."""
        pass


class SpellFactoryInterface(ABC):
    """Interface para fábrica de magias."""

    @abstractmethod
    def create_spell(self, name: str, components: List[MagicalComponentInterface],
                     primary_effect: Optional[MagicalEffectInterface] = None,
                     secondary_effects: Optional[List[MagicalEffectInterface]] = None) -> SpellInterface:
        """Cria uma magia."""
        pass


class CraftingSystemInterface(ABC):
    """Interface para o sistema de crafting."""

    @abstractmethod
    def register_component(self, component: MagicalComponentInterface) -> None:
        """Registra um componente no sistema."""
        pass

    @abstractmethod
    def register_effect(self, effect: MagicalEffectInterface) -> None:
        """Registra um efeito no sistema."""
        pass

    @abstractmethod
    def register_recipe(self, recipe_name: str, component_names: List[str], effect_name: str) -> None:
        """Registra uma receita no sistema."""
        pass

    @abstractmethod
    def add_combination_rule(self, rule: CombinationRuleInterface) -> None:
        """Adiciona uma regra de combinação ao sistema."""
        pass

    @abstractmethod
    def create_spell(self, spell_name: str, component_names: List[str]) -> SpellInterface:
        """Cria uma magia a partir de componentes."""
        pass


class ObserverInterface(ABC):
    """Interface para observadores de eventos do sistema."""

    @abstractmethod
    def update(self, event_type: str, data: Any) -> None:
        """Atualiza o observador com novos dados."""
        pass


class SubjectInterface(ABC):
    """Interface para sujeitos observáveis."""

    @abstractmethod
    def attach(self, observer: ObserverInterface) -> None:
        """Adiciona um observador."""
        pass

    @abstractmethod
    def detach(self, observer: ObserverInterface) -> None:
        """Remove um observador."""
        pass

    @abstractmethod
    def notify(self, event_type: str, data: Any) -> None:
        """Notifica todos os observadores."""
        pass


class AIModelInterface(ABC):
    """Interface para modelos de IA."""

    @abstractmethod
    def train(self) -> bool:
        """Treina o modelo de IA."""
        pass

    @abstractmethod
    def predict(self, input_data: Any) -> Any:
        """Faz uma previsão baseada nos dados de entrada."""
        pass