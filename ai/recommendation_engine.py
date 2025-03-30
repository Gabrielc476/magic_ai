# spellcrafting/ai/recommendation_engine.py
"""
Sistema de recomendação para componentes de magia.
"""
from typing import List, Dict, Any, Optional, Tuple
from collections import Counter
import numpy as np

from ..core.interfaces import MagicalComponentInterface, AIModelInterface
from .vector_converter import VectorConverter
from ..system.crafting_system import CraftingSystem


class ComponentRecommendationEngine(AIModelInterface):
    """
    Motor de recomendação para componentes mágicos.
    Sugere componentes compatíveis com base nos componentes atuais.
    """

    def __init__(self, crafting_system: CraftingSystem, vector_converter: Optional[VectorConverter] = None):
        """
        Inicializa o motor de recomendação.

        Args:
            crafting_system: Sistema de crafting a ser usado para recomendações
            vector_converter: Conversor de vetores (opcional)
        """
        self._crafting_system = crafting_system
        self._vector_converter = vector_converter or VectorConverter()
        self._model = None  # Será inicializado durante o treinamento
        self._trained = False

    def train(self) -> bool:
        """
        Treina o modelo de recomendação com base no histórico de magias.

        Returns:
            True se o treinamento foi bem-sucedido, False caso contrário
        """
        try:
            from sklearn.neighbors import NearestNeighbors

            # Prepara os dados de treinamento a partir do histórico de magias
            spell_history = self._crafting_system.spell_history

            if len(spell_history) < 2:
                return False  # Dados insuficientes para treinar

            # Converte cada combinação de componentes para um vetor
            X = []
            for components, _ in spell_history:
                X.append(self._vector_converter.components_to_vector(components))

            # Treina o modelo de vizinhos mais próximos
            self._model = NearestNeighbors(n_neighbors=min(3, len(X)), algorithm='auto')
            self._model.fit(X)

            self._trained = True
            return True

        except Exception as e:
            print(f"Erro durante o treinamento: {e}")
            return False

    def predict(self, components: List[MagicalComponentInterface]) -> List[MagicalComponentInterface]:
        """
        Recomenda componentes adicionais compatíveis com os componentes atuais.

        Args:
            components: Lista atual de componentes

        Returns:
            Lista de componentes recomendados
        """
        # Se não houver componentes ou o modelo não estiver treinado,
        # usa recomendações baseadas apenas em elementos
        if not components or not self._trained or self._model is None:
            return self._recommend_by_elements(components)

        # Converte os componentes atuais em um vetor
        current_vector = self._vector_converter.components_to_vector(components)

        try:
            # Encontra as combinações mais similares no histórico
            distances, indices = self._model.kneighbors([current_vector])

            # Extrai os componentes das combinações similares
            recommended_components = []
            current_component_names = {c.name for c in components}

            spell_history = self._crafting_system.spell_history
            for idx in indices[0]:
                # Obtém os componentes desta combinação similar
                similar_combo = spell_history[idx][0]
                for comp in similar_combo:
                    if comp.name not in current_component_names:
                        recommended_components.append(comp)

            # Conta as ocorrências de cada componente
            counter = Counter(comp.name for comp in recommended_components)

            # Obtém os 3 componentes mais frequentes
            top_components = []
            for name, _ in counter.most_common(3):
                component = self._crafting_system.get_component(name)
                if component:
                    top_components.append(component)

            # Se não encontrou 3 componentes, completa com recomendações baseadas em elementos
            if len(top_components) < 3:
                remaining = 3 - len(top_components)
                top_components.extend(self._recommend_by_elements(
                    components,
                    remaining,
                    exclude=[c.name for c in top_components]
                ))

            return top_components

        except Exception as e:
            print(f"Erro durante a predição: {e}")
            return self._recommend_by_elements(components)

    def _recommend_by_elements(
            self,
            components: List[MagicalComponentInterface],
            count: int = 3,
            exclude: List[str] = None
    ) -> List[MagicalComponentInterface]:
        """
        Recomenda componentes baseados na compatibilidade de elementos.

        Args:
            components: Lista atual de componentes
            count: Número de recomendações a retornar
            exclude: Lista de nomes de componentes a serem excluídos

        Returns:
            Lista de componentes recomendados
        """
        exclude = exclude or []

        # Se não há componentes, recomenda aleatoriamente
        if not components:
            available_components = [
                comp for name, comp in self._crafting_system.registered_components.items()
                if name not in exclude
            ]

            if not available_components:
                return []

            # Escolhe 'count' componentes aleatórios
            selected_indices = np.random.choice(
                len(available_components),
                size=min(count, len(available_components)),
                replace=False
            )
            return [available_components[i] for i in selected_indices]

        # Conta a frequência de cada elemento
        element_counts = Counter(comp.element for comp in components)
        dominant_element = element_counts.most_common(1)[0][0]

        # Encontra componentes compatíveis com o elemento dominante
        compatible_items = []

        for name, comp in self._crafting_system.registered_components.items():
            if name not in exclude and comp.name not in [c.name for c in components]:
                compatibility_score = self._calculate_compatibility_score(comp, dominant_element)
                compatible_items.append((comp, compatibility_score))

        # Ordena por compatibilidade e depois por potência
        compatible_items.sort(key=lambda x: (x[1], x[0].power), reverse=True)

        # Retorna os 'count' componentes mais compatíveis
        return [comp for comp, _ in compatible_items[:count]]

    def _calculate_compatibility_score(
            self,
            component: MagicalComponentInterface,
            dominant_element: str
    ) -> int:
        """
        Calcula a pontuação de compatibilidade de um componente com o elemento dominante.

        Args:
            component: Componente a ser avaliado
            dominant_element: Elemento dominante atual

        Returns:
            Pontuação de compatibilidade (maior é melhor)
        """
        if component.element == dominant_element:
            return 3  # Peso maior para o mesmo elemento

        compatible_elements = self._crafting_system.get_compatible_elements(dominant_element)
        if component.element in compatible_elements:
            return 2  # Peso médio para elementos compatíveis

        return 1  # Peso menor para outros elementos

    def explain_recommendation(self, components: List[MagicalComponentInterface]) -> str:
        """
        Explica por que esses componentes foram recomendados.

        Args:
            components: Lista de componentes recomendados

        Returns:
            Explicação em texto
        """
        if not components:
            return "Nenhum componente para explicar."

        # Obtém o elemento dominante
        element_counts = Counter(comp.element for comp in components)
        dominant_element = element_counts.most_common(1)[0][0]

        # Explica com base no elemento dominante
        explanations = {
            "fogo": "Estes componentes têm afinidade com o elemento fogo, que é excelente para magias ofensivas e destrutivas.",
            "água": "Estes componentes têm afinidade com o elemento água, bom para magias de controle, transformação e cura parcial.",
            "terra": "Estes componentes têm afinidade com o elemento terra, ideal para magias defensivas e de fortificação.",
            "ar": "Estes componentes têm afinidade com o elemento ar, que funciona bem para magias de movimento, velocidade e controle do clima.",
            "luz": "Estes componentes têm afinidade com o elemento luz, perfeito para magias de cura, purificação e revelação.",
            "trevas": "Estes componentes têm afinidade com o elemento trevas, poderoso para magias de debilitação, ilusão e manipulação."
        }

        base_explanation = explanations.get(dominant_element,
                                            f"Estes componentes são dominados pelo elemento {dominant_element}.")

        # Adiciona explicação sobre potência
        total_power = sum(comp.power for comp in components)
        if total_power > 20:
            power_level = "muito poderosa"
        elif total_power > 15:
            power_level = "poderosa"
        elif total_power > 10:
            power_level = "moderada"
        else:
            power_level = "básica"

        power_explanation = f"A combinação tem uma potência total de {total_power}, o que deve resultar em uma magia de intensidade {power_level}."

        # Verifica se há raridades elevadas
        rarities = [comp.rarity for comp in components]
        if "lendário" in rarities:
            rarity_explanation = "A presença de um componente lendário pode resultar em efeitos extraordinários ou imprevisíveis."
        elif "épico" in rarities:
            rarity_explanation = "O componente épico aumentará significativamente o poder da magia resultante."
        elif "raro" in rarities:
            rarity_explanation = "Os componentes raros conferem estabilidade e força à magia."
        else:
            rarity_explanation = "Esta é uma combinação relativamente comum, mas ainda eficaz."

        return f"{base_explanation} {power_explanation} {rarity_explanation}"