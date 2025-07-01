from prefect.runner.storage import GitRepository
from prefect_github import GitHubCredentials
from prefect.client.schemas.schedules import IntervalSchedule
from datetime import timedelta
from prefect import flow




if __name__ == "__main__":

    source = GitRepository(
        url="https://github.com/mygainwell/bps-rpa-automations.git",
        branch="main",
        credentials=GitHubCredentials.load("josh-pat")
    )

    schedule = IntervalSchedule(interval=timedelta(minutes=10))

    # Use the flow.from_source method to deploy the flow.
    flow.from_source(
        source=source,
        entrypoint="main.py:rpa_services_flow"
    ).deploy(
        name="bps-rpa-python-deploy",
        work_pool_name="process-pool",  # Replace with your actual work pool name
        schedule=schedule

    )



