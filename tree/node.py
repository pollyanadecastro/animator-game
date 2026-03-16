class Node:
    def __init__(self, question=None, answer=None):
        self.question = question
        self.answer   = answer
        self.yes      = None
        self.no       = None
        self.height   = 1

    def is_leaf(self):
        return self.yes is None and self.no is None

    def __repr__(self):
        if self.answer is not None:
            return f"[Folha: {self.answer}]"
        return f"[Pergunta: {self.question}]"
