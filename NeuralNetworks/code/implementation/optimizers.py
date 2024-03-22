from abc import ABC, abstractmethod
import pandas as pd
import numpy as np


class Optimizer(ABC):
    @abstractmethod
    def optimize(
        self,
        X,
        y,
        initial_solution,
        calculate_gradient,
        learning_rate=0.01,
        max_num_epoch=1000,
        batch_size=1,
        batch_fraction=None,
    ):
        pass

    @staticmethod
    def transfer_data_to_numpy(X, y):
        if isinstance(X, pd.DataFrame) or isinstance(X, pd.Series):
            X = X.to_numpy()
            if len(X.shape) == 1:
                X = X.reshape(-1, 1)
        if isinstance(y, pd.DataFrame) or isinstance(y, pd.Series):
            y = y.to_numpy()
            if len(y.shape) == 1:
                y = y.reshape(-1, 1)
        return X, y

    @staticmethod
    def calculate_batch_size_and_iteration(batch_size, batch_fraction, X):
        """
        Calculate batch size and number of iterations for the optimizer
        If batch_fraction is provided (not None), batch_size is calculated as a fraction of the dataset
        else batch_size is used as provided parameter or default value
        """
        assert type(batch_size) is int, "batch_size must be an integer"
        if batch_fraction is not None:
            assert 0 < batch_fraction <= 1, "batch_fraction must be between 0 and 1"
            batch_size = int(X.shape[0] * batch_fraction)
        iterations = int(X.shape[0] / batch_size)
        return batch_size, iterations


class mini_batch_gradient_descent(Optimizer):

    @staticmethod
    def optimize(
        X,
        y,
        initial_solution,
        calculate_gradient,
        learning_rate=0.01,
        max_num_epoch=1000,
        batch_size=42,
        batch_fraction=None,
    ):
        """
        Performs mini batch gradient descent optimization.

        Parameters:
        - X: Input data.
        - y: Target labels.
        - initial_solution: Initial solution for optimization.
        - calculate_gradient: Function to calculate the gradient.
        - learning_rate: Learning rate for updating the solution (default: 0.01).
        - max_num_iters: Maximum number of iterations (default: 1000).
        - batch_size: Size of the mini batch (default: 1).
        - batch_fraction: Fraction of the data to use in each mini batch (default: None).

        Returns:
        - The optimized solution.
        """

        X, y = Optimizer.transfer_data_to_numpy(X, y)
        batch_size, iterations = Optimizer.calculate_batch_size_and_iteration(
            batch_size, batch_fraction, X
        )

        current_solution = initial_solution

        for _ in range(max_num_epoch):
            N = X.shape[0]
            shuffled_idx = np.random.permutation(N)
            X, y = X[shuffled_idx], y[shuffled_idx]
            for idx in range(iterations):
                X_selected, y_selected = (
                    X[idx * batch_size : (idx + 1) * batch_size],
                    y[idx * batch_size : (idx + 1) * batch_size],
                )
                gradient = calculate_gradient(X_selected, y_selected, current_solution)
                current_solution = current_solution - learning_rate * gradient
            print("Epoch:", current_solution)
        return current_solution


class stochastic_gradient_descent(Optimizer):

    @staticmethod
    def optimize(
        X,
        y,
        initial_solution,
        calculate_gradient,
        learning_rate=0.01,
        max_num_epoch=1000,
    ):
        """
        Performs stochastic gradient descent optimization.

        Parameters:
        - X: Input data.
        - y: Target labels.
        - initial_solution: Initial solution for optimization.
        - calculate_gradient: Function to calculate the gradient.
        - learning_rate: Learning rate for updating the solution (default: 0.01).
        - max_num_iters: Maximum number of iterations (default: 1000).

        Returns:
        - The optimized solution.
        """
        return mini_batch_gradient_descent().optimize(
            X,
            y,
            initial_solution,
            calculate_gradient,
            learning_rate,
            max_num_epoch,
            batch_size=1,
        )


class full_batch_gradient_descent(Optimizer):
    @staticmethod
    def optimize(
        X,
        y,
        initial_solution,
        calculate_gradient,
        learning_rate=0.01,
        max_num_epoch=1000,
    ):
        """
        Performs full batch gradient descent optimization.

        Parameters:
        - X: Input data.
        - y: Target labels.
        - initial_solution: Initial solution for optimization.
        - calculate_gradient: Function to calculate the gradient.
        - learning_rate: Learning rate for updating the solution (default: 0.01).
        - max_num_iters: Maximum number of iterations (default: 1000).

        Returns:
        - The optimized solution.
        """
        return mini_batch_gradient_descent().optimize(
            X,
            y,
            initial_solution,
            calculate_gradient,
            learning_rate,
            max_num_epoch,
            batch_fraction=1,
        )


