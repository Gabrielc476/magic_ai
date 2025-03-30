# spellcrafting/calculators/scaling_calculator.py
"""
Implementação de calculadoras de escalonamento de magia.
"""
from typing import List, Dict, Any, Optional
from ..core.interfaces import ScalingCalculatorInterface, SpellInterface
from ..utils.constants import ELEMENT_SCALING_EFFECTS


class DefaultScalingCalculator(ScalingCalculatorInterface):
    """
    Calculadora padrão para o escalonamento de uma magia.
    Define como os efeitos da magia escalam com níveis de conjuração mais altos.
    """

    def calculate(self, spell: SpellInterface) -> Dict[int, Dict[str, Any]]:
        """
        Calcula o escalonamento da magia.

        Args:
            spell: A magia a ser escalonada

        Returns:
            Dicionário mapeando níveis de conjuração para efeitos escalonados
        """
        if not spell.primary_effect:
            return {}

        base_effect = spell.primary_effect
        base_level = spell.level
        scaling = {}

        # Define como o efeito escala por nível
        for level in range(max(1, base_level), 10):
            # Aumento de poder base escala de forma não linear
            power_increase = base_effect.base_power * (1 + (level - base_level) * 0.5)

            # Aumento de alcance/área de efeito
            base_range = 10  # pés
            increased_area = base_range * (1 + (level - base_level) * 0.3)

            # Aumento de duração
            base_duration = 1  # rodada/minuto
            increased_duration = base_duration * (1 + (level - base_level) * 0.5)

            # Efeitos adicionais baseados no elemento dominante
            additional_effects = []
            if level - base_level >= 2:  # A cada 2 níveis, adiciona um efeito
                element = spell.dominant_element
                if element in ELEMENT_SCALING_EFFECTS:
                    effect_template = ELEMENT_SCALING_EFFECTS[element]
                    additional_effects.append(effect_template.format(magnitude=5 * (level - base_level)))

            scaling[level] = {
                "poder": round(power_increase),
                "alcance": round(increased_area),
                "duracao": round(increased_duration),
                "efeitos_adicionais": additional_effects
            }

        return scaling


