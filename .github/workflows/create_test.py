import yaml

test_workflow = {
    "name": "Test",
    "on": ["workflow_dispatch"],
    "jobs": {
        "call-reuse-workflow": {
            "uses": "./.github/workflows/reuse-workflow.yml",
            "with": {
                "who": "Workaround"
            }
        }
    }
}

with open("test-reuse.yml", "w") as f:
    yaml.dump(test_workflow, f)
