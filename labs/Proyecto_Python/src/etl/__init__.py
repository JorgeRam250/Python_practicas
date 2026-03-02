"""Capa ETL separada del dominio.

Aqui viviran procesos de staging, dimensiones, hechos y validaciones analiticas.
"""

__all__ = ["extract", "generate_seed", "load", "pipeline", "transform"]
