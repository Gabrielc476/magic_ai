# spellcrafting/ai/effect_predictor.py
"""
Sistema de predição de efeitos de magia.
"""
from typing import List, Dict, Optional, Tuple
from collections import Counter

from spellcrafting.core import MagicalComponentInterface, MagicalEffectInterface, AIModelInterface
from spellcrafting.core import MagicalEffect
from .vector_converter import VectorConverter
from spellcrafting.system.crafting_system import CraftingSystem


class EffectPredictor(AIModelInterface):
    """
    Motor de predição para efeitos mágicos.
    Prevê o efeito mais provável para uma combinação de componentes.
    """

    def __init__(self, crafting_system: CraftingSystem, vector_converter: Optional[VectorConverter] = None):
        """
        Inicializa o motor de predição.

        Args:
            crafting_system: Sistema de crafting a ser usado para predições
            vector_converter: Conversor de vetores (opcional)
        """
        self._crafting_system = crafting_system
        self._vector_converter = vector_converter or VectorConverter()
        self._model = None  # Será inicializado durante o treinamento
        self._effect_mapping: Dict[str, int] = {}  # Mapeamento entre nomes de efeitos e índices
        self._trained = False

    def train(self) -> bool:
        """
        Treina o modelo de predição com base no histórico de magias.

        Returns:
            True se o treinamento foi bem-sucedido, False caso contrário
        """
        try:
            from sklearn.ensemble import RandomForestClassifier

            # Prepara os dados de treinamento a partir do histórico de magias
            spell_history = self._crafting_system.spell_history

            if len(spell_history) < 2:
                return False  # Dados insuficientes para treinar

            X = []  # Vetores de características das combinações
            y = []  # Índices dos efeitos correspondentes

            # Prepara os dados de treinamento
            for components, effect in spell_history:
                X.append(self._vector_converter.components_to_vector(components))

                # Se este efeito ainda não foi visto, adicione ao dicionário
                effect_name = effect.name
                if effect_name not in self._effect_mapping:
                    self._effect_mapping[effect_name] = len(self._effect_mapping)

                y.append(self._effect_mapping[effect_name])

            # Verifica se há pelo menos duas classes diferentes
            if len(set(y)) < 2:
                return False  # Precisa de pelo menos duas classes

            # Treina o modelo de classificação
            self._model = RandomForestClassifier(n_estimators=10)
            self._model.fit(X, y)

            self._trained = True
            return True

        except Exception as e:
            print(f"Erro durante o treinamento: {e}")
            return False

    def predict(self, components: List[MagicalComponentInterface]) -> MagicalEffectInterface:
        """
        Prevê o efeito mais provável para uma combinação de componentes.

        Args:
            components: Lista de componentes mágicos

        Returns:
            O efeito mágico previsto
        """
        if not self._trained or self._model is None:
            # Fallback para a previsão baseada em elemento dominante
            return self._predict_by_dominant_element(components)

        try:
            # Converte a combinação em um vetor
            components_vector = self._vector_converter.components_to_vector(components)

            # Prevê o índice do efeito
            predicted_index = self._model.predict([components_vector])[0]

            # Encontra o nome do efeito correspondente ao índice
            for name, index in self._effect_mapping.items():
                if index == predicted_index:
                    # Encontra o objeto MagicalEffect correspondente
                    effect = self._crafting_system.get_effect(name)
                    if effect:
                        return effect

            # Se não encontrar, usa o fallback
            return self._predict_by_dominant_element(components)

        except Exception as e:
            print(f"Erro durante a predição: {e}")
            # Em caso de erro, usa o fallback
            return self._predict_by_dominant_element(components)

    def _predict_by_dominant_element(self, components: List[MagicalComponentInterface]) -> MagicalEffectInterface:
        """
        Prevê um efeito com base no elemento dominante dos componentes.

        Args:
            components: Lista de componentes mágicos

        Returns:
            Um efeito mágico baseado no elemento dominante
        """
        # Determina o elemento dominante
        element_counts = Counter(comp.element for comp in components)
        dominant_element = element_counts.most_common(1)[0][0]

        # Calcula o poder total baseado nos componentes
        total_power = sum(comp.power for comp in components)

        # Cria descrições baseadas no elemento dominante
        descriptions = {
            "fogo": "Cria uma manifestação flamejante de energia mágica",
            "água": "Invoca uma onda de energia aquática mágica",
            "terra": "Forma uma barreira sólida de energia terrestre",
            "ar": "Libera uma rajada de energia eólica concentrada",
            "luz": "Emite um feixe de energia luminosa purificadora",
            "trevas": "Envolve o alvo em sombras místicas corrosivas"
        }

        # Cria nomes baseados no elemento dominante
        names = {
            "fogo": "Manifestação de Fogo",
            "água": "Manifestação Aquática",
            "terra": "Manifestação Terrestre",
            "ar": "Manifestação Eólica",
            "luz": "Manifestação Luminosa",
            "trevas": "Manifestação Sombria"
        }

        name = names.get(dominant_element, f"Manifestação de {dominant_element.capitalize()}")
        description = descriptions.get(dominant_element, f"Produz uma manifestação mágica de {dominant_element}")

        return MagicalEffect(name, description, total_power)


