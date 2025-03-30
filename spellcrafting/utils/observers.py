# spellcrafting/utils/observers.py
"""
Implementação de observadores para eventos do sistema.
"""
from typing import Any, List, Dict
from spellcrafting.core import ObserverInterface, SubjectInterface


class Subject(SubjectInterface):
    """
    Implementação base do padrão Observer.
    Permite que observadores se registrem para receber notificações de eventos.
    """

    def __init__(self):
        """Inicializa a classe Subject com uma lista vazia de observadores."""
        self._observers: List[ObserverInterface] = []

    def attach(self, observer: ObserverInterface) -> None:
        """
        Adiciona um observador à lista de observadores.

        Args:
            observer: O observador a ser adicionado
        """
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: ObserverInterface) -> None:
        """
        Remove um observador da lista de observadores.

        Args:
            observer: O observador a ser removido
        """
        self._observers.remove(observer)

    def notify(self, event_type: str, data: Any = None) -> None:
        """
        Notifica todos os observadores sobre um evento.

        Args:
            event_type: Tipo do evento
            data: Dados associados ao evento
        """
        for observer in self._observers:
            observer.update(event_type, data)


class LoggingObserver(ObserverInterface):
    """
    Observador que registra eventos do sistema.
    """

    def __init__(self, log_file: str = None):
        """
        Inicializa o observador de log.

        Args:
            log_file: Caminho para o arquivo de log (opcional)
        """
        self._log_file = log_file
        self._log: List[Dict[str, Any]] = []

    def update(self, event_type: str, data: Any) -> None:
        """
        Registra um evento do sistema.

        Args:
            event_type: Tipo do evento
            data: Dados associados ao evento
        """
        log_entry = {
            'event_type': event_type,
            'data': data
        }

        self._log.append(log_entry)

        # Se um arquivo de log foi especificado, escreve nele
        if self._log_file:
            try:
                with open(self._log_file, 'a') as f:
                    f.write(f"{event_type}: {str(data)}\n")
            except Exception as e:
                print(f"Erro ao escrever no arquivo de log: {e}")
        else:
            print(f"Log: {event_type} - {data}")

    def get_log(self) -> List[Dict[str, Any]]:
        """Retorna o log completo."""
        return self._log.copy()

    def clear_log(self) -> None:
        """Limpa o log."""
        self._log.clear()


class SpellCreationObserver(ObserverInterface):
    """
    Observador específico para eventos de criação de magias.
    Pode ser usado para análise de tendências ou armazenamento de histórico.
    """

    def __init__(self):
        """Inicializa o observador de criação de magias."""
        self._spells_created = 0
        self._component_usage: Dict[str, int] = {}
        self._element_usage: Dict[str, int] = {}

    def update(self, event_type: str, data: Any) -> None:
        """
        Processa eventos relacionados à criação de magias.

        Args:
            event_type: Tipo do evento
            data: Dados associados ao evento
        """
        if event_type == "spell_created" and data:
            self._spells_created += 1

            # Registra o uso de componentes
            if hasattr(data, 'components'):
                for component in data.components:
                    comp_name = component.name
                    self._component_usage[comp_name] = self._component_usage.get(comp_name, 0) + 1

                    elem_name = component.element
                    self._element_usage[elem_name] = self._element_usage.get(elem_name, 0) + 1

    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas sobre magias criadas."""
        top_components = sorted(
            self._component_usage.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]

        top_elements = sorted(
            self._element_usage.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return {
            "spells_created": self._spells_created,
            "top_components": top_components,
            "element_distribution": self._element_usage
        }