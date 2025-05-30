# Gerenciador de Tarefas

Sistema de gerenciamento de tarefas com suporte a prioridades e lembretes, desenvolvido com orientação a objetos.

## Objetivo

Auxiliar o usuário na organização de tarefas do dia a dia, com possibilidade de configurar prazos, prioridades e lembretes. O sistema utiliza uma interface gráfica simples para facilitar a interação.

## ✅ Casos de Uso

### 1. Criar Tarefa
O usuário informa o nome da tarefa, descrição, data limite, prioridade e lembrete (opcional). O sistema salva a tarefa.

### 2. Visualizar Tarefas
O sistema exibe todas as tarefas cadastradas, ordenadas por prioridade e/ou data.

### 3. Editar Tarefa
Não implementado nesta versão.

### 4. Marcar como Concluída
O usuário pode marcar uma tarefa como concluída. Ela continua visível na lista como concluída.

### 5. Excluir Tarefa
Funcionalidade de remoção está presente na classe, mas não está acessível pela interface gráfica nesta versão.

### 6. Notificações
O sistema verifica periodicamente (a cada minuto) lembretes configurados e exibe alertas para o usuário.

## 🛠️ Recursos O.O Utilizados

- **Herança**: `TarefaComLembrete` herda de `Tarefa`.
- **Polimorfismo**: `exibir_info()` sobrescrito em `TarefaComLembrete`.
- **Mixins**: `Notificador` e `Serializador`.
- **Composição forte**: `GerenciadorTarefas` mantém e controla as tarefas.
- **Associação fraca**: Interface acessa `GerenciadorTarefas` e outros pacotes.

## 📁 Estrutura do Projeto

```
GerenciadordeTarefas/
├── main.py
├── README.md
└── package/
    ├── tarefa.py
    ├── gerenciador.py
    ├── notificador.py
    ├── serializador.py
    └── interface.py
```
## 📷 Diagrama de Classes

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#f0f0f0', 'edgeLabelBackground':'#fff', 'tertiaryColor': '#dcd0ff'}}}%%
usecaseDiagram
    title Diagrama de Casos de Uso - TaskManager Pro
    actor Usuário as user
    
    package "Sistema" {
        usecase "Adicionar Tarefa" as UC1
        usecase "Editar Tarefa" as UC2
        usecase "Remover Tarefa" as UC3
        usecase "Marcar como Concluída" as UC4
        usecase "Visualizar Tarefas" as UC5
        usecase "Filtrar Tarefas" as UC6
        usecase "Ordenar Tarefas" as UC7
        usecase "Definir Lembrete" as UC8
        usecase "Receber Notificação" as UC9
        
        user --> UC1
        user --> UC2
        user --> UC3
        user --> UC4
        user --> UC5
        user --> UC6
        user --> UC7
        user --> UC8
        user --> UC9
        
        UC5 --> UC6
        UC5 --> UC7
        
        note right of UC1
        Campos obrigatórios:
        - Título
        - Data limite
        - Prioridade
        end note
        
        note left of UC9
        O sistema verifica
        lembretes a cada minuto
        end note
    }

## 🐍 Requisitos

- Python 3.10+
- tkinter (nativo em instalações padrão do Python)

## ▶️ Execução

```bash
python main.py
```

## 🗃️ Serialização

As tarefas são salvas automaticamente em um arquivo `tarefas.pkl` na raiz do projeto.

---

Desenvolvido para a disciplina de **Orientação a Objetos**, semestre 01/2025  
**Faculdade UnB Gama** - Prof. Henrique Moura
