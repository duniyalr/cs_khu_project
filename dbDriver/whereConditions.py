def stringer(v):
    if type(v) is str:
        return f"'{v}'"
    return str(v)

class equal():
    def __init__(self, column_name, value):
        self.column_name = column_name
        self.value = value

    def __str__(self):
        return f'{self.column_name}={stringer(self.value)}'

class greater():
    def __init__(self, column_name, value):
        self.column_name = column_name
        self.value = value
        
    def __str__(self):
        return f'{self.column_name}>{stringer(self.value)}'

class less():
    def __init__(self, column_name, value):
        self.column_name = column_name
        self.value = value
        
    def __str__(self):
        return f'{self.column_name}<{stringer(self.value)}'
