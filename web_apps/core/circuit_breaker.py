import functools
import requests
from datetime import datetime
import http


class State:
    OPEN = 'open'
    CLOSED = 'closed'
    HALF_OPEN = 'half_open'


class RemoteServiceError(Exception):
    pass


class CircuitBreaker:
    def __init__(self, func, exception, failure_threshold=5, delay=5):
        """
        :param func: The function to wrap
        :param exception: The exception to catch
        :param failure_threshold: The number of failures before the circuit is tripped
        :param delay: The number of seconds between 'CLOSED' and 'HALF_OPEN' states
        """
        self.func = func
        self.exception = exception
        self.failure_threshold = failure_threshold
        self.delay = delay
        self.state = State.CLOSED
        self.failure_count = 0
        self.last_failure_time = None

    def update_last_failure_time(self):
        self.last_failure_time = datetime.utcnow().timestamp()

    def set_state(self, state):
        self.state = state

    def increment_failure_count(self):
        self.failure_count += 1

    def handle_circuit_closed(self, *args, **kwargs):
        exceptions = self.exception

        try:
            ret_val = self.func(*args, **kwargs)
            self.update_last_failure_time()
            return ret_val
        except exceptions as e:
            self.increment_failure_count()
            self.update_last_failure_time()

            if self.failure_count >= self.failure_threshold:
                self.set_state(State.OPEN)
            raise RemoteServiceError from e

    def handle_circuit_open(self, *args, **kwargs):
        current_timestamp = datetime.utcnow().timestamp()

        if self.last_failure_time + self.delay >= current_timestamp:
            raise RemoteServiceError(
                f"Service is unavailable. Try again in {self.last_failure_time + self.delay - current_timestamp} seconds")

        self.set_state(State.HALF_OPEN)

        try:
            ret_val = self.func(*args, **kwargs)
            self.set_state(State.CLOSED)
            self.failure_count = 0
            self.update_last_failure_time()

            return ret_val
        except self.exception as e:
            self.set_state(State.OPEN)
            self.update_last_failure_time()
            self.increment_failure_count()
            raise RemoteServiceError from e

    def make_api_call(self, *args, **kwargs):
        if self.state == State.CLOSED:
            return self.handle_circuit_closed(*args, **kwargs)
        if self.state == State.OPEN:
            return self.handle_circuit_open(*args, **kwargs)


class APICircuitBreaker:
    def __init__(self, exceptions=(http.client.RemoteDisconnected, requests.exceptions.ConnectionError, Exception), failure_threshold=5, delay=5):
        self.circuit_breakers = functools.partial(
            CircuitBreaker,
            exception=exceptions,
            failure_threshold=failure_threshold,
            delay=delay)

    def __call__(self, func):
        self.circuit_breakers = self.circuit_breakers(func=func)

        def decorator(*args, **kwargs):
            return self.circuit_breakers.make_api_call(*args, **kwargs)

        return decorator

    def __getattr__(self, attr):
        return getattr(self.circuit_breakers, attr)


def circuit_breaker(func):
    def wrapper(*args, **kwargs):
        return APICircuitBreaker()(func)(*args, **kwargs)
    return wrapper
