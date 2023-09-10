from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "skip" ADD "ssn" VARCHAR(9) NOT NULL UNIQUE;
        ALTER TABLE "skipemail" ADD "email" VARCHAR(255) NOT NULL UNIQUE;
        CREATE UNIQUE INDEX "uid_skip_ssn_d2ea60" ON "skip" ("ssn");
        CREATE UNIQUE INDEX "uid_skipemail_email_fe7626" ON "skipemail" ("email");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX "idx_skipemail_email_fe7626";
        DROP INDEX "idx_skip_ssn_d2ea60";
        ALTER TABLE "skip" DROP COLUMN "ssn";
        ALTER TABLE "skipemail" DROP COLUMN "email";"""
