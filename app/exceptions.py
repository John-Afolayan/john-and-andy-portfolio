

class MissingField(BaseException):
  "Defines what a missing field exception looks like"

  def __init__(self, error):
    self.error = error;
  
  def get_str(self):
    return f'Invalid {self.error}'