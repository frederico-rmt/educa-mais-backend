from psycopg_pool import AsyncConnectionPool
from src.infra.database.database_driver import IDatabaseDriver

class PgDriver(IDatabaseDriver):
  def __init__(self, host: str, port: int, database: str, user: str, password: str):
    super().__init__()
    self._dsn = f"postgresql://{user}:{password}@{host}:{port}/{database}"
    self._pool: AsyncConnectionPool = AsyncConnectionPool(conninfo=self._dsn, min_size=1, max_size=10)

  async def close(self):
    await self._pool.close()

  async def query(self, query, params = ()):
    async with self._pool.connection() as conn:
      async with conn.cursor() as cursor:
        await cursor.execute(query, params)
        if cursor.description:
          return await cursor.fetchall()
        return None