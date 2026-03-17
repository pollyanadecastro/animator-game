from tree.node import Node

# Contador global para DFS
dfs_counter = 0
dfs_path = []

def dfs_traversal(node, depth=0, prefix=""):
    """
    Percorre a árvore em profundidade (DFS) e imprime a ordem de visita.
    Versão recursiva que mostra a estrutura da árvore.
    """
    global dfs_counter, dfs_path
    
    if node is None:
        return
    
    dfs_counter += 1
    node.visited = True
    
    # Indentação para mostrar profundidade
    indent = "  " * depth
    node_info = f"[{dfs_counter}] "
    
    if node.is_leaf():
        print(f"{indent}{node_info}📄 {prefix} Resposta: {node.answer}")
        dfs_path.append(f"Resposta: {node.answer}")
    else:
        print(f"{indent}{node_info}❓ {prefix} {node.question}")
        dfs_path.append(f"Pergunta: {node.question}")
        
        # Percorre primeiro o caminho SIM, depois o NÃO
        if node.yes:
            dfs_traversal(node.yes, depth + 1, "[SIM] ")
        if node.no:
            dfs_traversal(node.no, depth + 1, "[NÃO] ")

def dfs_find_answer(node, caminho=None):
    """
    Usa DFS para encontrar uma resposta baseada nas respostas do usuário.
    Retorna o caminho percorrido e a resposta final.
    """
    if caminho is None:
        caminho = []
    
    if node is None:
        return caminho, "Não encontrei nada"
    
    if node.is_leaf():
        caminho.append(("FIM", node.answer))
        return caminho, node.answer
    
    # Pergunta ao usuário
    print(f"\n❓ {node.question}")
    resposta = input("Responda (s/n): ").lower().strip()
    
    caminho.append((node.question, resposta))
    
    if resposta == 's' and node.yes:
        return dfs_find_answer(node.yes, caminho)
    elif resposta == 'n' and node.no:
        return dfs_find_answer(node.no, caminho)
    else:
        # Se não tem o caminho, pergunta se quer continuar
        print("❌ Caminho não encontrado!")
        return caminho, "Não encontrei uma resposta específica"

def reset_dfs():
    """Reseta os contadores globais do DFS"""
    global dfs_counter, dfs_path
    dfs_counter = 0
    dfs_path = []
