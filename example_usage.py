# example_usage.py
"""
Exemplo completo de uso do sistema de crafting de magia.
Demonstra a integração entre os vários componentes.
"""
import os
from spellcrafting.system.spellcrafting_system import SpellcraftingSystem
from spellcrafting.rules.combination_rules import (
    ExplosionRule, HealingRule, ShieldRule, DualityRule, ElementalStormRule
)
from spellcrafting.utils.observers import LoggingObserver, SpellCreationObserver
from spellcrafting.utils.enums import ElementType, RarityType


def create_sample_data(system: SpellcraftingSystem):
    """
    Cria dados de exemplo para o sistema.

    Args:
        system: O sistema de crafting
    """
    # Registra alguns componentes básicos
    print("Registrando componentes...")

    # Componentes de fogo
    system.register_component("Pena de Fênix", "fogo", 8, "raro")
    system.register_component("Essência de Chamas", "fogo", 6, "incomum")
    system.register_component("Carvão Flamejante", "fogo", 4, "comum")
    system.register_component("Pó de Dragão", "fogo", 9, "épico")

    # Componentes de água
    system.register_component("Lágrima de Sereia", "água", 7, "raro")
    system.register_component("Cristal Oceânico", "água", 6, "incomum")
    system.register_component("Alga Mística", "água", 3, "comum")
    system.register_component("Essência Glacial", "água", 8, "épico")

    # Componentes de terra
    system.register_component("Cristal Primordial", "terra", 6, "raro")
    system.register_component("Areia de Encantamentos", "terra", 4, "incomum")
    system.register_component("Rocha de Força", "terra", 3, "comum")
    system.register_component("Diamante Terrano", "terra", 9, "épico")

    # Componentes de ar
    system.register_component("Brisa Etérea", "ar", 5, "incomum")
    system.register_component("Sussurro do Vento", "ar", 7, "raro")
    system.register_component("Pluma de Grifo", "ar", 4, "comum")
    system.register_component("Tornado Engarrafado", "ar", 9, "épico")

    # Componentes de luz
    system.register_component("Fragmento Estelar", "luz", 8, "raro")
    system.register_component("Pétala da Aurora", "luz", 6, "incomum")
    system.register_component("Poeira Luminosa", "luz", 3, "comum")
    system.register_component("Cristal do Sol", "luz", 10, "lendário")

    # Componentes de trevas
    system.register_component("Essência Sombria", "trevas", 7, "raro")
    system.register_component("Cristal Obscuro", "trevas", 5, "incomum")
    system.register_component("Pó de Obsidiana", "trevas", 3, "comum")
    system.register_component("Âmbar Negro", "trevas", 9, "épico")

    print(f"Total de {len(system.get_all_components())} componentes registrados.\n")

    # Registra alguns efeitos básicos
    print("Registrando efeitos...")

    system.register_effect("Explosão de Fogo", "Cria uma explosão de chamas que causa dano em área", 15)
    system.register_effect("Cura Restauradora", "Restaura pontos de vida para o alvo", 12)
    system.register_effect("Escudo Rochoso", "Cria uma barreira protetora que absorve dano", 14)
    system.register_effect("Rajada Cortante", "Dispara uma rajada de ar afiado que causa dano e empurra", 13)
    system.register_effect("Luz Purificadora", "Emite um raio de luz que purifica e cura maldições", 16)
    system.register_effect("Toque das Sombras", "Envolve o alvo em sombras, causando medo e debilitação", 15)
    system.register_effect("Tempestade Elemental", "Cria uma tempestade caótica de energia elemental combinada", 20)
    system.register_effect("Dualidade Arcana", "Manipula o equilíbrio entre luz e trevas", 18)

    print(f"Total de {len(system.get_all_effects())} efeitos registrados.\n")

    # Registra algumas receitas
    print("Registrando receitas...")

    system.register_recipe(
        "Explosão Flamejante",
        ["Pena de Fênix", "Essência de Chamas", "Sussurro do Vento"],
        "Explosão de Fogo"
    )

    system.register_recipe(
        "Restauração Celestial",
        ["Fragmento Estelar", "Pétala da Aurora", "Cristal Oceânico"],
        "Cura Restauradora"
    )

    system.register_recipe(
        "Barreira Terrana",
        ["Cristal Primordial", "Rocha de Força", "Diamante Terrano"],
        "Escudo Rochoso"
    )

    system.register_recipe(
        "Tempestade dos Elementos",
        ["Pena de Fênix", "Lágrima de Sereia", "Cristal Primordial", "Brisa Etérea"],
        "Tempestade Elemental"
    )

    system.register_recipe(
        "Equilíbrio Místico",
        ["Fragmento Estelar", "Essência Sombria", "Brisa Etérea"],
        "Dualidade Arcana"
    )

    print("Receitas registradas com sucesso.\n")

    # Adiciona regras de combinação
    print("Adicionando regras de combinação...")

    system.add_combination_rule(ExplosionRule())
    system.add_combination_rule(HealingRule())
    system.add_combination_rule(ShieldRule())
    system.add_combination_rule(DualityRule())
    system.add_combination_rule(ElementalStormRule())

    print("Regras de combinação adicionadas.\n")