class mini_batch_gradient_descent_with_momentum(Optimizer):
    @staticmethod
    def optimize(
        X,
        y,
        initial_solution,
        calculate_gradient,
        learning_rate=0.01,
        momentum_decay=0.9,
        max_num_epoch=1000,
        batch_size=1,
        batch_fraction=None,
    ):
        """
        Performs mini batch gradient descent with momentum optimization.

        Parameters:
        - X: Input data.
        - y: Target labels.
        - initial_solution: Initial solution for optimization.
        - calculate_gradient: Function to calculate the gradient.
        - learning_rate: Learning rate for updating the solution (default: 0.01).
        - momentum_decay: Decay rate for the momentum (default: 0.9).
        - max_num_iters: Maximum number of iterations (default: 1000).
        - batch_size: Size of the mini batch (default: 1).
        - batch_fraction: Fraction of the data to use in each mini batch (default: None).

        Returns:
        - The optimized solution.
        """

        X, y = Optimizer.transfer_data_to_numpy(X, y)
        batch_size, iterations = Optimizer.calculate_batch_size_and_iteration(
            batch_size, batch_fraction, X
        )

        current_solution = initial_solution
        momentum = np.zeros_like(initial_solution)

        for _ in range(max_num_epoch):
            N = X.shape[0]
            shuffled_idx = np.random.permutation(N)
            X, y = X[shuffled_idx], y[shuffled_idx]
            for idx in range(iterations):
                X_selected, y_selected = (
                    X[idx * batch_size : (idx + 1) * batch_size],
                    y[idx * batch_size : (idx + 1) * batch_size],
                )
                gradient = calculate_gradient(X_selected, y_selected, current_solution)
                momentum = momentum_decay * momentum - learning_rate * gradient
                current_solution = current_solution + momentum
            print("Epoch:", current_solution)
        return current_solution


class adagrad(Optimizer):

    @staticmethod
    def optimize(
        X,
        y,
        initial_solution,
        calculate_gradient,
        learning_rate=0.01,
        max_num_epoch=1000,
        batch_size=1,
        batch_fraction=None,
        epsilon=1e-8,
    ):
        """
        Performs adagrad optimization.

        Parameters:
        - X: Input data.
        - y: Target labels.
        - initial_solution: Initial solution for optimization.
        - calculate_gradient: Function to calculate the gradient.
        - learning_rate: Learning rate for updating the solution (default: 0.01).
        - max_num_iters: Maximum number of iterations (default: 1000).
        - batch_size: Size of the mini batch (default: 1).
        - batch_fraction: Fraction of the data to use in each mini batch (default: None).
        - epsilon: Small value to avoid division by zero (default: 1e-8).

        Returns:
        - The optimized solution.
        """

        X, y = Optimizer.transfer_data_to_numpy(X, y)
        batch_size, iterations = Optimizer.calculate_batch_size_and_iteration(
            batch_size, batch_fraction, X
        )

        current_solution = initial_solution
        squared_gradients = np.zeros_like(initial_solution)

        for _ in range(max_num_epoch):
            N = X.shape[0]
            shuffled_idx = np.random.permutation(N)
            X, y = X[shuffled_idx], y[shuffled_idx]
            for idx in range(iterations):
                X_selected, y_selected = (
                    X[idx * batch_size : (idx + 1) * batch_size],
                    y[idx * batch_size : (idx + 1) * batch_size],
                )
                gradient = calculate_gradient(X_selected, y_selected, current_solution)
                squared_gradients += gradient**2
                current_solution = current_solution - learning_rate * gradient / (
                    np.sqrt(squared_gradients) + epsilon
                )
            print("Epoch:", current_solution)
        return current_solution


