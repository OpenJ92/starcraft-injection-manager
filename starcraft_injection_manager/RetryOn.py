from asyncio import sleep
from random import uniform
import logging

class RetryOn:
    def __init__(self, exceptions, retries=3, base_delay=1, max_delay=16, jitter=.3):
        """
        Parameters:
        - exceptions: Tuple of exceptions to retry on.
        - retries: Maximum number of retry attempts.
        - base_delay: Initial delay in seconds.
        - max_delay: Maximum delay between retries.
        - jitter: Whether to add randomness to the delay.
        """
        self.exceptions = exceptions
        self.retries = retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.jitter = jitter

    def __call__(self, func):
        async def wrapper(*args, **kwargs):
            attempt = 1
            while True:
                try:
                    return await func(*args, **kwargs)

                except self.exceptions as e:
                    if attempt >= self.retries:
                        # print(f"{func.__name__} failed after {self.retries}")
                        raise

                    delay = uniform(0, self.jitter)
                    print(f"{e.__class__.__name__} on attempt {attempt}:. Retrying in {delay:.2f} seconds...")
                    await sleep(delay)
                    attempt += 1

                except Exception as e:
                    # print(f"Unexpected error in {func.__name__}: {e}")
                    raise

        return wrapper

