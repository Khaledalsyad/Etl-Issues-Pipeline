from config import engine, GITHUB_ORGANIZATION, GITHUB_REPOSITORY
from decorators.logger import logger

from github_client import GitHubGraphqlClaint

from extract import GitHubExtractor
from transform import GitHubTransformer
from load import GitHubLoader

from metadata import (
    get_last_run,
    update_last_run,
)
from uuid import uuid4


def main_pipeline():

    try:

        logger.info("Pipeline started.")

        #################################
        # Initialize Components
        #################################

        client = GitHubGraphqlClaint()

        extractor = GitHubExtractor(client)

        transformer = GitHubTransformer()

        loader = GitHubLoader(engine)

        #################################
        # Metadata
        #################################

        last_run = get_last_run(engine)

        #################################
        # Extract
        #################################

        raw_data = extractor.extract(
            login_organization= GITHUB_ORGANIZATION,
            repository_name= GITHUB_REPOSITORY,
            updated_at= last_run
        )
        if raw_data is None:

            logger.warning("No data extracted.")

            return

        raw_data["pipeline_run_id"] = str(uuid4())

        #################################
        # Transform
        #################################

        dataframes = transformer.transform(
            raw_data,
            last_run,
        )

        if not dataframes:

            logger.warning("No transformed data.")

            return

        #################################
        # Load
        #################################

        loader.load_all(dataframes)

        #################################
        # Update Metadata
        #################################
        def get_max_updated_at(issues):

            if not issues:
                return None

            updated_dates = [
                issue.get("updatedAt")
                for issue in issues
                if issue.get("updatedAt")
            ]

            return max(updated_dates, default=None)

        issues = raw_data.get("issues", [])

        max_updated_at = get_max_updated_at(issues)

        if max_updated_at:
            update_last_run(
                engine,
                max_updated_at,
            )
        logger.info("Pipeline finished successfully.")

    except Exception:

        logger.exception(
            "Pipeline execution failed."
        )

        raise


if __name__ == "__main__":

    main_pipeline()
