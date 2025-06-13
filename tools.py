from aaaai.agent import Agent


class TestAgent(Agent):
    def say_hello(self, person_name: str) -> str:
        """this function say hello to smoeone

        Args:
            person_name (str): target name

        Returns:
            str: what you need say
        """

        return f"Hi {person_name}!"


a = TestAgent("your name is Nora", "gemma3:12b")


response = a.message("say hello to ali")
print(response)
