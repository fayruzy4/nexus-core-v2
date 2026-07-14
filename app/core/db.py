from __future__ import annotations

import asyncpg


class DatabasePool:
    _pool: asyncpg.Pool | None = None

    @classmethod
    async def init(cls, dsn: str) -> asyncpg.Pool:
        if cls._pool is None:
            cls._pool = await asyncpg.create_pool(
                dsn=dsn,
                min_size=1,
                max_size=5,
                command_timeout=60,
            )
        return cls._pool

    @classmethod
    def get(cls) -> asyncpg.Pool:
        if cls._pool is None:
            raise RuntimeError('Database pool belum diinisialisasi.')
        return cls._pool

    @classmethod
    async def close(cls) -> None:
        if cls._pool is not None:
            await cls._pool.close()
            cls._pool = None
