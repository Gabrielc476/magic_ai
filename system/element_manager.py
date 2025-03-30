# spellcrafting/system/element_manager.py
"""
Gerenciador de elementos mágicos e suas interações.
"""
from typing import List, Dict, Any, Optional, Set, Tuple
from ..core.interfaces import MagicalElement, SubjectInterface
from ..utils.observers import Subject
from ..utils.enums import ElementType, ElementInteraction


class Element(MagicalElement):
    """
    Implementação concreta de um elemento mágico.
    """

    def __init__(self, name: str, compatible_elements: List[str], properties: Dict[str, Any] = None):
        """
        Inicializa um elemento mágico.

        Args:
            name: Nome do elemento
            compatible_elements: Lista de elementos compatíveis
            properties: Propriedades específicas do elemento
        """
        self._name = name
        self._compatible_elements = compatible_elements
        self._properties = properties or {}

    @property
    def name(self) -> str:
        """Retorna o nome do elemento."""
        return self._name

    @property
    def compatible_elements(self) -> List[str]:
        """Retorna a lista de elementos compatíveis."""
        return self._compatible_elements.copy()

    @property
    def properties(self) -> Dict[str, Any]:
        """Retorna as propriedades do elemento."""
        return self._properties.copy()

    def __str__(self) -> str:
        """Retorna uma representação em string do elemento."""
        return f"Elemento: {self._name}"

    def __repr__(self) -> str:
        """Retorna uma representação em string do elemento para debugging."""
        return f"Element('{self._name}', {self._compatible_elements}, {self._properties})"