class ElementalAffinityPredictor(AIModelInterface):
    """
    Preditor especializado em afinidades elementais.
    Prevê efeitos baseados em combinações específicas de elementos.
    """

    def __init__(self, crafting_system: CraftingSystem):
        """
        Inicializa o preditor de afinidade elemental.

        Args:
            crafting_system: Sistema de crafting
        """
        self._crafting_system = crafting_system
        self._element_affinities = self._init_element_affinities()
        self._trained = True  # Este preditor baseado em regras não precisa de treinamento

    def _init_element_affinities(self) -> Dict[Tuple[str, str], MagicalEffectInterface]:
        """
        Inicializa as afinidades entre elementos e seus efeitos típicos.

        Returns:
            Dicionário de pares de elementos e seus efeitos
        """
        # Define as combinações elementais mais comuns e seus efeitos
        affinities = {}

        # Fogo + Ar = Explosão
        affinities[("fogo", "ar")] = MagicalEffect(
            "Explosão Flamejante",
            "Cria uma explosão de chamas intensas em área",
            15
        )

        # Água + Terra = Lama
        affinities[("água", "terra")] = MagicalEffect(
            "Controle de Lama",
            "Manipula e controla a lama, criando terreno difícil",
            12
        )

        # Luz + Ar = Relâmpago
        affinities[("luz", "ar")] = MagicalEffect(
            "Relâmpago Divino",
            "Invoca um poderoso raio de energia pura",
            16
        )

        # Fogo + Terra = Magma
        affinities[("fogo", "terra")] = MagicalEffect(
            "Erupção de Magma",
            "Faz jorrar magma do solo, causando dano contínuo",
            18
        )

        # Água + Ar = Neblina
        affinities[("água", "ar")] = MagicalEffect(
            "Névoa Espessa",
            "Cria uma neblina densa que obscurece a visão",
            10
        )

        # Luz + Água = Purificação
        affinities[("luz", "água")] = MagicalEffect(
            "Águas Curativas",
            "Cria água purificada com propriedades curativas",
            14
        )

        # Trevas + Terra = Putrefação
        affinities[("trevas", "terra")] = MagicalEffect(
            "Solo Corrupto",
            "Contamina o solo com energia negativa, causando deterioração",
            13
        )

        # Trevas + Fogo = Chamas Sombrias
        affinities[("trevas", "fogo")] = MagicalEffect(
            "Chamas Sombrias",
            "Invoca fogo negro que queima a essência vital",
            17
        )

        # Luz + Trevas = Equilíbrio
        affinities[("luz", "trevas")] = MagicalEffect(
            "Harmonia dos Opostos",
            "Canaliza o poder do equilíbrio cósmico para efeitos extraordinários",
            20
        )

        return affinities

    def train(self) -> bool:
        """
        Este preditor não requer treinamento formal.

        Returns:
            Sempre retorna True
        """
        return True

    def predict(self, components: List[MagicalComponentInterface]) -> MagicalEffectInterface:
        """
        Prevê o efeito baseado nas afinidades elementais.

        Args:
            components: Lista de componentes mágicos

        Returns:
            O efeito mágico previsto
        """
        # Identifica os elementos presentes
        elements = [comp.element for comp in components]
        element_counts = Counter(elements)

        # Calcula o poder total
        total_power = sum(comp.power for comp in components)

        # Verifica pares de elementos com forte presença
        strongest_affinity = None
        strongest_count = 0

        for (elem1, elem2), effect in self._element_affinities.items():
            count1 = element_counts.get(elem1, 0)
            count2 = element_counts.get(elem2, 0)

            # Ambos os elementos devem estar presentes
            if count1 > 0 and count2 > 0:
                combined_count = count1 + count2

                # Escolhe a afinidade com maior presença combinada
                if combined_count > strongest_count:
                    strongest_count = combined_count
                    strongest_affinity = (elem1, elem2)

        # Se encontrou uma afinidade forte, retorna o efeito correspondente
        # com potência ajustada
        if strongest_affinity and strongest_affinity in self._element_affinities:
            base_effect = self._element_affinities[strongest_affinity]

            # Ajusta a potência com base nos componentes
            adjusted_power = int(total_power * 0.8)  # 80% do poder total

            return MagicalEffect(
                base_effect.name,
                base_effect.description,
                adjusted_power
            )

        # Caso não encontre afinidades fortes, cria um efeito genérico
        # baseado no elemento dominante
        dominant_element = element_counts.most_common(1)[0][0]

        return MagicalEffect(
            f"Manifestação de {dominant_element.capitalize()}",
            f"Produz uma manifestação genérica de energia de {dominant_element}",
            total_power
        )