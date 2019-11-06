class Instruction:
    def __init__(self, command, value, cs=None):
        self.command = command
        self.value = value
        self.cs = cs
