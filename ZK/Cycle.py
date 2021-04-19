from ZK.Answer import Answer
from ZK.Question import Question


class Cycle:

    def __init__(self, id_agent: int, question: Question, b: bool):
        self.id_agent = id_agent
        self.question = question
        self.b = b
        self.answer = {}

    def update_answer(self, id_agent: int, answer: Answer):
        self.answer[id_agent] = answer
