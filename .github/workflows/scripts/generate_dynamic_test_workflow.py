#!/usr/bin/env python3

import argparse

import yaml


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output", type=str, help="Output path for the generated workflow YAML file", required=True
    )
    args = parser.parse_args()

    output_path = args.output

    oses = [
        "ubuntu-24.04",
        "ubuntu-22.04",
        "macos-15",
        "macos-14",
        "windows-2025",
        "windows-2022",
    ]

    plantuml_versions = [
        "latest",
        "1.2025.8",
        "1.2025.4",
        "1.2025.3",
    ]

    dynamic_test_workflow = {
        "name": "Test the action run-plantuml-local (dynamic edition)",
        "on": {
            "workflow_dispatch": {
                "inputs": {
                    "ref": {
                        "description": "the git ref where the dynamic test workflow is available.",
                        "required": True,
                    },
                    "trigger_sha": {
                        "description": "the sha related to the trigger for this workflow.",
                        "required": True,
                    }
                }
            },
        },
        "env": {
            "GH_TOKEN": "${{ github.token }}"
        },
        "jobs": {
            "cli-generate-diagram": {
                "name": "CLI arguments processed",
                "strategy": {
                    "matrix": {
                        "os": oses,
                        "plantuml_version": plantuml_versions,
                    }
                },
                "runs-on": "${{ matrix.os }}",
                "steps": [
                    {
                        "name": "Report pending status to trigger SHA",
                        "run": (
                            'gh api repos/${{ github.repository }}/statuses/${{ inputs.trigger_sha}} '
                            '--field state=pending '
                            '--field context="test(dynamic): ${{ matrix.os}} - ${{ matrix.plantuml_version }}" '
                            '--field description="test(dynamic): ${{ matrix.os}} - ${{ matrix.plantuml_version }} result: pending"'
                        ),
                    },
                    {
                        "name": "Checkout Dynamic Test Workflow",
                        "uses": "actions/checkout@v5.0.0",
                        "with": {
                            "ref": "${{ github.event.workflow_dispatch.inputs.ref }}",
                            "token": "${{ secrets.PAT_ACTIONS }}",
                        },
                    },
                    {
                        "name": "Hello World",
                        "id": "test-step",
                        "run": 'echo "::info::Hello World from ${{ matrix.os }} with PlantUML version ${{ matrix.plantuml_version }}!"',
                    },
                    {
                        "name": "Report final status to trigger SHA",
                        "if": "(${{ success() }} || ${{ failure() }})",
                        "run": (
                            'gh api repos/${{ github.repository }}/statuses/${{ inputs.trigger_sha}} '
                            '--field state=${{ steps.test-step.outcome }} '
                            '--field context="test(dynamic): ${{ matrix.os}} - ${{ matrix.plantuml_version }}" '
                            '--field description="test(dynamic): ${{ matrix.os}} - ${{ matrix.plantuml_version }} result: ${{ steps.test-step.outcome }}"'
                        )
                    },
                ],
            },
        },
    }

    with open(output_path, "w") as f:
        yaml.dump(dynamic_test_workflow, f)


if __name__ == "__main__":
    main()
