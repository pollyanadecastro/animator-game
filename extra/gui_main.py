#!/usr/bin/env python3
"""
Interface Gráfica para o Sistema Akinator
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sys
import os
import time
from threading import Thread

# Adiciona os caminhos das pastas ao sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), 'tree'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'algorithms'))

from tree.build_tree import build_decision_tree, print_tree
from algorithms.dfs import dfs_traversal, dfs_find_answer, reset_dfs
from algorithms.bfs import bfs_traversal, bfs_find_answer

class AkinatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Akinator - Árvore de Decisão")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)
        
        # Configurar estilo
        self.setup_styles()
        
        # Carregar árvore
        self.tree = None
        self.current_node = None
        self.game_path = []
        
        # Criar interface
        self.create_widgets()
        
        # Carregar dados
        self.load_tree()
        
    def setup_styles(self):
        """Configura estilos e cores da interface"""
        self.bg_color = "#2b2b2b"
        self.fg_color = "#ffffff"
        self.accent_color = "#4a9eff"
        self.success_color = "#4CAF50"
        self.error_color = "#f44336"
        self.warning_color = "#ff9800"
        
        self.root.configure(bg=self.bg_color)
        
        # Configurar estilo ttk
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('Title.TLabel', 
                       background=self.bg_color, 
                       foreground=self.accent_color,
                       font=('Helvetica', 24, 'bold'))
        
        style.configure('Header.TLabel', 
                       background=self.bg_color, 
                       foreground=self.fg_color,
                       font=('Helvetica', 14, 'bold'))
        
        style.configure('Normal.TLabel', 
                       background=self.bg_color, 
                       foreground=self.fg_color,
                       font=('Helvetica', 11))
        
        style.configure('Success.TLabel', 
                       background=self.bg_color, 
                       foreground=self.success_color,
                       font=('Helvetica', 12, 'bold'))
        
        style.configure('Game.TLabel', 
                       background="#3c3c3c", 
                       foreground=self.fg_color,
                       font=('Helvetica', 14, 'bold'),
                       padding=10)
        
        style.configure('Stats.TLabel', 
                       background="#3c3c3c", 
                       foreground=self.fg_color,
                       font=('Courier', 10))
        
        style.configure('Custom.TButton',
                       background=self.accent_color,
                       foreground='black',
                       font=('Helvetica', 11, 'bold'),
                       padding=8)
        
        style.map('Custom.TButton',
                 background=[('active', '#357abd')])
        
        style.configure('Success.TButton',
                       background=self.success_color,
                       foreground='black',
                       font=('Helvetica', 11, 'bold'),
                       padding=8)
        
        style.map('Success.TButton',
                 background=[('active', '#3d8b40')])
        
    def create_widgets(self):
        """Cria todos os widgets da interface"""
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Cabeçalho
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        title = ttk.Label(header_frame, text="🎮 AKINATOR - ÁRVORE DE DECISÃO", style='Title.TLabel')
        title.pack(side=tk.LEFT)
        
        # Frame de status
        self.status_label = ttk.Label(header_frame, text="✅ Sistema pronto!", style='Success.TLabel')
        self.status_label.pack(side=tk.RIGHT)
        
        # Notebook para abas
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Aba do Jogo
        self.create_game_tab()
        
        # Aba de Visualização
        self.create_view_tab()
        
        # Aba de Comparação
        self.create_comparison_tab()
        
        # Aba de Estatísticas
        self.create_stats_tab()
        
        # Barra de progresso
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=(10, 0))
        
    def create_game_tab(self):
        """Cria a aba do jogo principal"""
        game_frame = ttk.Frame(self.notebook)
        self.notebook.add(game_frame, text="🎮 Jogo")
        
        # Frame do jogo
        game_container = ttk.Frame(game_frame)
        game_container.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # Instruções
        instructions = ttk.Label(game_container, 
                                text="Pense em um animal e eu tentarei adivinhar!",
                                style='Header.TLabel')
        instructions.pack(pady=(0, 20))
        
        # Frame da pergunta atual
        question_frame = ttk.Frame(game_container, relief="solid", borderwidth=2)
        question_frame.pack(fill=tk.X, pady=20, ipady=20)
        
        self.question_label = ttk.Label(question_frame, 
                                       text="Clique em 'Iniciar Jogo' para começar",
                                       style='Game.TLabel',
                                       wraplength=800)
        self.question_label.pack(expand=True)
        
        # Frame dos botões de resposta
        button_frame = ttk.Frame(game_container)
        button_frame.pack(pady=20)
        
        self.yes_button = ttk.Button(button_frame, 
                                     text="✅ SIM",
                                     style='Success.TButton',
                                     state='disabled',
                                     command=self.answer_yes)
        self.yes_button.pack(side=tk.LEFT, padx=10)
        
        self.no_button = ttk.Button(button_frame,
                                    text="❌ NÃO",
                                    style='Custom.TButton',
                                    state='disabled',
                                    command=self.answer_no)
        self.no_button.pack(side=tk.LEFT, padx=10)
        
        # Frame de controle
        control_frame = ttk.Frame(game_container)
        control_frame.pack(pady=20)
        
        self.start_button = ttk.Button(control_frame,
                                       text="🎲 Iniciar Jogo",
                                       style='Success.TButton',
                                       command=self.start_game)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.reset_button = ttk.Button(control_frame,
                                       text="🔄 Reiniciar",
                                       style='Custom.TButton',
                                       state='disabled',
                                       command=self.reset_game)
        self.reset_button.pack(side=tk.LEFT, padx=5)
        
        # Histórico do jogo
        history_frame = ttk.LabelFrame(game_container, text="📋 Histórico de Perguntas")
        history_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        self.history_text = scrolledtext.ScrolledText(history_frame,
                                                      height=8,
                                                      bg="#3c3c3c",
                                                      fg=self.fg_color,
                                                      font=('Courier', 10))
        self.history_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
    def create_view_tab(self):
        """Cria a aba de visualização da árvore"""
        view_frame = ttk.Frame(self.notebook)
        self.notebook.add(view_frame, text="🌳 Visualização")
        
        # Botões de controle
        control_frame = ttk.Frame(view_frame)
        control_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(control_frame, 
                  text="📊 Ver DFS",
                  style='Custom.TButton',
                  command=self.show_dfs).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(control_frame,
                  text="📊 Ver BFS",
                  style='Custom.TButton',
                  command=self.show_bfs).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(control_frame,
                  text="🔄 Reset",
                  style='Custom.TButton',
                  command=self.reset_view).pack(side=tk.LEFT, padx=5)
        
        # Área de texto para visualização
        self.view_text = scrolledtext.ScrolledText(view_frame,
                                                   bg="#1e1e1e",
                                                   fg="#d4d4d4",
                                                   font=('Courier', 10))
        self.view_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def create_comparison_tab(self):
        """Cria a aba de comparação"""
        comp_frame = ttk.Frame(self.notebook)
        self.notebook.add(comp_frame, text="⚖️ Comparação")
        
        # Botão de comparar
        ttk.Button(comp_frame,
                  text="🔍 Comparar BFS vs DFS",
                  style='Custom.TButton',
                  command=self.compare_algorithms).pack(pady=20)
        
        # Área de resultado
        self.comp_text = scrolledtext.ScrolledText(comp_frame,
                                                   bg="#1e1e1e",
                                                   fg="#d4d4d4",
                                                   font=('Courier', 10))
        self.comp_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def create_stats_tab(self):
        """Cria a aba de estatísticas"""
        stats_frame = ttk.Frame(self.notebook)
        self.notebook.add(stats_frame, text="📊 Estatísticas")
        
        # Frame para estatísticas
        self.stats_text = scrolledtext.ScrolledText(stats_frame,
                                                    bg="#1e1e1e",
                                                    fg="#d4d4d4",
                                                    font=('Courier', 12))
        self.stats_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Botão atualizar
        ttk.Button(stats_frame,
                  text="🔄 Atualizar Estatísticas",
                  style='Custom.TButton',
                  command=self.show_stats).pack(pady=10)
        
    def load_tree(self):
        """Carrega a árvore de decisão"""
        def load():
            self.progress.start()
            try:
                base_dir = os.path.dirname(os.path.abspath(__file__))
                csv_path = os.path.join(base_dir, 'data', 'zoo.csv')
                
                self.status_label.config(text="⏳ Carregando árvore...")
                self.tree = build_decision_tree(csv_path)
                self.status_label.config(text="✅ Árvore carregada!")
                self.show_stats()
                
            except Exception as e:
                self.status_label.config(text=f"❌ Erro: {str(e)}")
                messagebox.showerror("Erro", f"Falha ao carregar árvore:\n{str(e)}")
            finally:
                self.progress.stop()
        
        Thread(target=load).start()
        
    def start_game(self):
        """Inicia o jogo"""
        if not self.tree:
            messagebox.showwarning("Aviso", "Árvore ainda não carregada!")
            return
        
        self.current_node = self.tree
        self.game_path = []
        self.update_game_display()
        
        self.start_button.config(state='disabled')
        self.reset_button.config(state='normal')
        self.yes_button.config(state='normal')
        self.no_button.config(state='normal')
        
    def reset_game(self):
        """Reseta o jogo"""
        self.current_node = None
        self.game_path = []
        self.question_label.config(text="Clique em 'Iniciar Jogo' para começar")
        self.history_text.delete(1.0, tk.END)
        
        self.start_button.config(state='normal')
        self.reset_button.config(state='disabled')
        self.yes_button.config(state='disabled')
        self.no_button.config(state='disabled')
        
    def update_game_display(self):
        """Atualiza a exibição do jogo"""
        if self.current_node:
            if self.current_node.is_leaf():
                self.question_label.config(text=f"🎉 Eu acho que é: {self.current_node.answer}!")
                self.yes_button.config(state='disabled')
                self.no_button.config(state='disabled')
            else:
                self.question_label.config(text=f"❓ {self.current_node.question}")
                
    def answer_yes(self):
        """Processa resposta SIM"""
        if self.current_node and self.current_node.yes:
            self.game_path.append((self.current_node.question, "SIM"))
            self.history_text.insert(tk.END, f"❓ {self.current_node.question} → ✅ SIM\n")
            self.history_text.see(tk.END)
            
            self.current_node = self.current_node.yes
            self.update_game_display()
            
    def answer_no(self):
        """Processa resposta NÃO"""
        if self.current_node and self.current_node.no:
            self.game_path.append((self.current_node.question, "NÃO"))
            self.history_text.insert(tk.END, f"❓ {self.current_node.question} → ❌ NÃO\n")
            self.history_text.see(tk.END)
            
            self.current_node = self.current_node.no
            self.update_game_display()
            
    def show_dfs(self):
        """Mostra percurso DFS"""
        if not self.tree:
            return
        
        self.view_text.delete(1.0, tk.END)
        self.view_text.insert(tk.END, "📚 PERCURSO DFS (Busca em Profundidade)\n")
        self.view_text.insert(tk.END, "═" * 60 + "\n\n")
        
        # Redireciona print para o texto
        old_stdout = sys.stdout
        sys.stdout = TextRedirector(self.view_text)
        
        reset_dfs()
        dfs_traversal(self.tree)
        
        sys.stdout = old_stdout
        
    def show_bfs(self):
        """Mostra percurso BFS"""
        if not self.tree:
            return
        
        self.view_text.delete(1.0, tk.END)
        self.view_text.insert(tk.END, "📊 PERCURSO BFS (Busca em Largura)\n")
        self.view_text.insert(tk.END, "═" * 60 + "\n\n")
        
        # Redireciona print para o texto
        old_stdout = sys.stdout
        sys.stdout = TextRedirector(self.view_text)
        
        bfs_traversal(self.tree)
        
        sys.stdout = old_stdout
        
    def reset_view(self):
        """Reseta a visualização"""
        self.view_text.delete(1.0, tk.END)
        
    def show_stats(self):
        """Mostra estatísticas da árvore"""
        if not self.tree:
            return
        
        def count_nodes(node):
            if node is None:
                return 0, 0, 0
            
            if node.is_leaf():
                return 1, 0, 1
            
            folhas_yes, internos_yes, prof_yes = count_nodes(node.yes)
            folhas_no, internos_no, prof_no = count_nodes(node.no)
            
            folhas = folhas_yes + folhas_no
            internos = internos_yes + internos_no + 1
            profundidade = max(prof_yes, prof_no) + 1
            
            return folhas, internos, profundidade
        
        folhas, internos, profundidade = count_nodes(self.tree)
        total = folhas + internos
        
        self.stats_text.delete(1.0, tk.END)
        
        stats = f"""
{'📊' * 30}
📊 ESTATÍSTICAS DA ÁRVORE
{'📊' * 30}

