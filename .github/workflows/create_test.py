import yaml

test_workflow = {
    "name": "Test",
    "on": {
        "workflow_run" :
        {
            "workflows": ["Call Reuse Workflow Experiment"],
            "types": ["completed"]
        }
    },
    "jobs": {
        "say-hello": {
            "runs-on": "ubuntu-latest",
            "steps": [
                {
                    "name": "Greet",
                    "run": 'echo "Hello, World!"',
                }
            ]
        }
    }
}

with open("test-reuse.yml", "w") as f:
    yaml.dump(test_workflow, f)
