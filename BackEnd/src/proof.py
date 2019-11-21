class Proof:
    def __init__(self, proof=0, difficulty=0, cooldown=0.0, messages=[], errors=[]):
        self.proof = proof
        self.difficulty = difficulty
        self.cooldown = cooldown
        self.messages = messages
        self.errors = errors
