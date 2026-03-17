import csv
from tree.node import Node
from tree.avl import AVL


PERGUNTAS = {
    "hair":       "Tem pelo?",
    "feathers":   "Tem penas?",
    "eggs":       "Bota ovos?",
    "milk":       "Amamenta?",
    "airborne":   "Voa?",
    "aquatic":    "É aquático?",
    "predator":   "É predador?",
    "toothed":    "Tem dentes?",
    "backbone":   "Tem espinha dorsal?",
    "breathes":   "Respira ar?",
    "venomous":   "É venenoso?",
    "fins":       "Tem nadadeiras?",
    "tem_pernas": "Tem pernas?",
    "tail":       "Tem cauda?",
    "domestic":   "É doméstico?",
    "catsize":    "É do tamanho de um gato?",
}


def _montar_caminho(row):
    caminho = []
    for col in PERGUNTAS:
        col_csv = "legs" if col == "tem_pernas" else col
        if col_csv in row and row[col_csv] == "1":
            caminho.append(col)
    return caminho


def build_tree(csv_path: str) -> AVL:
    avl = AVL()
    total = 0

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            folha = Node(answer=row["animal_name"])
            caminho = _montar_caminho(row)

            if not caminho:
                avl.insert(folha)
                total += 1
                continue

            no_atual = folha
            for atributo in reversed(caminho):
                no_pergunta = Node(question=PERGUNTAS[atributo])
                no_pergunta.yes = no_atual
                no_atual = no_pergunta

            avl.insert(no_atual)
            total += 1

    if total == 0:
        print("Aviso: nenhum animal carregado. Verifique o zoo.csv.")
    else:
        print(f"{total} animais carregados na árvore.")

    return avl


def add_node(avl: AVL, question: str, answer: str) -> None:
    nova_folha = Node(answer=answer)
    no_pergunta = Node(question=question)
    no_pergunta.yes = nova_folha
    avl.insert(no_pergunta)
