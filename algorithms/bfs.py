from collections import deque
from tree.node import Node

def bfs_traversal(root):
    """
    Percorre a árvore em largura (BFS) e imprime a ordem de visita.
    Usa uma fila para processamento por níveis.
    """
    if root is None:
        return
    
    print("\n📊 PERCURSO BFS (Busca em Largura):")
    print("═" * 60)
    
    queue = deque([(root, 0, "")])  # (nó, nível, caminho)
    visited_count = 0
    current_level = 0
    level_nodes = []
    all_paths = []
    
    while queue:
        node, level, path = queue.popleft()
        visited_count += 1
        
        # Se mudou de nível, imprime o nível anterior
        if level > current_level:
            print(f"\n📌 Nível {current_level}:")
            for item in level_nodes:
                print(f"   {item}")
            level_nodes = []
            current_level = level
        
        # Prepara informação do nó
        if node.is_leaf():
            node_info = f"📄 {node.answer}"
        else:
            node_info = f"❓ {node.question}"
        
        level_nodes.append(f"[{visited_count}] {node_info}")
        
        # Adiciona filhos na fila com seus caminhos
        if node.yes:
            new_path = path + f" → SIM: {node.question[:20]}..." if path else f"SIM: {node.question[:20]}..."
            queue.append((node.yes, level + 1, new_path))
        if node.no:
            new_path = path + f" → NÃO: {node.question[:20]}..." if path else f"NÃO: {node.question[:20]}..."
            queue.append((node.no, level + 1, new_path))
        
        if node.is_leaf():
            all_paths.append((path, node.answer))
    
    # Imprime o último nível
    if level_nodes:
        print(f"\n📌 Nível {current_level}:")
        for item in level_nodes:
            print(f"   {item}")
    
    print(f"\n📊 Total de nós visitados: {visited_count}")
    
    # Mostra todos os caminhos possíveis
    print("\n🛤️  TODOS OS CAMINHOS POSSÍVEIS:")
    print("═" * 60)
    for i, (path, answer) in enumerate(all_paths, 1):
        print(f"\nCaminho {i}: {path} → 📄 {answer}")

def bfs_find_answer(root):
    """
    Usa BFS para encontrar respostas possíveis.
    Mostra todas as opções em cada nível antes de aprofundar.
    """
    if root is None:
        return
    
    print("\n🔍 EXPLORANDO POSSIBILIDADES COM BFS:")
    print("═" * 60)
    
    queue = deque([(root, [], 0)])  # (nó, caminho, nível)
    respostas_encontradas = []
    
    while queue:
        node, path, level = queue.popleft()
        
        if node.is_leaf():
            respostas_encontradas.append((path, node.answer, level))
            print(f"\n✨ Resposta encontrada no nível {level}: {node.answer}")
            print(f"   Caminho: {' → '.join(path)}")
        else:
            # Adiciona filhos na fila
            if node.yes:
                new_path = path + [f"{node.question} (SIM)"]
                queue.append((node.yes, new_path, level + 1))
            if node.no:
                new_path = path + [f"{node.question} (NÃO)"]
                queue.append((node.no, new_path, level + 1))
    
    # Estatísticas
    print(f"\n📊 ESTATÍSTICAS BFS:")
    print(f"   Total de respostas encontradas: {len(respostas_encontradas)}")
    niveis = [r[2] for r in respostas_encontradas]
    if niveis:
        print(f"   Menor caminho: {min(niveis)} perguntas")
        print(f"   Maior caminho: {max(niveis)} perguntas")
        print(f"   Média de perguntas: {sum(niveis)/len(niveis):.1f}")
