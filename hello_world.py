from tdw.controller import Controller

"""
GOAL: Print "hello world".
"""

c = Controller()
print("Hello world")
c.communicate({"$type": "terminate"})
