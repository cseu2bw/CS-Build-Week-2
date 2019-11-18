class Queue:
  def __init__(self):
      self.storage = list()

  def push(self, value):
      self.storage.append(value)

  def pop(self):
    if self.len() > 0:
      self.storage.pop(0)
    else:
      return None

  def len(self):
      return len(self.storage)

  def __len__(self):
    return self.len()