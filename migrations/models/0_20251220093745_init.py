from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "fileasset" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "key" VARCHAR(255) NOT NULL,
    "alt_text" VARCHAR(255),
    "content_type" VARCHAR(100),
    "file_size" INT
);
COMMENT ON TABLE "fileasset" IS 'File model';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "eJztlW9P2zAQxr9KlVcgsQm6MtDehUpom7YisT+ahFDkJtfUqmOH+LK1Q/3u+Jy0TtM0UA"
    "QbnfaOPvecfffDubv1EhWB0K99yHg49t51bj3JEjB/1CIHHY+lqdNJQDYU1sqcZ6gxYyEa"
    "dcSEBiNFoMOMp8iVNKrMhSBRhcbIZeykXPKbHAJUMeAYMhO4ujYylxFMQS9+ppNgxEFEK6"
    "XyiO62eoCz1GofJJ5bI902DEIl8kQ6czrDsZJLN5dIagwSMoZAx2OWU/lUXdnnoqOiUmcp"
    "SqzkRDBiucBKuw9kECpJ/Ew12jYY0y2vuke9k97pm7e9U2OxlSyVk3nRnuu9SLQEBl+9uY"
    "0zZIXDYnTcfkKmqaQ1eP0xy5rpVVJqCE3hdYQLYG0MF4KD6B7OE1FM2DQQIGOkB949Pm5h"
    "9t2/7L/3L/eMa5+6UeYxF298UIa6RYzAOpD0aWwBsbTvJsCjw8MHADSujQBtbBWguRGh+A"
    "ZXIX78cjFohlhJqYH8Jk2DVxEP8aAjuMbrl4m1hSJ1TUUnWt+IKry9z/6POtf+p4szS0Fp"
    "jDN7ij3gzDCmkTmaVD5+EoYsnPxiWRSsRVRXbfKuh5JuUleYZLFlRR1Tf+USOecCfK0Bmz"
    "aMC7YumZGxsaXtvj3j0akde4xX+2/UQv/3zh/fOxOYbTMuS/tujsvn2TcCA4Rpw7xsWTqV"
    "nEehLB/Zv0Wy3CIFii1o1vN2kuizrHKa04HmvxtwbpyNKzn3j8iXgfIJhuRfXc/zO7LCc/"
    "g="
)
