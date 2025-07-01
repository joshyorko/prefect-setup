from prefect.runner.storage import GitRepository
from prefect_github import GitHubCredentials
from prefect.client.schemas.schedules import IntervalSchedule
from prefect.docker import DockerImage
from datetime import timedelta
from prefect import flow

if __name__ == "__main__":
    source = GitRepository(
        url="https://github.com/joshyorko/cook-with-gas-rpa-challenge.git",
        branch="main",
        credentials=GitHubCredentials.load("josh-pat")
    )
    docker_image = DockerImage(
        name="ghcr.io/joshyorko/cookie-with-gas-prefect-rcc",
        tag="latest",
        dockerfile="rcc_builds/Dockerfile"
    )
    schedule = IntervalSchedule(interval=timedelta(hours=1))

    # Attach the spawned container to the 'app-network' so that "action-server" is resolvable
    flow.from_source(
        source=source,
        entrypoint="main.py:rpaservicesflow"
    ).deploy(
        name="rpaservicesflow-deployment",
        work_pool_name="docker-pool",
        image=docker_image,
        schedule=schedule,
        build=False,
        push=False,
        job_variables={
            "image_pull_policy": "Always",  # Only pull if not available locally
            "networks": ["shared-network"]    # Attach to the app-network so "action-server" can be resolved
        }
    )
