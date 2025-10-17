#!/usr/bin/env python3

import argparse

import yaml


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output", type=str, help="Output path for the generated workflow file", required=True
    )
    args = parser.parse_args()

    output_path = args.output

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
                    }
                }
            }
        },
        "jobs": {
            "main-branch-default-job": {
                "runs-on": "ubuntu-latest",
                "steps": [
                    {
                        "name": "Default job on main branch",
                        "run": (
                            'echo "::notice::"'
                            '"The default job on the main branch. "'
                            '"The generated dynamic workflows should override it with "'
                            '"one or more jobs."'
                        ),
                    }
                ],
            },
        },
    }

    with open(output_path, "w") as f:
        yaml.dump(dynamic_test_workflow, f)


if __name__ == "__main__":
    main()
