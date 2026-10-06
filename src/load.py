from decorators.logger import logger
from sql.queries import QUERIES
from validation import validate_dataframe
import pandas as pd 
from sqlalchemy import bindparam, text


class GitHubLoader:

    def __init__(self, engine):
        self.engine = engine

    def load_all(self, dataframes: dict):

        try:

            with self.engine.begin() as connection:
                issues_df = dataframes.get("issues")
                if issues_df is not None and not issues_df.empty:
                    issue_ids = issues_df["github_issue_id"].tolist()
                    # A changed issue may have lost all labels/assignees. Clear its
                    # old relationship rows before inserting the current snapshot.
                    for table_name in ("issue_labels", "issue_assignees"):
                        statement = text(
                            f"DELETE FROM {table_name} WHERE github_issue_id IN :issue_ids"
                        ).bindparams(bindparam("issue_ids", expanding=True))
                        connection.execute(statement, {"issue_ids": issue_ids})
                
                # here i do the loop  in the table_dataframes coming from layer 
                # loop don't inerterest for the count of tables_df come
                #  
                for table_name, dataframe in dataframes.items():

                    query = QUERIES.get(table_name)

                    if query is None:
                        raise ValueError(
                            f"No SQL query defined for table '{table_name}'."
                        )

                    self._load_dataframe(
                        connection=connection,
                        dataframe=dataframe,
                        query=query,
                        table_name=table_name,
                    )

            logger.info("All tables loaded successfully.")

        except Exception:
            logger.exception("Loading failed.")
            raise

    def _load_dataframe(
        self,
        connection,
        dataframe,
        query,
        table_name,
    ):

        if dataframe is None or dataframe.empty:

            logger.info(
                "%s dataframe is empty. Skipping...",
                table_name,
            )

            return
        
        logger.info("Validating %s dataframe...", table_name)

        validate_dataframe(dataframe, table_name)

        records = (
            dataframe
            .astype(object)
            .where(pd.notnull(dataframe), None)
            .to_dict(orient="records")
        )


        logger.info("Loading table %s",table_name)

        connection.execute(query, records)

        logger.info(
            "%s: %d rows loaded.",
            table_name,
            len(records),
        )
        
        logger.info("Finshed loaded %s", table_name)
