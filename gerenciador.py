from package.tarefa import Tarefa, TarefaComLembrete

class GerenciadorTarefas:
    def __init__(self):
        self.tarefas = []

    def adicionar_tarefa(self, tarefa):
        self.tarefas.append(tarefa)

    def remover_tarefa(self, indice):
        if 0 <= indice < len(self.tarefas):
            del self.tarefas[indice]

    def listar_tarefas(self, incluir_concluidas=True):
        if incluir_concluidas:
            return self.tarefas
        return [t for t in self.tarefas if not t.concluida]

    def marcar_concluida(self, indice):
        if 0 <= indice < len(self.tarefas):
            self.tarefas[indice].marcar_concluida()

    def obter_tarefas_com_lembrete(self):
        return [t for t in self.tarefas if isinstance(t, TarefaComLembrete)]
