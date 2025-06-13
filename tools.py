from aaaai.agent import Agent
from aaaai.orchestra import Orchestration


a = Agent("this is a simple person number 1", "gemma3:12b")
b = Agent("this is a simple person number 2", "gemma3:12b")
c = Agent("this is a simple person number 3", "gemma3:12b")


orch = Orchestration("gemma3:12b")

orch.register(a)
orch.register(b)
orch.register(c)


print(orch.invoke("who is person 1?"))
