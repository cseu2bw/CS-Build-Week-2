class Room:
  def __init__(self, id=0, exits=None, title=None, description=None, coordinates=None):
    self.id = id
    self.exits = exits
    self.title = title
    self.description = description
    self.coordinates = coordinates