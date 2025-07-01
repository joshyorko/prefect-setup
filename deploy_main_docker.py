from prefect.runner.storage import GitRepository
from prefect_github import GitHubCredentials
from prefect.client.schemas.schedules import IntervalSchedule
from prefect.docker import DockerImage
from datetime import timedelta
from prefect import flow

if __name__ == "__main__":
    source = GitRepository(
        url="https://github.com/mygainwell/bps-rpa-automations.git",
        branch="main",
        credentials=GitHubCredentials.load("josh-pat")
    )
    docker_image = DockerImage(
        name="ghcr.io/mygainwell/awesome-sauce",
        tag="latest",
        dockerfile="DockerFiles/Dockerfile"
    )
    schedule = IntervalSchedule(interval=timedelta(minutes=10))

    # Attach the spawned container to the 'app-network' so that "action-server" is resolvable
    flow.from_source(
        source=source,
        entrypoint="main.py:rpa_billing_report_flow"
    ).deploy(
        name="bps-rpa-python-deploy",
        work_pool_name="docker-pool",
        image=docker_image,
        schedule=schedule,
        push=True,
        job_variables={
            "image_pull_policy": "Never",  # Use the locally available image
            "networks": ["app-network"]    # Attach to the app-network so "action-server" can be resolved
        }
    )
