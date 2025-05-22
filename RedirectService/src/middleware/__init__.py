from .cors import CORS
from .prometheus import Prometheus

middlewares = [
    CORS,
    Prometheus,
]
