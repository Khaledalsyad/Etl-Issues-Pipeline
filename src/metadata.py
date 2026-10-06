import pandas as pd
from sqlalchemy import text

from decorators.logger import logger
from decorators.timer import timer


PIPELINE_NAME = "issue_pipeline"


@timer
def get_last_run(engine):

    query = text(
        """
        SELECT last_run
        FROM metadata_pipeline
        WHERE pipeline_name = :pipeline_name
        """
    )

    df = pd.read_sql(
        query,
        engine,
        params={
            "pipeline_name": PIPELINE_NAME
        }
    )

    if df.empty:
        logger.info("No previous pipeline run found.")
        return None

    last_run = df.loc[0, "last_run"]

    logger.info(
        "Last pipeline run: %s",
        last_run,
    )

    return last_run


@timer
def update_last_run(
    engine,
    max_updated_at,
):

    if pd.isna(max_updated_at):
        logger.warning(
            "max_updated_at is NULL. Metadata was not updated."
        )
        return

    query = text(
        """
        UPDATE metadata_pipeline
        SET last_run = :last_run,
            updated_at = NOW()
        WHERE pipeline_name = :pipeline_name
        """
    )

    with engine.begin() as connection:

        connection.execute(
            query,
            {
                "last_run": max_updated_at,
                "pipeline_name": PIPELINE_NAME,
            },
        )

    logger.info(
        "Metadata updated successfully: %s",
        max_updated_at,
    )
