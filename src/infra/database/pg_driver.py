from psycopg_pool import AsyncConnectionPool
from src.infra.database.database_driver import IDatabaseDriver

class PgDriver(IDatabaseDriver):
  def __init__(self, host: str, port: int, database: str, user: str, password: str):
    super().__init__()
    self._dsn = f"postgresql://{user}:{password}@{host}:{port}/{database}"
    self._pool = AsyncConnectionPool(
      conninfo=self._dsn,
      min_size=1,
      max_size=10,
      open=False
    )

  def is_pool_open(self) -> bool:
    return hasattr(self._pool, '_closed') and not self._pool._closed

  async def close(self):
    if self.is_pool_open():
      await self._pool.close()

  async def connect(self):
    if not self.is_pool_open():
      await self._pool.open()

  async def query(self, query, params = ()):
    if not self.is_pool_open():
      await self.connect()
    async with self._pool.connection() as conn:
      async with conn.cursor() as cursor:
        await cursor.execute(query, params)
        if cursor.description:
          return await cursor.fetchall()
        return None