def demonstrate_crafting(system: SpellcraftingSystem):
    """
    Demonstra o uso do sistema para criar magias.

    Args:
        system: O sistema de crafting
    """
    print("\n===== DEMONSTRAÇÃO DE CRAFTING =====\n")

    # Exemplo 1: Criar uma magia usando uma receita
    print("Exemplo 1: Criando uma magia usando uma receita")
    spell1 = system.create_spell(
        "Inferno Explosivo",
        ["Pena de Fênix", "Essência de Chamas", "Sussurro do Vento"]
    )

    print(f"Magia criada: {spell1.name}")
    print(f"Nível: {spell1.level} ({spell1.get_level_description()})")
    print(f"Poder: {spell1.power}")
    print(f"Elemento dominante: {spell1.dominant_element}")
    print(f"Efeito primário: {spell1.primary_effect.name} - {spell1.primary_effect.description}")
    print(f"Requisitos de conjurador: {spell1.get_caster_requirements()}\n")

    # Exemplo 2: Criar uma magia usando uma regra de combinação
    print("Exemplo 2: Criando uma magia usando uma regra de combinação")
    spell2 = system.create_spell(
        "Aura Luminosa",
        ["Fragmento Estelar", "Pétala da Aurora", "Cristal do Sol"]
    )

    print(f"Magia criada: {spell2.name}")
    print(f"Nível: {spell2.level} ({spell2.get_level_description()})")
    print(f"Poder: {spell2.power}")
    print(f"Elemento dominante: {spell2.dominant_element}")
    print(f"Efeito primário: {spell2.primary_effect.name} - {spell2.primary_effect.description}")
    print(f"Requisitos de conjurador: {spell2.get_caster_requirements()}\n")

    # Exemplo 3: Criar uma magia com muitos componentes
    print("Exemplo 3: Criando uma magia com muitos componentes de elementos diferentes")
    spell3 = system.create_spell(
        "Caos Primordial",
        [
            "Pena de Fênix", "Lágrima de Sereia", "Cristal Primordial",
            "Sussurro do Vento", "Fragmento Estelar", "Essência Sombria"
        ]
    )

    print(f"Magia criada: {spell3.name}")
    print(f"Nível: {spell3.level} ({spell3.get_level_description()})")
    print(f"Poder: {spell3.power}")
    print(f"Elemento dominante: {spell3.dominant_element}")
    print(f"Efeito primário: {spell3.primary_effect.name} - {spell3.primary_effect.description}")
    print(f"Requisitos de conjurador: {spell3.get_caster_requirements()}")

    # Mostra efeitos de escalonamento
    if spell3.level > 0:
        print("\nEfeitos de escalonamento:")
        for level, effect in spell3._scaled_effect.items():
            print(
                f"  Nível {level}: Poder {effect['poder']}, Alcance {effect['alcance']} pés, Duração {effect['duracao']} rodadas")
            if effect['efeitos_adicionais']:
                print(f"    Efeitos adicionais: {', '.join(effect['efeitos_adicionais'])}")
    print()

    return [spell1, spell2, spell3]


def demonstrate_ai_features(system: SpellcraftingSystem):
    """
    Demonstra as funcionalidades de IA do sistema.

    Args:
        system: O sistema de crafting
    """
    print("\n===== DEMONSTRAÇÃO DE RECURSOS DE IA =====\n")

    # Treina os modelos de IA
    print("Treinando modelos de IA...")
    success = system.train_ai_models()
    print(f"Treinamento {'bem-sucedido' if success else 'falhou'}\n")

    # Exemplo 1: Recomendação de componentes
    print("Exemplo 1: Recomendação de componentes")
    components = [
        system.get_component("Pena de Fênix"),
        system.get_component("Brisa Etérea")
    ]

    print("Componentes atuais:")
    for comp in components:
        print(f"  - {comp.name} ({comp.element}, Potência: {comp.power}, Raridade: {comp.rarity})")

    recommendations = system.recommend_components(components)

    print("\nComponentes recomendados:")
    for comp in recommendations:
        print(f"  - {comp.name} ({comp.element}, Potência: {comp.power}, Raridade: {comp.rarity})")
    print()

    # Exemplo 2: Previsão de efeito
    print("Exemplo 2: Previsão de efeito")
    prediction_components = [
        system.get_component("Pena de Fênix"),
        system.get_component("Sussurro do Vento"),
        system.get_component("Essência de Chamas")
    ]

    print("Componentes:")
    for comp in prediction_components:
        print(f"  - {comp.name} ({comp.element}, Potência: {comp.power}, Raridade: {comp.rarity})")

    predicted_effect = system.predict_effect(prediction_components)

    print(f"\nEfeito previsto: {predicted_effect.name}")
    print(f"Descrição: {predicted_effect.description}")
    print(f"Poder base: {predicted_effect.base_power}\n")

    # Exemplo 3: Geração de nome de magia
    print("Exemplo 3: Geração de nome de magia")

    name_components = [
        system.get_component("Cristal do Sol"),
        system.get_component("Fragmento Estelar"),
        system.get_component("Pétala da Aurora")
    ]

    effect = system.get_effect("Luz Purificadora")

    print("Componentes:")
    for comp in name_components:
        print(f"  - {comp.name} ({comp.element})")

    print(f"Efeito: {effect.name}")

    spell_names = system._ai_manager.generate_spell_name(name_components, effect, count=3)

    print("\nNomes gerados:")
    for name in spell_names:
        print(f"  - {name}")
    print()


