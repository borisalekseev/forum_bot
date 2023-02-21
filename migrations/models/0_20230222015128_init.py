from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);
CREATE TABLE IF NOT EXISTS "post" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "text" TEXT NOT NULL,
    "photos" JSON NOT NULL
);
CREATE TABLE IF NOT EXISTS "posttask" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "datetime" TIMESTAMP NOT NULL,
    "topics" TEXT NOT NULL,
    "done" INT NOT NULL  DEFAULT 0,
    "planned" INT NOT NULL  DEFAULT 0,
    "failed" INT NOT NULL  DEFAULT 0,
    "post_id_id" INT NOT NULL REFERENCES "post" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
