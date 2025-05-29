from datetime import datetime

class Notificador:
    def verificar_lembretes(self, tarefas):
        agora = datetime.now()
        lembretes_ativos = []
        for tarefa in tarefas:
            if hasattr(tarefa, 'lembrete') and tarefa.lembrete <= agora and not tarefa.concluida:
                lembretes_ativos.append(tarefa)
        return lembretes_ativos
