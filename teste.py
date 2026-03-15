from tree.node import Node
from algorithms.dfs import dfs
from algorithms.bfs import bfs


def build_test_tree():

    root = Node(question="Vive na água?")

    root.yes = Node(question="É mamífero?")
    root.no = Node(question="Tem asas?")

    root.yes.yes = Node(answer="Golfinho")
    root.yes.no = Node(answer="Tubarão")

    root.no.yes = Node(answer="Águia")
    root.no.no = Node(answer="Cachorro")

    return root


def play_game(root):

    node = root

    while not node.is_leaf():

        answer = input(f"{node.question} (s/n): ").lower()

        if answer == "s":
            node = node.yes
        else:
            node = node.no

    print(f"\nVocê pensou em: {node.answer}")


def show_dfs(root):

    print("\n=== DFS ===")

    paths = dfs(root)

    for p in paths:
        print(p)


def show_bfs(root):

    print("\n=== BFS ===")

    order = bfs(root)

    for node in order:
        print(node)


def main():

    root = build_test_tree()

    while True:

        print("\n==== MENU ====")
        print("1 - Executar DFS")
        print("2 - Executar BFS")
        print("3 - Jogar")
        print("4 - Sair")

        option = input("Escolha: ")

        if option == "1":
            show_dfs(root)

        elif option == "2":
            show_bfs(root)

        elif option == "3":
            play_game(root)

        elif option == "4":
            print("Encerrando...")
            break

        else:
            print("Opção inválida")


if __name__ == "__main__":
    main()
