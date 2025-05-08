from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from . import schemas
from src.skopeo.skopeo import SkopeoClient

app = FastAPI(
    title="Artefact Manager API",
    description="WIP API for managing artefacts using Skopeo.",
    version="0.1.0",
    openapi_tags=[
        {
            "name": "Artefact Management",
            "description": (
                "Operations related to artefact management "
                "registries."
            )
        }
    ]
)


@app.get("/", include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse(url="/docs")


@app.post("/artefact-exists", tags=["Artefact Management"])
def artefact_exists(
    artefact: schemas.PostArtefactExists
) -> schemas.PostArtefactExistsResponse:
    """
    API endpoint to check if a Helm Chart or container image with a specific
    tag exists in a repository.
    """
    try:
        exists = SkopeoClient.artefact_exists(
            registry_url=artefact.registry_url,
            artefact_name=artefact.artefact_name,
            artefact_tag=artefact.artefact_tag,
            registry_username=artefact.registry_username,
            registry_password=artefact.registry_password
        )
        return schemas.PostArtefactExistsResponse(exists=exists)

    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Uncategorized error: " + str(e)
        )


@app.post("/copy-artefact", tags=["Artefact Management"])
def copy_artefact(
    artefact: schemas.PostCopyArtefact
) -> schemas.PostCopyArtefactResponse:
    """
    API Endpoint to copy a Helm Chart/container image from one registry
    to another.
    """
    try:
        dst_name = artefact.dst_artefact_name or artefact.src_artefact_name
        dst_tag = artefact.dst_artefact_tag or artefact.src_artefact_tag

        success = SkopeoClient.copy_artefact(
            src_registry_url=artefact.src_registry_url,
            src_artefact_name=artefact.src_artefact_name,
            src_artefact_tag=artefact.src_artefact_tag,
            dst_registry_url=artefact.dst_registry_url,
            dst_artefact_name=dst_name,
            dst_artefact_tag=dst_tag,
            src_registry_username=artefact.src_registry_username,
            src_registry_password=artefact.src_registry_password,
            dst_registry_username=artefact.dst_registry_username,
            dst_registry_password=artefact.dst_registry_password
        )
        return schemas.PostCopyArtefactResponse(success=success)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


# @app.post("/placeholder")
# def placeholder(
#     artefact: schemas.PostPlaceholder
# ) -> schemas.PostPlaceholderResponse:
#     raise HTTPException(status_code=501, detail="Not implemented")
