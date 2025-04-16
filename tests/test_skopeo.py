from src.skopeo.skopeo import SkopeoClient


def test_artefact_exists():
    artefact_exists = SkopeoClient.artefact_exists(
        registry_url="docker.io/library/",
        artefact_name="nginx",
        artefact_tag="latest"
    )
    assert artefact_exists
