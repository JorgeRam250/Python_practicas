# Evidencia de seguridad - Distrito Chilaquil

Fecha de verificacion: 2026-03-02
Entorno: local Windows + Poetry

## 1) Herramientas ejecutadas

```powershell
poetry run bandit -q -r src
poetry run safety check
poetry run pip-audit
```

## 2) Resultado resumido

- `bandit`: sin hallazgos en `src`.
- `safety`: sin vulnerabilidades reportadas despues de actualizar FastAPI/Starlette.
- `pip-audit`: sin vulnerabilidades reportadas despues de actualizar FastAPI/Starlette.

## 3) Riesgo historico identificado y remediado

En verificaciones previas existian dos CVE sobre `starlette 0.46.2`:

- `CVE-2025-54121`
- `CVE-2025-62727`

Remediacion aplicada en Fase 8:

- `fastapi` actualizado a `0.135.1`
- `starlette` actualizado a `0.49.3`

## 4) Evidencia tecnica de dependencias

```powershell
poetry show fastapi
poetry show starlette
```

Salida esperada:

- `fastapi 0.135.1`
- `starlette 0.49.3`

## 5) Nota operativa

`safety check` muestra mensaje de deprecacion del comando, pero sigue siendo util como evidencia best-effort.
Para evolucion futura, migrar a `safety scan` segun politicas del equipo.