def demonstrate_element_interactions(system: SpellcraftingSystem):
    """
    Demonstra interações entre elementos.

    Args:
        system: O sistema de crafting
    """
    print("\n===== DEMONSTRAÇÃO DE INTERAÇÕES ELEMENTAIS =====\n")

    # Exemplo 1: Informações sobre elementos
    print("Exemplo 1: Informações sobre elementos")

    for element_name in ["fogo", "água", "luz", "trevas"]:
        print(system._element_manager.get_element_description(element_name))
        print()

    # Exemplo 2: Compatibilidades e oposições
    print("Exemplo 2: Compatibilidades e oposições")

    element = "fogo"
    compatibles = system.get_compatible_elements(element)
    opposites = system._element_manager.get_opposing_elements(element)

    print(f"Elemento: {element.capitalize()}")
    print(f"Elementos compatíveis: {', '.join(compatibles)}")
    print(f"Elementos opostos: {', '.join(opposites)}")
    print()

    # Exemplo 3: Bônus elementais
    print("Exemplo 3: Bônus elementais")

    test_combinations = [
        ["fogo", "fogo", "fogo"],  # Mesmo elemento
        ["fogo", "ar", "fogo"],  # Sinergia
        ["fogo", "água", "fogo"],  # Oposição
        ["luz", "trevas", "ar"],  # Combinação rara
        ["fogo", "água", "terra", "ar", "luz"]  # Alta diversidade
    ]

    for combo in test_combinations:
        bonus = system._element_manager.calculate_elemental_bonus(combo)
        print(f"Combinação: {', '.join(combo)}")
        print(f"Bônus elemental: {bonus:.2f}x")
        print()

    # Exemplo 4: Combinações sinérgicas
    print("Exemplo 4: Combinações sinérgicas")

    synergies = system._element_manager.get_synergistic_combinations()
    rares = system._element_manager.get_rare_combinations()

    print("Combinações sinérgicas:")
    for elem1, elem2 in synergies:
        print(f"  - {elem1.capitalize()} + {elem2.capitalize()}")

    print("\nCombinações raras:")
    for elem1, elem2 in rares:
        print(f"  - {elem1.capitalize()} + {elem2.capitalize()}")
    print()


def main():
    """Função principal para demonstrar o uso do sistema."""
    print("Inicializando o sistema de crafting de magia...\n")

    # Cria o diretório de dados
    os.makedirs("data", exist_ok=True)

    # Inicializa o sistema
    system = SpellcraftingSystem(data_directory="data")

    # Adiciona observadores
    logger = LoggingObserver("data/spellcrafting.log")
    spell_observer = SpellCreationObserver()

    system._crafting_system.attach(logger)
    system._crafting_system.attach(spell_observer)

    # Cria dados de exemplo
    create_sample_data(system)

    # Demonstra o crafting
    spells = demonstrate_crafting(system)

    # Demonstra recursos de IA
    demonstrate_ai_features(system)

    # Demonstra interações elementais
    demonstrate_element_interactions(system)

    # Demonstra persistência
    print("\n===== DEMONSTRAÇÃO DE PERSISTÊNCIA =====\n")

    # Salva os dados
    print("Salvando todos os dados...")
    system.save_all_data()

    # Salva uma magia específica
    print("Salvando uma magia específica...")
    system.save_spell(spells[2])

    print("Dados salvos com sucesso em 'data/'.")

    # Mostra estatísticas
    stats = spell_observer.get_stats()
    print("\nEstatísticas de criação de magias:")
    print(f"Total de magias criadas: {stats['spells_created']}")

    print("\nComponentes mais utilizados:")
    for comp, count in stats['top_components']:
        print(f"  - {comp}: {count} usos")

    print("\nDistribuição de elementos:")
    for elem, count in stats['element_distribution'].items():
        print(f"  - {elem.capitalize()}: {count} usos")

    print("\nDemonstração concluída!")


if __name__ == "__main__":
    main()