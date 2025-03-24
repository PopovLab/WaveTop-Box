class ErrorModel:
    name:  str = 'Error'
    text: str
    def __init__(self, name:str, text:str):
        self.name = name
        self.text = text