class EnhancedScalingCalculator(ScalingCalculatorInterface):
    """
    Calculadora avançada para escalonamento de magia.
    Considera nível, elemento dominante e raridade dos componentes
    para determinar efeitos mais complexos de escalonamento.
    """

    def calculate(self, spell: SpellInterface) -> Dict[int, Dict[str, Any]]:
        """
        Calcula o escalonamento da magia com efeitos mais complexos.

        Args:
            spell: A magia a ser escalonada

        Returns:
            Dicionário mapeando níveis de conjuração para efeitos escalonados
        """
        if not spell.primary_effect:
            return {}

        base_effect = spell.primary_effect
        base_level = spell.level
        scaling = {}

        # Contabiliza a raridade média dos componentes
        rarity_values = {
            "comum": 1.0,
            "incomum": 1.2,
            "raro": 1.5,
            "épico": 2.0,
            "lendário": 3.0
        }

        total_rarity = sum(rarity_values.get(comp.rarity, 1.0) for comp in spell.components)
        rarity_multiplier = total_rarity / len(spell.components)

        # Aplica o mesmo escalonamento básico para poder, alcance e duração
        for level in range(max(1, base_level), 10):
            level_difference = level - base_level

            # Escalonamento de poder baseado na raridade
            power_scale = 1 + (level_difference * 0.4 * rarity_multiplier)
            power_increase = base_effect.base_power * power_scale

            # Escalonamento de alcance
            base_range = 10  # pés
            range_scale = 1 + (level_difference * 0.25 * rarity_multiplier)
            increased_area = base_range * range_scale

            # Escalonamento de duração
            base_duration = 1  # rodada/minuto
            duration_scale = 1 + (level_difference * 0.4 * rarity_multiplier)
            increased_duration = base_duration * duration_scale

            # Efeitos adicionais baseados no elemento dominante
            additional_effects = []

            # Adiciona efeitos com base no nível de escalonamento
            threshold = 3 if "lendário" in [comp.rarity for comp in spell.components] else 2
            if level_difference >= threshold:
                element = spell.dominant_element
                if element in ELEMENT_SCALING_EFFECTS:
                    base_magnitude = 5 * level_difference
                    # Aplica bônus baseado em raridade
                    magnitude = base_magnitude * rarity_multiplier
                    effect_template = ELEMENT_SCALING_EFFECTS[element]
                    additional_effects.append(effect_template.format(magnitude=round(magnitude)))

            # Adiciona efeitos extra em níveis mais altos
            if level_difference >= 4:
                # Determine secondary element effects
                elements = [comp.element for comp in spell.components]
                elements_set = set(elements)

                # Encontra o segundo elemento mais comum
                if len(elements_set) > 1:
                    element_counts = {}
                    for e in elements:
                        element_counts[e] = element_counts.get(e, 0) + 1

                    # Remove o elemento dominante
                    dominant = spell.dominant_element
                    if dominant in element_counts:
                        del element_counts[dominant]

                    # Encontra o segundo mais comum
                    if element_counts:
                        secondary_element = max(element_counts, key=element_counts.get)
                        if secondary_element in ELEMENT_SCALING_EFFECTS:
                            magnitude = 3 * level_difference  # Menor que o efeito primário
                            effect_template = ELEMENT_SCALING_EFFECTS[secondary_element]
                            additional_effects.append(
                                f"Secundário: {effect_template.format(magnitude=round(magnitude))}")

            # Efeitos especiais em níveis muito altos (7+)
            if level >= 7 and base_level < 7:
                # Adiciona um efeito especial para magias de alto nível
                dominant = spell.dominant_element
                special_effects = {
                    "fogo": "Ignora resistência parcial a fogo",
                    "água": "Afeta alvos mesmo parcialmente imersos em água",
                    "terra": "A barreira resiste mesmo a ataques mágicos",
                    "ar": "Efeito afeta criaturas voadoras com desvantagem",
                    "luz": "Efeito dispersa magias de escuridão de nível inferior",
                    "trevas": "Alvo tem desvantagem em salvaguardas contra o efeito"
                }

                if dominant in special_effects:
                    additional_effects.append(special_effects[dominant])

            scaling[level] = {
                "poder": round(power_increase),
                "alcance": round(increased_area),
                "duracao": round(increased_duration),
                "efeitos_adicionais": additional_effects
            }

        return scaling


