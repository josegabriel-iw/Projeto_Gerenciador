from datetime import datetime

class Tarefa:
    def __init__(self, titulo, descricao, data_limite, prioridade):
        self.titulo = titulo
        self.descricao = descricao
        self.data_limite = data_limite
        self.prioridade = prioridade
        self.concluida = False

    def marcar_concluida(self):
        self.concluida = True

    def exibir_info(self):
        status = 'Concluída' if self.concluida else 'Pendente'
        return f"{self.titulo} - {self.descricao} - Até: {self.data_limite.strftime('%d/%m/%Y')} - Prioridade: {self.prioridade} - {status}"


class TarefaComLembrete(Tarefa):
    def __init__(self, titulo, descricao, data_limite, prioridade, lembrete):
        super().__init__(titulo, descricao, data_limite, prioridade)
        self.lembrete = lembrete

    def exibir_info(self):
        base_info = super().exibir_info()
        return f"{base_info} - Lembrete em: {self.lembrete.strftime('%d/%m/%Y %H:%M')}"
