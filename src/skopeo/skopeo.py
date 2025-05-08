import json
import subprocess
from typing import Optional


class SkopeoClient:
    """
    Skopeo client that sends requests to the Skopeo CLI to interact with
    artefact registries.
    """

    @staticmethod
    def artefact_exists(
        registry_url: str,
        artefact_name: str,
        artefact_tag: str,
        registry_username: Optional[str] = None,
        registry_password: Optional[str] = None,
    ) -> bool:
        """
        Checks if a specific artefact tag exists in a artefact registry
        registry using Skopeo.

        :param registry_url: The base registry URL including the project
                             (e.g., registry.example.com/project)
        :param artefact_name: The artefact name (e.g., nginx)
        :param artefact_tag: The artefact tag to check (e.g., latest)
        :param registry_username: Optional registry username for authentication
        :param registry_password: Optional password for authentication
        :return: True if the artefact exists, False if it does not.
        :raises RuntimeError: If authentication fails, repository does not
                              exist, or connectivity issues occur.
        """
        full_repo_url = f"{registry_url.rstrip('/')}/{artefact_name}"
        skopeo_command = [
            "skopeo",
            "inspect",
            f"docker://{full_repo_url}:{artefact_tag}",
        ]
        if registry_username and registry_password:
            skopeo_command.extend(
                ["--creds", f"{registry_username}:{registry_password}"]
            )

        try:
            subprocess.run(skopeo_command, check=True, capture_output=True, text=True)
            return True  # If the command succeeds, the artefact exists

        except subprocess.CalledProcessError as e:
            error_message = e.stderr.strip().lower()
            # TODO check HTTP codes for the different errors.
            # Check which built-in exceptions to raise

            if (
                "invalid username/password" in error_message
                or "unauthorized" in error_message
            ):
                raise PermissionError(
                    (("Authentication failed: Invalid username or " "password."))
                )
            if "not found" in error_message:
                raise RuntimeError(
                    (
                        (
                            f"Artefact {artefact_name}:{artefact_tag} not "
                            f"found in {registry_url}"
                        )
                    )
                )

                raise RuntimeError(
                    (f"DNS resolution failed: Unable to resolve " f"'{registry_url}'.")
                )
                raise RuntimeError("Network error: Unable to reach the registry.")

            if (
                "no such host" in error_message
                or "name or service not known" in error_message
            ):
                raise RuntimeError(
                    (f"DNS resolution failed: Unable to resolve " f"'{registry_url}'.")
                )

            return False

        except json.JSONDecodeError:
            raise RuntimeError("Failed to parse Skopeo output")

    @staticmethod
    def copy_artefact(
        src_registry_url: str,
        src_artefact_name: str,
        src_artefact_tag: str,
        dst_registry_url: str,
        dst_artefact_name: str,
        dst_artefact_tag: str,
        src_registry_username: Optional[str] = None,
        src_registry_password: Optional[str] = None,
        dst_registry_username: Optional[str] = None,
        dst_registry_password: Optional[str] = None,
    ) -> bool:
        """
        Copies an artefact from one registry to another using Skopeo.
        """
        src_url = (
            f"docker://{src_registry_url.rstrip('/')}/"
            f"{src_artefact_name}:"
            f"{src_artefact_tag}"
        )
        dst_url = (
            f"docker://{dst_registry_url.rstrip('/')}/"
            f"{dst_artefact_name}:{dst_artefact_tag}"
        )

        skopeo_command = [
            "skopeo",
            "copy",
            src_url,
            dst_url,
        ]

        if src_registry_username and src_registry_password:
            skopeo_command.extend(
                ["--src-creds", f"{src_registry_username}:{src_registry_password}"]
            )

        if dst_registry_username and dst_registry_password:
            skopeo_command.extend(
                ["--dest-creds", f"{dst_registry_username}:{dst_registry_password}"]
            )

        try:
            subprocess.run(skopeo_command, check=True, capture_output=True, text=True)
            return True  # If the command succeeds, the artefact was copied

        except subprocess.CalledProcessError as e:
            error_message = e.stderr.strip().lower()

            if (
                "invalid username/password" in error_message
                or "unauthorized" in error_message
            ):
                raise RuntimeError(
                    "Authentication failed: Invalid username or password."
                )

            if "no such artefact" in error_message:
                raise RuntimeError(
                    (
                        f"Source artefact '{src_artefact_name}:"
                        f"{src_artefact_tag}' not found in '{src_registry_url}'."
                    )
                )

            if (
                "no route to host" in error_message
                or "connection refused" in error_message
            ):
                raise RuntimeError(
                    "Network error: Unable to reach one of the registries."
                )

            if (
                "no such host" in error_message
                or "name or service not known" in error_message
            ):
                raise RuntimeError(
                    f"DNS resolution failed: Unable to resolve "
                    f"'{src_registry_url}' or '{dst_registry_url}'."
                )

            raise RuntimeError(f"Artefact copy failed: {error_message}")