class ElementalSpecialistScalingCalculator(ScalingCalculatorInterface):
    """
    Calculadora especializada em escalonamento baseado em elementos.
    Cria padrões de escalonamento únicos para cada elemento.
    """

    def calculate(self, spell: SpellInterface) -> Dict[int, Dict[str, Any]]:
        """
        Calcula o escalonamento da magia com especialização elemental.

        Args:
            spell: A magia a ser escalonada

        Returns:
            Dicionário mapeando níveis de conjuração para efeitos escalonados
        """
        if not spell.primary_effect:
            return {}

        base_effect = spell.primary_effect
        base_level = spell.level
        dominant_element = spell.dominant_element
        scaling = {}

        # Define padrões de escalonamento específicos para cada elemento
        element_scaling_patterns = {
            "fogo": {
                "power_factor": 0.6,  # Escalonamento de poder mais agressivo
                "range_factor": 0.3,
                "duration_factor": 0.3,
                "effect_threshold": 1  # Adiciona efeitos adicionais mais cedo
            },
            "água": {
                "power_factor": 0.4,
                "range_factor": 0.4,
                "duration_factor": 0.6,  # Duração mais longa
                "effect_threshold": 2
            },
            "terra": {
                "power_factor": 0.5,
                "range_factor": 0.2,
                "duration_factor": 0.7,  # Duração muito longa
                "effect_threshold": 2
            },
            "ar": {
                "power_factor": 0.4,
                "range_factor": 0.7,  # Alcance muito amplo
                "duration_factor": 0.3,
                "effect_threshold": 2
            },
            "luz": {
                "power_factor": 0.5,
                "range_factor": 0.5,
                "duration_factor": 0.5,
                "effect_threshold": 1
            },
            "trevas": {
                "power_factor": 0.7,  # Escalonamento de poder mais agressivo
                "range_factor": 0.3,
                "duration_factor": 0.4,
                "effect_threshold": 2
            }
        }

        # Usa padrão padrão se o elemento não estiver definido
        pattern = element_scaling_patterns.get(dominant_element, {
            "power_factor": 0.5,
            "range_factor": 0.4,
            "duration_factor": 0.5,
            "effect_threshold": 2
        })

        # Calcula escalonamento para cada nível
        for level in range(max(1, base_level), 10):
            level_difference = level - base_level

            # Escalonamento de poder
            power_increase = base_effect.base_power * (1 + (level_difference * pattern["power_factor"]))

            # Escalonamento de alcance
            base_range = 10  # pés
            increased_area = base_range * (1 + (level_difference * pattern["range_factor"]))

            # Escalonamento de duração
            base_duration = 1  # rodada/minuto
            increased_duration = base_duration * (1 + (level_difference * pattern["duration_factor"]))

            # Efeitos adicionais baseados no elemento dominante
            additional_effects = []

            # Adiciona efeitos com base no limiar específico do elemento
            if level_difference >= pattern["effect_threshold"]:
                # Obtém o modelo de efeito para o elemento
                if dominant_element in ELEMENT_SCALING_EFFECTS:
                    effect_template = ELEMENT_SCALING_EFFECTS[dominant_element]

                    # Calcula a magnitude com base no nível e no elemento
                    magnitude_factors = {
                        "fogo": 6,
                        "água": 4,
                        "terra": 3,
                        "ar": 5,
                        "luz": 4,
                        "trevas": 5
                    }

                    magnitude_factor = magnitude_factors.get(dominant_element, 5)
                    magnitude = magnitude_factor * level_difference

                    additional_effects.append(effect_template.format(magnitude=round(magnitude)))

            # Adiciona efeitos secundários em níveis mais altos
            if level_difference >= 3:
                # Efeitos secundários específicos de elemento
                secondary_effects = {
                    "fogo": [
                        "Alvos em chamas têm desvantagem em ataques",
                        f"Área permanece em chamas por {level_difference} rodadas após conjuração"
                    ],
                    "água": [
                        f"Cria terreno difícil aquático por {level_difference} rodadas",
                        "Apaga fogos não-mágicos na área"
                    ],
                    "terra": [
                        f"Cria terreno difícil por {level_difference} rodadas",
                        "Criaturas na área têm -2 em CA"
                    ],
                    "ar": [
                        "Dispersa gases e névoas",
                        f"Criaturas voadoras têm velocidade reduzida em {5 * level_difference} pés"
                    ],
                    "luz": [
                        "Criaturas sensíveis à luz ficam cegas por 1 rodada",
                        f"Concede visão clara em escuridão mágica por {level_difference} rodadas"
                    ],
                    "trevas": [
                        f"Criaturas na área têm desvantagem em testes de Percepção por {level_difference} rodadas",
                        "Luz não-mágica é suprimida na área"
                    ]
                }

                if dominant_element in secondary_effects:
                    # Adiciona um efeito secundário com base no nível
                    idx = min(len(secondary_effects[dominant_element]) - 1, level_difference - 3)
                    additional_effects.append(secondary_effects[dominant_element][idx])

            scaling[level] = {
                "poder": round(power_increase),
                "alcance": round(increased_area),
                "duracao": round(increased_duration),
                "efeitos_adicionais": additional_effects
            }

        return scaling