"""Operational continuation-state memory derived from a learned Mealy model."""
from adapter import label


class ModelMismatch(RuntimeError):
    pass


class PredictiveMonitor:
    def __init__(self, model):
        self.model = model
        self.state = model['initial']
        self.positions = {action: i for i, action in enumerate(model['alphabet'])}

    def predict(self, action):
        return self.model['table'][self.state][self.positions[action]][1]

    def observe(self, action, observation):
        destination, expected = self.model['table'][self.state][self.positions[action]]
        if label(observation) != expected:
            raise ModelMismatch('Observed output does not match the learned continuation model')
        self.state = destination
        return self.state
