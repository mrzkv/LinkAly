from abc import abstractmethod

from .cors import CORS
from .prometheus import Prometheus

middlewares = (
    CORS,
    Prometheus,
)

