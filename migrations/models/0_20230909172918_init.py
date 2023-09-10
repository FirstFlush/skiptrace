from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "spiderasset" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "spider_name" VARCHAR(255) NOT NULL,
    "file_path" VARCHAR(255) NOT NULL,
    "error_count" SMALLINT NOT NULL  DEFAULT 0,
    "is_active" BOOL NOT NULL  DEFAULT True,
    "date_created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "bank" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS "skip" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "first_name" VARCHAR(255) NOT NULL,
    "last_name" VARCHAR(255) NOT NULL,
    "middle_name" VARCHAR(255),
    "birthday" DATE NOT NULL,
    "date_created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "bankbranch" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "address" VARCHAR(255) NOT NULL,
    "address_2" VARCHAR(255),
    "city" VARCHAR(255) NOT NULL,
    "state" VARCHAR(2) NOT NULL,
    "zipcode" VARCHAR(10) NOT NULL,
    "is_certain" BOOL NOT NULL  DEFAULT False,
    "bank_id_id" INT NOT NULL REFERENCES "bank" ("id") ON DELETE CASCADE,
    "skip_id_id" INT NOT NULL REFERENCES "skip" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "bankbranch"."state" IS 'Alaska: AK\nAlabama: AL\nArkansas: AR\nArizona: AZ\nCalifornia: CA\nColorado: CO\nConnecticut: CT\nDistrict_of_Columbia: DC\nDelaware: DE\nFlorida: FL\nGeorgia: GA\nHawaii: HI\nIowa: IA\nIdaho: ID\nIllinois: IL\nIndiana: IN\nKansas: KS\nKentucky: KY\nLouisiana: LA\nMassachusetts: MA\nMaryland: MD\nMaine: ME\nMichigan: MI\nMinnesota: MN\nMissouri: MO\nMississippi: MS\nMontana: MT\nNorth_Carolina: NC\nNorth_Dakota: ND\nNebraska: NE\nNew_Hampshire: NH\nNew_Jersey: NJ\nNew_Mexico: NM\nNevada: NV\nNew_York: NY\nOhio: OH\nOklahoma: OK\nOregon: OR\nPennsylvania: PA\nRhode_Island: RI\nSouth_Carolina: SC\nSouth_Dakota: SD\nTennessee: TN\nTexas: TX\nUtah: UT\nVirginia: VA\nVermont: VT\nWashington: WA\nWisconsin: WI\nWest_Virginia: WV\nWyoming: WY';
CREATE TABLE IF NOT EXISTS "skipaddress" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "address" VARCHAR(255) NOT NULL,
    "address_2" VARCHAR(255),
    "city" VARCHAR(255) NOT NULL,
    "state" VARCHAR(2) NOT NULL,
    "is_cover" BOOL NOT NULL  DEFAULT False,
    "zipcode" VARCHAR(10) NOT NULL,
    "skip_id_id" INT NOT NULL REFERENCES "skip" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "skipaddress"."state" IS 'Alaska: AK\nAlabama: AL\nArkansas: AR\nArizona: AZ\nCalifornia: CA\nColorado: CO\nConnecticut: CT\nDistrict_of_Columbia: DC\nDelaware: DE\nFlorida: FL\nGeorgia: GA\nHawaii: HI\nIowa: IA\nIdaho: ID\nIllinois: IL\nIndiana: IN\nKansas: KS\nKentucky: KY\nLouisiana: LA\nMassachusetts: MA\nMaryland: MD\nMaine: ME\nMichigan: MI\nMinnesota: MN\nMissouri: MO\nMississippi: MS\nMontana: MT\nNorth_Carolina: NC\nNorth_Dakota: ND\nNebraska: NE\nNew_Hampshire: NH\nNew_Jersey: NJ\nNew_Mexico: NM\nNevada: NV\nNew_York: NY\nOhio: OH\nOklahoma: OK\nOregon: OR\nPennsylvania: PA\nRhode_Island: RI\nSouth_Carolina: SC\nSouth_Dakota: SD\nTennessee: TN\nTexas: TX\nUtah: UT\nVirginia: VA\nVermont: VT\nWashington: WA\nWisconsin: WI\nWest_Virginia: WV\nWyoming: WY';
CREATE TABLE IF NOT EXISTS "skipcompany" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "company_name" VARCHAR(255) NOT NULL,
    "phone" VARCHAR(255),
    "website" VARCHAR(255),
    "skip_id_id" INT NOT NULL REFERENCES "skip" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "skipemail" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "is_cover" BOOL NOT NULL  DEFAULT False,
    "skip_id_id" INT NOT NULL REFERENCES "skip" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "skipphone" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "number" VARCHAR(255) NOT NULL,
    "is_cover" BOOL NOT NULL  DEFAULT False,
    "skip_id_id" INT NOT NULL REFERENCES "skip" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "skiprelative" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "first_name" VARCHAR(255) NOT NULL,
    "last_name" VARCHAR(255) NOT NULL,
    "is_alive" BOOL NOT NULL  DEFAULT True,
    "possible_mmn" BOOL NOT NULL  DEFAULT False,
    "phone" VARCHAR(255),
    "skip_id_id" INT NOT NULL REFERENCES "skip" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "skipsocialmedia" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "website" VARCHAR(255) NOT NULL,
    "username" VARCHAR(255),
    "skip_id_id" INT NOT NULL REFERENCES "skip" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
