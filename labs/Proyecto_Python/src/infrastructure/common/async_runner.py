"""Puente controlado para ejecutar corrutinas desde puertos sincronos."""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable
from concurrent.futures import Future
from threading import Event, Lock, Thread
from typing import TypeVar

T = TypeVar("T")


class _BackgroundEventLoopRunner:
    """Ejecuta corrutinas en un event loop dedicado en segundo plano.

    Comentario para junior:
    - Evita crear/cerrar un loop nuevo en cada llamada.
    - Esto reduce errores de transporte al reutilizar conexiones async (ej. asyncpg).
    """

    def __init__(self) -> None:
        self._lock = Lock()
        self._loop: asyncio.AbstractEventLoop | None = None
        self._thread: Thread | None = None
        self._ready = Event()

    def _start_loop_thread(self) -> None:
        """Inicializa un loop daemon y lo deja listo para ejecutar corrutinas."""

        def _thread_target() -> None:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            self._loop = loop
            self._ready.set()
            loop.run_forever()

            # Cierre ordenado de tareas pendientes al detener el proceso.
            pending = asyncio.all_tasks(loop)
            if pending:
                for task in pending:
                    task.cancel()
                loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()

        self._ready.clear()
        self._thread = Thread(
            target=_thread_target,
            name="dc-async-runner",
            daemon=True,
        )
        self._thread.start()
        self._ready.wait(timeout=5)

    def _get_loop(self) -> asyncio.AbstractEventLoop:
        """Devuelve loop vivo, iniciandolo si es necesario."""
        with self._lock:
            if self._loop is not None and self._thread is not None and self._thread.is_alive():
                return self._loop
            self._start_loop_thread()
            if self._loop is None:
                raise RuntimeError("No fue posible iniciar el event loop en segundo plano.")
            return self._loop

    def run(self, awaitable: Awaitable[T]) -> T:
        """Ejecuta una corrutina en el loop de fondo y espera resultado."""
        loop = self._get_loop()
        future: Future[T] = asyncio.run_coroutine_threadsafe(_as_coroutine(awaitable), loop)
        return future.result()


_BACKGROUND_RUNNER = _BackgroundEventLoopRunner()


def run_sync(awaitable: Awaitable[T]) -> T:
    """Ejecuta una corrutina en contexto sincrono.

    Nota:
    - Este puente existe porque los puertos de aplicacion actuales son sincronos.
    - Si existe un event loop activo en el thread actual, se lanza error explicito.
    """
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return _BACKGROUND_RUNNER.run(awaitable)

    raise RuntimeError(
        "No se puede ejecutar adaptador sincrono con event loop activo. "
        "Use un adaptador asincrono para este contexto."
    )


async def _as_coroutine(awaitable: Awaitable[T]) -> T:
    """Convierte Awaitable generico en corrutina para asyncio.run."""
    return await awaitable
