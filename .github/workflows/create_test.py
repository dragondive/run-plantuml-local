import yaml

test_workflow = {
    "name": "Test",
    "on": ["workflow_call"],
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
