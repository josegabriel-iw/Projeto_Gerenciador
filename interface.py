import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from package.gerenciador import GerenciadorTarefas
from package.tarefa import Tarefa, TarefaComLembrete
from package.notificador import Notificador
from package.serializador import Serializador

class Interface(tk.Tk, Notificador, Serializador):
    def __init__(self):
        super().__init__()
        self.title("Gerenciador de Tarefas")
        self.geometry("700x600")
        self.configure(bg='#f0f0f0')
        
        try:
            self.iconbitmap('task_icon.ico')
        except:
            pass
        
        # Configuração de estilo
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Arial', 10), padding=5)
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('TRadiobutton', background='#f0f0f0')
        
        # Frame principal
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(expand=True, fill='both')
        
        # Cabeçalho
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(header_frame, 
                text="Gerenciador de Tarefas", 
                font=('Helvetica', 16, 'bold'),
                foreground='#333333').pack(side='left')
        
        # Controles de filtro e ordenação
        filter_frame = ttk.Frame(main_frame)
        filter_frame.pack(fill='x', pady=5)
        
        self.filter_var = tk.StringVar(value="Todas")
        ttk.Radiobutton(filter_frame, text="Todas", variable=self.filter_var, 
                       value="Todas", command=self.atualizar_lista).pack(side='left', padx=5)
        ttk.Radiobutton(filter_frame, text="Pendentes", variable=self.filter_var, 
                       value="Pendentes", command=self.atualizar_lista).pack(side='left', padx=5)
        ttk.Radiobutton(filter_frame, text="Concluídas", variable=self.filter_var, 
                       value="Concluídas", command=self.atualizar_lista).pack(side='left', padx=5)
        
        ttk.Label(filter_frame, text="Ordenar por:").pack(side='left', padx=(15,5))
        self.sort_var = tk.StringVar()
        self.sort_combobox = ttk.Combobox(filter_frame, textvariable=self.sort_var, 
                                        values=["Prioridade", "Data Limite", "Título"],
                                        state="readonly", width=15)
        self.sort_combobox.pack(side='left')
        self.sort_combobox.bind("<<ComboboxSelected>>", lambda e: self.atualizar_lista())
        
        # Lista de tarefas com scrollbar
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(expand=True, fill='both')
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.lista = tk.Listbox(list_frame, 
                              width=80, 
                              height=20,
                              font=('Arial', 10),
                              yscrollcommand=scrollbar.set,
                              selectbackground='#4a6baf',
                              selectforeground='white',
                              activestyle='none',
                              borderwidth=2,
                              relief='groove')
        self.lista.pack(expand=True, fill='both')
        scrollbar.config(command=self.lista.yview)
        
        # Botões de ação
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        button_style = {'style': 'TButton'}
        self.btn_add = ttk.Button(button_frame, 
                                text="Adicionar Tarefa", 
                                command=self.adicionar_tarefa,
                                **button_style)
        self.btn_add.pack(side='left', padx=5)
        
        self.btn_editar = ttk.Button(button_frame, 
                                   text="Editar Tarefa", 
                                   command=self.editar_tarefa,
                                   **button_style)
        self.btn_editar.pack(side='left', padx=5)
        
        self.btn_concluir = ttk.Button(button_frame, 
                                     text="Marcar como Concluída", 
                                     command=self.marcar_concluida,
                                     **button_style)
        self.btn_concluir.pack(side='left', padx=5)
        
        self.btn_remover = ttk.Button(button_frame,
                                    text="Remover Tarefa",
                                    command=self.remover_tarefa,
                                    **button_style)
        self.btn_remover.pack(side='left', padx=5)
        
        # Barra de status
        self.status_var = tk.StringVar()
        status_bar = ttk.Label(self, 
                             textvariable=self.status_var,
                             relief='sunken',
                             anchor='center',
                             font=('Arial', 9),
                             background='#e0e0e0')
        status_bar.pack(side='bottom', fill='x')
        
        # Inicialização do gerenciador
        self.gerenciador = GerenciadorTarefas()
        self.arquivo = 'tarefas.pkl'
        self.gerenciador.tarefas = self.carregar_de_arquivo(self.arquivo)
        
        self.atualizar_lista()
        self.atualizar_status()
        self.after(5000, self.verificar_notificacoes)

    def atualizar_lista(self):
        self.lista.delete(0, tk.END)
        tarefas = self.gerenciador.listar_tarefas()
        
        # Aplicar filtro
        filtro = self.filter_var.get()
        if filtro == "Pendentes":
            tarefas = [t for t in tarefas if not t.concluida]
        elif filtro == "Concluídas":
            tarefas = [t for t in tarefas if t.concluida]
        
        # Aplicar ordenação
        ordem = self.sort_var.get()
        if ordem == "Prioridade":
            tarefas.sort(key=lambda x: x.prioridade)
        elif ordem == "Data Limite":
            tarefas.sort(key=lambda x: x.data_limite)
        elif ordem == "Título":
            tarefas.sort(key=lambda x: x.titulo.lower())
        
        # Exibir na lista
        for i, t in enumerate(tarefas):
            self.lista.insert(tk.END, t.exibir_info())
            
            # Colorir baseado no status e prioridade
            if t.concluida:
                self.lista.itemconfig(i, {'fg': '#888888'})  # Cinza para concluídas
            else:
                if t.prioridade == 1:
                    self.lista.itemconfig(i, {'fg': '#cc0000'})  # Vermelho para alta prioridade
                elif t.prioridade == 2:
                    self.lista.itemconfig(i, {'fg': '#e68a00'})  # Laranja para média prioridade
                else:
                    self.lista.itemconfig(i, {'fg': '#006600'})  # Verde para baixa prioridade

    def atualizar_status(self):
        total = len(self.gerenciador.tarefas)
        concluidas = sum(1 for t in self.gerenciador.tarefas if t.concluida)
        self.status_var.set(f"Total: {total} | Concluídas: {concluidas} | Pendentes: {total-concluidas}")
        self.after(60000, self.atualizar_status)

    def adicionar_tarefa(self):
        def salvar():
            try:
                titulo = ent_titulo.get()
                descricao = ent_desc.get()
                data_limite = datetime.strptime(ent_data.get(), '%d/%m/%Y')
                prioridade = int(ent_prioridade.get())
                lembrete_str = ent_lembrete.get()

                if lembrete_str:
                    lembrete = datetime.strptime(lembrete_str, '%d/%m/%Y %H:%M')
                    tarefa = TarefaComLembrete(titulo, descricao, data_limite, prioridade, lembrete)
                else:
                    tarefa = Tarefa(titulo, descricao, data_limite, prioridade)

                self.gerenciador.adicionar_tarefa(tarefa)
                self.salvar_em_arquivo(self.arquivo, self.gerenciador.tarefas)
                self.atualizar_lista()
                self.atualizar_status()
                top.destroy()
            except ValueError as e:
                messagebox.showerror("Erro", f"Formato inválido: {str(e)}")

        top = tk.Toplevel(self)
        top.title("Nova Tarefa")
        top.geometry("400x450")
        top.configure(bg='#f0f0f0')
        top.grab_set()
        
        form_frame = ttk.Frame(top, padding="10")
        form_frame.pack(expand=True, fill='both')
        
        # Campos do formulário
        ttk.Label(form_frame, text="Título*:").pack(anchor='w', pady=(5,0))
        ent_titulo = ttk.Entry(form_frame)
        ent_titulo.pack(fill='x', pady=(0,10))
        
        ttk.Label(form_frame, text="Descrição:").pack(anchor='w', pady=(5,0))
        ent_desc = ttk.Entry(form_frame)
        ent_desc.pack(fill='x', pady=(0,10))
        
        ttk.Label(form_frame, text="Data limite (dd/mm/aaaa)*:").pack(anchor='w', pady=(5,0))
        ent_data = ttk.Entry(form_frame)
        ent_data.pack(fill='x', pady=(0,10))
        
        ttk.Label(form_frame, text="Prioridade (1=Alta, 2=Média, 3=Baixa)*:").pack(anchor='w', pady=(5,0))
        ent_prioridade = ttk.Entry(form_frame)
        ent_prioridade.pack(fill='x', pady=(0,10))
        
        ttk.Label(form_frame, text="Lembrete (opcional - dd/mm/aaaa hh:mm):").pack(anchor='w', pady=(5,0))
        ent_lembrete = ttk.Entry(form_frame)
        ent_lembrete.pack(fill='x', pady=(0,15))
        
        # Botões
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(fill='x')
        
        ttk.Button(button_frame, 
                 text="Cancelar", 
                 command=top.destroy,
                 style='TButton').pack(side='right', padx=5)
        
        ttk.Button(button_frame, 
                 text="Salvar", 
                 command=salvar,
                 style='TButton').pack(side='right')

    def editar_tarefa(self):
        selecao = self.lista.curselection()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione uma tarefa para editar")
            return
        
        tarefa = self.gerenciador.tarefas[selecao[0]]
        
        def salvar_edicao():
            try:
                tarefa.titulo = ent_titulo.get()
                tarefa.descricao = ent_desc.get()
                tarefa.data_limite = datetime.strptime(ent_data.get(), '%d/%m/%Y')
                tarefa.prioridade = int(ent_prioridade.get())
                
                if isinstance(tarefa, TarefaComLembrete):
                    lembrete_str = ent_lembrete.get()
                    if lembrete_str:
                        tarefa.lembrete = datetime.strptime(lembrete_str, '%d/%m/%Y %H:%M')
                
                self.salvar_em_arquivo(self.arquivo, self.gerenciador.tarefas)
                self.atualizar_lista()
                top.destroy()
            except ValueError as e:
                messagebox.showerror("Erro", f"Formato inválido: {str(e)}")

        top = tk.Toplevel(self)
        top.title("Editar Tarefa")
        top.geometry("400x450")
        top.configure(bg='#f0f0f0')
        top.grab_set()
        
        form_frame = ttk.Frame(top, padding="10")
        form_frame.pack(expand=True, fill='both')
        
        # Campos do formulário preenchidos
        ttk.Label(form_frame, text="Título*:").pack(anchor='w', pady=(5,0))
        ent_titulo = ttk.Entry(form_frame)
        ent_titulo.insert(0, tarefa.titulo)
        ent_titulo.pack(fill='x', pady=(0,10))
        
        ttk.Label(form_frame, text="Descrição:").pack(anchor='w', pady=(5,0))
        ent_desc = ttk.Entry(form_frame)
        ent_desc.insert(0, tarefa.descricao)
        ent_desc.pack(fill='x', pady=(0,10))
        
        ttk.Label(form_frame, text="Data limite (dd/mm/aaaa)*:").pack(anchor='w', pady=(5,0))
        ent_data = ttk.Entry(form_frame)
        ent_data.insert(0, tarefa.data_limite.strftime('%d/%m/%Y'))
        ent_data.pack(fill='x', pady=(0,10))
        
        ttk.Label(form_frame, text="Prioridade (1=Alta, 2=Média, 3=Baixa)*:").pack(anchor='w', pady=(5,0))
        ent_prioridade = ttk.Entry(form_frame)
        ent_prioridade.insert(0, str(tarefa.prioridade))
        ent_prioridade.pack(fill='x', pady=(0,10))
        
        ttk.Label(form_frame, text="Lembrete (opcional - dd/mm/aaaa hh:mm):").pack(anchor='w', pady=(5,0))
        ent_lembrete = ttk.Entry(form_frame)
        if isinstance(tarefa, TarefaComLembrete):
            ent_lembrete.insert(0, tarefa.lembrete.strftime('%d/%m/%Y %H:%M'))
        ent_lembrete.pack(fill='x', pady=(0,15))
        
        # Botões
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(fill='x')
        
        ttk.Button(button_frame, 
                 text="Cancelar", 
                 command=top.destroy,
                 style='TButton').pack(side='right', padx=5)
        
        ttk.Button(button_frame, 
                 text="Salvar", 
                 command=salvar_edicao,
                 style='TButton').pack(side='right')

    def marcar_concluida(self):
        selecao = self.lista.curselection()
        if selecao:
            self.gerenciador.marcar_concluida(selecao[0])
            self.salvar_em_arquivo(self.arquivo, self.gerenciador.tarefas)
            self.atualizar_lista()
            self.atualizar_status()
        else:
            messagebox.showwarning("Aviso", "Selecione uma tarefa para marcar como concluída")

    def remover_tarefa(self):
        selecao = self.lista.curselection()
        if selecao:
            if messagebox.askyesno("Confirmar", "Deseja realmente remover esta tarefa?"):
                self.gerenciador.remover_tarefa(selecao[0])
                self.salvar_em_arquivo(self.arquivo, self.gerenciador.tarefas)
                self.atualizar_lista()
                self.atualizar_status()
        else:
            messagebox.showwarning("Aviso", "Selecione uma tarefa para remover")

    def verificar_notificacoes(self):
        lembretes = self.verificar_lembretes(self.gerenciador.obter_tarefas_com_lembrete())
        if lembretes:
            try:
                import winsound
                winsound.MessageBeep()
            except:
                pass
            
            for t in lembretes:
                messagebox.showinfo("Lembrete!", f"Tarefa: {t.titulo}\nLembrete para agora!")
        self.after(60000, self.verificar_notificacoes)

def iniciar_interface():
    app = Interface()
    app.mainloop()