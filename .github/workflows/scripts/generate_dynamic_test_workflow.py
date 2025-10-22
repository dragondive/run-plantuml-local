#!/usr/bin/env python3

import argparse
import re

import yaml
from typing import List, Dict, Tuple

ACTIONS_CHECKOUT_VERSION = "v5.0.0"


def make_step_report_status(status: str, context: str, description: str) -> Dict[str, str]:
    return {
        "name": f"Report '{status}' status to the trigger SHA",
        "if": "${{ always() }}",
        "run": (
            "gh api repos/${{ github.repository }}/statuses/${{ inputs.trigger_sha }} "
            f"--field state={status} "
            f'--field context="{context}" '
            f'--field description="{description} status: {status}" '
        ),
    }


def make_step_checkout() -> Dict[str, str]:
    return {
        "name": "Checkout dynamic workflow",
        "uses": f"actions/checkout@{ACTIONS_CHECKOUT_VERSION}",
        "with": {
            "ref": "${{ github.event.workflow_dispatch.inputs.ref }}",
            "token": "${{ secrets.PAT_ACTIONS }}",
        },
    }


def make_dynamic_test_job(
    job_base_key: str,
    job_base_name: str,
    os: str,
    plantuml_version: str,
    user_steps: List[Dict[str, str]],
) -> Tuple[str, Dict[str, str]]:
    return (
        re.sub(r"[^a-zA-Z0-9_-]", "_", f"{os}-{plantuml_version}-{job_base_key}"),
        {
            "name": f"[{os}, {plantuml_version}]-{job_base_name}",
            "runs-on": os,
            "steps": [
                make_step_report_status(
                    status="pending",
                    context=f"{os}-{plantuml_version}-{job_base_key} (dynamic-test)",
                    description=f"{os}-{plantuml_version}-{job_base_key} (dynamic-test) status: pending"
                ),
                make_step_checkout(),
                *user_steps,
                make_step_report_status(
                    status="${{ steps.result.outcome }}",
                    context=f"{os}-{plantuml_version}-{job_base_key} (dynamic-test)",
                    description=(
                        f"{os}-{plantuml_version}-{job_base_key} (dynamic-test) status: "
                        "${{ steps.result.outcome }}"
                    )
                ),
            ],
        },
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output", type=str, help="Output path for the generated workflow file", required=True
    )
    args = parser.parse_args()

    output_path = args.output

    oses = [
        "ubuntu-24.04", "ubuntu-22.04",
        "macos-26", "macos-15", "macos-14",
        "windows-2025", "windows-2022",
        "ubuntu-24.04-arm", "ubuntu-22.04-arm",
        "windows-11-arm",
    ]

    plantuml_versions = [
        "latest",
        "1.2025.9", "1.2025.8", "1.2025.7", "1.2025.6", "1.2025.5", "1.2025.4",
        "1.2025.3", "1.2025.2", "1.2025.1", "1.2025.0", "1.2024.8", "1.2024.7",
        # "1.2024.6", "1.2024.5", "1.2024.4", "1.2024.3", "1.2024.2", "1.2024.1",
        # "1.2024.0", "1.2023.13", "1.2023.12", "1.2023.11", "1.2023.10", "1.2023.9",
        # "1.2023.8", "1.2023.7", "1.2023.6", "1.2023.5", "1.2023.4", "1.2023.3",
        # "1.2023.2", "1.2023.1", "1.2023.0", "1.2022.14", "1.2022.13", "1.2022.12",
        # "1.2022.11", "1.2022.10", "1.2022.9", "1.2022.8", "1.2022.7", "1.2022.6",
        # "1.2022.5", "1.2022.4", "1.2022.3", "1.2022.2", "1.2022.1", "1.2022.0",
        # "1.2021.16", "1.2021.15", "1.2021.14", "1.2021.13", "1.2021.12",
    ]

    jobs = {}
    for os_ in oses:
        for plantuml_version in plantuml_versions:
            (job_key, job_steps) = make_dynamic_test_job(
                job_base_key="cli-arguments-processed",
                job_base_name="CLI arguments processed",
                os=os_,
                plantuml_version=plantuml_version,
                user_steps=[
                    {
                        "name": "Run plantuml",
                        "uses": "./",
                        "with": {
                            "version": plantuml_version,
                            "cache-plantuml-jar": False,
                            "cli-arguments": (
                                "-tsvg -noerror "
                                "-Dinput_data_file=${{ github.workspace }}/${{ env.diagram-data-path }} "
                                "-Doutput_filename=${{ env.output-filename }} "
                                "-o ${{ github.workspace }} "
                                "${{ github.workspace }}/${{ env.diagram-source-path }}"
                            ),
                            "jvm-options": "",
                        },
                    },
                    {
                        "name": "Check result",
                        "id": "result",
                        "shell": "bash",
                        "run": """
                            if ! [ -f '${{ github.workspace }}/${{ env.output-filename }}.svg' ];
                            then
                                echo "::error::Diagram file not found."
                                exit 1
                            fi

                            if [ "$(awk 'BEGIN {count=0} \
                                    /Hello Alice!/ && /Hello Bob!/ {++count} \
                                    END {print count}' 2>/dev/null \
                                    '${{ github.workspace}}/${{ env.output-filename }}.svg')" -ne 1 ];
                            then
                                echo "::error::Diagram not created correctly."
                                exit 1
                            fi
                        """,
                    },
                ],
            )
            jobs[job_key] = job_steps

    for os_ in oses:
        for plantuml_version in plantuml_versions:
            (job_key, job_steps) = make_dynamic_test_job(
                job_base_key="jvm-arguments-processed",
                job_base_name="JVM arguments processed",
                os=os_,
                plantuml_version=plantuml_version,
                user_steps=[
                    {
                        "name": "Run plantuml",
                        "uses": "./",
                        "with": {
                            "version": plantuml_version,
                            "cache-plantuml-jar": False,
                            "cli-arguments": (
                                "-tpng -noerror -nometadata "
                                "-Dinput_data_file=${{ github.workspace }}/${{ env.diagram-data-path }} "
                                "-Doutput_filename=${{ env.output-filename }} "
                                "-o ${{ github.workspace }} "
                                "${{ github.workspace }}/${{ env.diagram-source-path }}"
                            ),
                            "jvm-options": "-DPLANTUML_LIMIT_SIZE=1",
                        },
                    },
                    {
                        "name": "Check result",
                        "id": "result",
                        "shell": "bash",
                        "run": """
                            if ! [ -f '${{ github.workspace }}/${{ env.output-filename }}.png' ];
                            then
                                echo "::error::Diagram file not found."
                                exit 1
                            fi

                            IMAGE_FILE_SIZE="$(ls -s \
                                '${{ github.workspace }}/${{ env.output-filename }}.png' \
                                | awk '{print $1}')"
                            THRESHOLD_SIZE=200
                            if [ "$IMAGE_FILE_SIZE" -lt 1 ] \
                                    || [ "$IMAGE_FILE_SIZE" -gt "$THRESHOLD_SIZE" ]; then
                                echo "::error::JVM options not processed correctly."
                                exit 1
                            fi
                        """,
                    },
                ],
            )
            jobs[job_key] = job_steps

    dynamic_test_workflow = {
        "name": "dynamic-test: Test the action run-plantuml-local",
        "on": {
            "workflow_dispatch": {
                "inputs": {
                    "ref": {
                        "description": "The git ref where the dynamic test workflow is committed.",
                        "required": True,
                    },
                    "trigger_sha": {
                        "description": "The SHA related to the trigger for this workflow.",
                        "required": True,
                    },
                }
            },
        },
        "env": {
            "GH_TOKEN": "${{ github.token }}",
            "diagram-source-path": ".github/workflows/plantuml/diagram.puml",
            "diagram-data-path": ".github/workflows/plantuml/diagram-data.json",
            "output-filename": "test_plantuml",
        },
        "jobs": jobs,
    }

    with open(output_path, "w") as f:
        yaml.dump(dynamic_test_workflow, f)


if __name__ == "__main__":
    main()
