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

    dynamic_test_workflow = {
        "name": "Test the action run-plantuml-local (dynamic edition)",
        "on": {
            "workflow_run": {"workflows": "Generate Dynamic Test Workflow", "types": ["completed"]}
        },
        "jobs": {
            "overridden-job-main-branch": {
                "runs-on": "ubuntu-latest",
                "if": "${{ github.event.workflow_run.conclusion == 'success' }}",
                "steps": [
                    {
                        "name": "Overridden Job",
                        "run": 'echo "::info::This is the overridden job for success case! (main branch)"',
                    }
                ],
            },
            "overridden-job-main-branch-failure": {
                "runs-on": "ubuntu-latest",
                "if": "${{ github.event.workflow_run.conclusion != 'success' }}",
                "steps": [
                    {
                        "name": "Overridden Job Failure",
                        "run": 'echo "::error::This is the overridden job for failure case! (main branch)" && exit 1',
                    }
                ],
            }
        },
    }

    with open(output_path, "w") as f:
        yaml.dump(dynamic_test_workflow, f)


if __name__ == "__main__":
    main()
