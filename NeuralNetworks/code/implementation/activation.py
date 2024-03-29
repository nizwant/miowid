from abc import ABC, abstractmethod
import numpy as np


class Activation(ABC):
    @abstractmethod
    def activation(self, x: np.double) -> np.double:
        pass

    @abstractmethod
    def derivative(self, x: np.double) -> np.double:
        pass


class Sigmoid(Activation):
    def activation(self, x: np.double) -> np.double:
        return 1 / (1 + np.exp(-x))

    def derivative(self, x: np.double) -> np.double:
        return self.activation(x) * (1 - self.activation(x))


class ReLU(Activation):
    def activation(self, x: np.double) -> np.double:
        return np.maximum(0, x)

    def derivative(self, x: float):
        return np.where(x < 0, 0, 1)


class Tanh(Activation):
    def activation(self, x: np.double) -> np.double:
        return np.tanh(x)

    def derivative(self, x: np.double) -> np.double:
        return 1 - np.tanh(x) ** 2


class Softmax(Activation):
    """
    Softmax function is used in the output layer of a neural network for multi-class classification problems.
    It squashes the output of each unit to be between 0 and 1, just like a sigmoid function.
    It also divides each output such that the total sum of the outputs is equal to 1.
    """

    def activation(self, x: np.double) -> np.double:
        if x.ndim == 1:
            exps = np.exp(x - np.max(x))
            return exps / np.sum(exps)
        exps = np.exp(x - x.max(axis=0, keepdims=True))
        return exps / np.sum(exps, axis=0, keepdims=True)

    def derivative(self, x: np.double) -> np.double:
        return self.activation(x) * (1 - self.activation(x))


class Linear(Activation):
    def activation(self, x: np.double) -> np.double:
        return x

    def derivative(self, x: np.double) -> np.double:
        return np.ones_like(x)


class LeakyReLU(Activation):
    def activation(self, x: np.double) -> np.double:
        return np.maximum(0.01 * x, x)

    def derivative(self, x: np.double) -> np.double:
        return np.where(x < 0, 0.01, 1)
