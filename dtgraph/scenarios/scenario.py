from abc import ABC, abstractmethod

class Scenario(ABC): 
    @staticmethod
    @abstractmethod
    def load(graph, size = None):
        pass