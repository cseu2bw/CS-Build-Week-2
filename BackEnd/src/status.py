class Status:
    def __init__(self, name='', cooldown=0, encumbrance=0, strength=0, speed=None, gold=None, bodywear=None, footwear=None, inventory=None, status=None, errors=None, messages=None, abilities=None):
        self.name = name
        self.cooldown = cooldown
        self.encumbrance = encumbrance
        self.strength = strength
        self.speed = speed
        self.gold = gold
        self.bodywear = bodywear
        self.footwear = footwear
        self.inventory = inventory
        self.status = status
        self.errors = errors
        self.messages = messages
        self.abilities = abilities