class rmsprop(Optimizer):
    @staticmethod
    def optimize(
        X,
        y,
        initial_solution,
        calculate_gradient,
        learning_rate=0.01,
        squared_gradient_decay=0.99,
        max_num_epoch=1000,
        batch_size=1,
        batch_fraction=None,
        epsilon=1e-8,
    ):
        """
        Performs RMSProp optimization.

        Parameters:
        - X: Input data.
        - y: Target labels.
        - initial_solution: Initial solution for optimization.
        - calculate_gradient: Function to calculate the gradient.
        - learning_rate: Learning rate for updating the solution (default: 0.01).
        - squared_gradient_decay: Decay rate for the squared gradient (default: 0.99).
        - max_num_iters: Maximum number of iterations (default: 1000).
        - batch_size: Size of the mini batch (default: 1).
        - batch_fraction: Fraction of the data to use in each mini batch (default: None).
        - epsilon: Small value to avoid division by zero (default: 1e-8).

        Returns:
        - The optimized solution.
        """

        X, y = Optimizer.transfer_data_to_numpy(X, y)
        batch_size, iterations = Optimizer.calculate_batch_size_and_iteration(
            batch_size, batch_fraction, X
        )

        current_solution = initial_solution
        squared_gradients = np.zeros_like(initial_solution)

        for _ in range(max_num_epoch):
            N = X.shape[0]
            shuffled_idx = np.random.permutation(N)
            X, y = X[shuffled_idx], y[shuffled_idx]
            for idx in range(iterations):
                X_selected, y_selected = (
                    X[idx * batch_size : (idx + 1) * batch_size],
                    y[idx * batch_size : (idx + 1) * batch_size],
                )
                gradient = calculate_gradient(X_selected, y_selected, current_solution)
                squared_gradients = (
                    squared_gradient_decay * squared_gradients
                    + (1 - squared_gradient_decay) * gradient**2
                )
                current_solution = current_solution - learning_rate * gradient / (
                    np.sqrt(squared_gradients) + epsilon
                )
            print("Epoch:", current_solution)
        return current_solution


class adam(Optimizer):
    @staticmethod
    def optimize(
        X,
        y,
        initial_solution,
        neural_network,
        using_backpropagation,
        learning_rate=0.01,
        momentum_decay=0.9,
        squared_gradient_decay=0.99,
        max_num_epoch=1000,
        batch_size=10,
        batch_fraction=None,
        epsilon=1e-8,
    ):
        """
        Performs optimization with adam algorithm.

        Parameters:
        - X: Input data.
        - y: Target labels.
        - initial_solution: Initial solution for optimization.
        - calculate_gradient: Function to calculate the gradient.
        - learning_rate: Learning rate for updating the solution (default: 0.01).
        - momentum_decay: Decay rate for the momentum (default: 0.9).
        - squared_gradient_decay: Decay rate for the squared gradient (default: 0.99).
        - max_num_iters: Maximum number of iterations (default: 1000).
        - batch_size: Size of the mini batch (default: 1).
        - batch_fraction: Fraction of the data to use in each mini batch (default: None).
        - epsilon: Small value to avoid division by zero (default: 1e-8).

        Returns:
        - The optimized solution.
        """

        X, y = Optimizer.transfer_data_to_numpy(X, y)
        batch_size, iterations = Optimizer.calculate_batch_size_and_iteration(
            batch_size, batch_fraction, X
        )

        current_solution = initial_solution
        momentum = np.zeros_like(initial_solution)
        squared_gradients = np.zeros_like(initial_solution)
        counter = 0

        for i in range(max_num_epoch):
            N = X.shape[0]
            shuffled_idx = np.random.permutation(N)
            # X, y = X[shuffled_idx], y[shuffled_idx]
            for idx in range(iterations):
                X_selected, y_selected = (
                    X[idx * batch_size : (idx + 1) * batch_size],
                    y[idx * batch_size : (idx + 1) * batch_size],
                )

                gradient = neural_network.calculate_and_extract_gradient(
                    X_selected, y_selected, current_solution, using_backpropagation
                )
                momentum = momentum_decay * momentum + (1 - momentum_decay) * gradient
                squared_gradients = (
                    squared_gradient_decay * squared_gradients
                    + (1 - squared_gradient_decay) * gradient**2
                )
                counter += 1

                # bias correction
                corrected_momentum = momentum / (1 - momentum_decay**counter)
                corrected_squared_gradients = squared_gradients / (
                    1 - squared_gradient_decay**counter
                )

                current_solution = (
                    current_solution
                    - learning_rate
                    * corrected_momentum
                    / (np.sqrt(corrected_squared_gradients) + epsilon)
                )

            print("Epoch:", i)
        return current_solution