class ElementManager(Subject):
    """
    Gerenciador de elementos mágicos e suas interações.
    Implementa o padrão Singleton para garantir uma única instância.
    """

    _instance = None

    def __new__(cls):
        """Implementa o padrão Singleton."""
        if cls._instance is None:
            cls._instance = super(ElementManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Inicializa o gerenciador de elementos."""
        if self._initialized:
            return

        super().__init__()
        self._elements: Dict[str, Element] = {}
        self._element_interactions: Dict[Tuple[str, str], ElementInteraction] = {}

        # Inicializa com elementos padrão
        self._initialize_default_elements()
        self._initialize_default_interactions()

        self._initialized = True

    def _initialize_default_elements(self) -> None:
        """Inicializa os elementos padrão."""
        default_elements = [
            Element("fogo", ["ar", "terra"], {
                "description": "Elemento ardente e consumidor",
                "opposing": "água",
                "primary_effect": "dano",
                "secondary_effect": "iluminação"
            }),
            Element("água", ["ar", "terra"], {
                "description": "Elemento fluido e adaptável",
                "opposing": "fogo",
                "primary_effect": "cura",
                "secondary_effect": "controle"
            }),
            Element("terra", ["água", "fogo"], {
                "description": "Elemento sólido e resistente",
                "opposing": "ar",
                "primary_effect": "proteção",
                "secondary_effect": "restrição"
            }),
            Element("ar", ["fogo", "água"], {
                "description": "Elemento livre e rápido",
                "opposing": "terra",
                "primary_effect": "movimento",
                "secondary_effect": "distância"
            }),
            Element("luz", ["ar", "fogo"], {
                "description": "Elemento revelador e purificador",
                "opposing": "trevas",
                "primary_effect": "iluminação",
                "secondary_effect": "cura"
            }),
            Element("trevas", ["terra", "água"], {
                "description": "Elemento misterioso e corruptor",
                "opposing": "luz",
                "primary_effect": "ocultação",
                "secondary_effect": "dano"
            })
        ]

        for element in default_elements:
            self.register_element(element)

    def _initialize_default_interactions(self) -> None:
        """Inicializa as interações padrão entre elementos."""
        # Interações poderosas
        self.register_interaction("fogo", "ar", ElementInteraction.SYNERGY,
                                  "Cria explosões e aumenta o alcance")
        self.register_interaction("água", "terra", ElementInteraction.SYNERGY,
                                  "Cria lama que dificulta movimento")
        self.register_interaction("luz", "ar", ElementInteraction.SYNERGY,
                                  "Cria raios solares benéficos")
        self.register_interaction("trevas", "terra", ElementInteraction.SYNERGY,
                                  "Corrompe o solo e drena energia")

        # Interações opostas
        self.register_interaction("fogo", "água", ElementInteraction.OPPOSITION,
                                  "Elementos opostos enfraquecem um ao outro")
        self.register_interaction("terra", "ar", ElementInteraction.OPPOSITION,
                                  "Elementos opostos enfraquecem um ao outro")
        self.register_interaction("luz", "trevas", ElementInteraction.OPPOSITION,
                                  "Elementos opostos enfraquecem um ao outro")

        # Interações neutras
        self.register_interaction("fogo", "trevas", ElementInteraction.NEUTRAL,
                                  "Combinação não possui efeitos especiais")
        self.register_interaction("água", "luz", ElementInteraction.NEUTRAL,
                                  "Combinação não possui efeitos especiais")

        # Interações raras
        self.register_interaction("luz", "trevas", ElementInteraction.RARE_COMBINATION,
                                  "Combinação rara que cria efeitos de dualidade")

    def register_element(self, element: Element) -> None:
        """
        Registra um novo elemento.

        Args:
            element: O elemento a ser registrado

        Raises:
            ValueError: Se um elemento com o mesmo nome já existir
        """
        if element.name in self._elements:
            raise ValueError(f"Elemento '{element.name}' já está registrado")

        self._elements[element.name] = element
        self.notify("element_registered", element)

    def register_interaction(
            self,
            element1: str,
            element2: str,
            interaction_type: ElementInteraction,
            description: str
    ) -> None:
        """
        Registra uma interação entre dois elementos.

        Args:
            element1: Nome do primeiro elemento
            element2: Nome do segundo elemento
            interaction_type: Tipo de interação
            description: Descrição da interação

        Raises:
            ValueError: Se algum dos elementos não estiver registrado
        """
        # Verifica se os elementos existem
        if element1 not in self._elements:
            raise ValueError(f"Elemento '{element1}' não está registrado")
        if element2 not in self._elements:
            raise ValueError(f"Elemento '{element2}' não está registrado")

        # Garante ordem consistente
        if element1 > element2:
            element1, element2 = element2, element1

        # Registra a interação
        interaction_key = (element1, element2)
        self._element_interactions[interaction_key] = interaction_type

        # Notifica os observadores
        self.notify("interaction_registered", {
            "elements": (element1, element2),
            "type": interaction_type,
            "description": description
        })

    def get_element(self, name: str) -> Optional[Element]:
        """
        Obtém um elemento pelo nome.

        Args:
            name: Nome do elemento

        Returns:
            O elemento, ou None se não encontrado
        """
        return self._elements.get(name)

    def get_all_elements(self) -> List[Element]:
        """
        Obtém todos os elementos registrados.

        Returns:
            Lista de todos os elementos
        """
        return list(self._elements.values())

    def get_interaction(self, element1: str, element2: str) -> ElementInteraction:
        """
        Obtém o tipo de interação entre dois elementos.

        Args:
            element1: Nome do primeiro elemento
            element2: Nome do segundo elemento

        Returns:
            O tipo de interação
        """
        # Garante ordem consistente
        if element1 > element2:
            element1, element2 = element2, element1

        interaction_key = (element1, element2)
        return self._element_interactions.get(interaction_key, ElementInteraction.NEUTRAL)

    def get_compatible_elements(self, element_name: str) -> List[str]:
        """
        Obtém a lista de elementos compatíveis com um determinado elemento.

        Args:
            element_name: Nome do elemento

        Returns:
            Lista de nomes de elementos compatíveis
        """
        element = self.get_element(element_name)
        if element:
            return element.compatible_elements
        return []

    def get_synergistic_combinations(self) -> List[Tuple[str, str]]:
        """
        Obtém todas as combinações de elementos que possuem sinergia.

        Returns:
            Lista de tuplas (elemento1, elemento2) com sinergia
        """
        synergistic = []
        for (element1, element2), interaction in self._element_interactions.items():
            if interaction == ElementInteraction.SYNERGY:
                synergistic.append((element1, element2))
        return synergistic

    def get_rare_combinations(self) -> List[Tuple[str, str]]:
        """
        Obtém todas as combinações raras de elementos.

        Returns:
            Lista de tuplas (elemento1, elemento2) que formam combinações raras
        """
        rare = []
        for (element1, element2), interaction in self._element_interactions.items():
            if interaction == ElementInteraction.RARE_COMBINATION:
                rare.append((element1, element2))
        return rare

    def calculate_elemental_bonus(self, elements: List[str]) -> float:
        """
        Calcula o bônus baseado nas interações entre múltiplos elementos.

        Args:
            elements: Lista de nomes de elementos

        Returns:
            Um multiplicador baseado nas interações
        """
        if not elements:
            return 1.0

        # Conta elementos únicos
        unique_elements = set(elements)
        if len(unique_elements) <= 1:
            return 1.0  # Sem bônus para um único elemento

        # Conta as interações
        synergies = 0
        oppositions = 0
        rare_combinations = 0

        # Verifica todas as combinações
        checked_pairs = set()
        for i, elem1 in enumerate(unique_elements):
            for elem2 in list(unique_elements)[i + 1:]:
                # Garante ordem consistente
                if elem1 > elem2:
                    elem1, elem2 = elem2, elem1

                pair = (elem1, elem2)
                if pair in checked_pairs:
                    continue

                interaction = self.get_interaction(elem1, elem2)
                if interaction == ElementInteraction.SYNERGY:
                    synergies += 1
                elif interaction == ElementInteraction.OPPOSITION:
                    oppositions += 1
                elif interaction == ElementInteraction.RARE_COMBINATION:
                    rare_combinations += 1

                checked_pairs.add(pair)

        # Calcula o multiplicador
        multiplier = 1.0
        multiplier += synergies * 0.2  # Cada sinergia adiciona 20%
        multiplier -= oppositions * 0.1  # Cada oposição reduz 10%
        multiplier += rare_combinations * 0.5  # Cada combinação rara adiciona 50%

        # Bônus para alta diversidade
        if len(unique_elements) >= 4:
            multiplier += 0.2
        if len(unique_elements) >= 5:
            multiplier += 0.3

        # Evita multiplicadores muito baixos
        return max(0.5, multiplier)