🌳 Total de nós: {total}
❓ Nós internos (perguntas): {internos}
📄 Nós folha (respostas): {folhas}
📏 Profundidade máxima: {profundidade}

{'─' * 40}

📋 CARACTERÍSTICAS:
• Cada pergunta é um nó interno
• Cada resposta é uma folha
• A árvore foi construída usando ganho de informação
• O algoritmo escolhe as melhores perguntas primeiro

{'─' * 40}

📈 COMPLEXIDADE:
• DFS: O({profundidade}) de memória
• BFS: O({max(folhas, internos)}) de memória no pior caso
• Altura da árvore: {profundidade} níveis
• Largura máxima: variável por nível
"""
        self.stats_text.insert(tk.END, stats)
        
    def compare_algorithms(self):
        """Compara BFS e DFS"""
        if not self.tree:
            return
        
        self.comp_text.delete(1.0, tk.END)
        self.comp_text.insert(tk.END, "⚖️ COMPARAÇÃO BFS vs DFS\n")
        self.comp_text.insert(tk.END, "═" * 60 + "\n\n")
        
        # Mede tempo DFS
        reset_dfs()
        start = time.time()
        old_stdout = sys.stdout
        sys.stdout = TextRedirector(self.comp_text)
        dfs_traversal(self.tree)
        time_dfs = time.time() - start
        
        self.comp_text.insert(tk.END, f"\n⏱️ Tempo DFS: {time_dfs*1000:.2f}ms\n\n")
        self.comp_text.insert(tk.END, "─" * 40 + "\n\n")
        
        # Mede tempo BFS
        start = time.time()
        bfs_traversal(self.tree)
        time_bfs = time.time() - start
        
        self.comp_text.insert(tk.END, f"\n⏱️ Tempo BFS: {time_bfs*1000:.2f}ms\n\n")
        
        sys.stdout = old_stdout
        
        # Adiciona tabela comparativa
        comparison = f"""
{'📊' * 30}
TABELA COMPARATIVA
{'📊' * 30}

┌─────────────────┬─────────────────┬─────────────────┐
│ Critério        │ DFS             │ BFS             │
├─────────────────┼─────────────────┼─────────────────┤
│ Estrutura       │ Pilha/Recursão  │ Fila            │
│ Exploração      │ Profundidade    │ Largura         │
│ Memória         │ O(altura)       │ O(largura)      │
│ Completa?       │ Sim             │ Sim             │
│ Ótima?          │ Não             │ Sim             │
│ Tempo (ms)      │ {time_dfs*1000:.2f}         │ {time_bfs*1000:.2f}         │
└─────────────────┴─────────────────┴─────────────────┘

💡 ANÁLISE:
• DFS é melhor para jogos interativos
• BFS é melhor para encontrar caminho mínimo
• No Akinator real: usa ambos!
"""
        self.comp_text.insert(tk.END, comparison)

class TextRedirector:
    """Classe para redirecionar print para widget Text"""
    def __init__(self, widget):
        self.widget = widget
        
    def write(self, string):
        self.widget.insert(tk.END, string)
        self.widget.see(tk.END)
        
    def flush(self):
        pass

def main():
    root = tk.Tk()
    app = AkinatorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
