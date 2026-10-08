import json
import os
import subprocess
from datetime import datetime


def run_tests():
    result = subprocess.run(
        ["python", "-m", "pytest", "-q"],
        capture_output=True,
        text=True
    )

    return {
        "success": result.returncode == 0,
        "output": result.stdout,
        "errors": result.stderr
    }


def check_required_files():
    required_files = [
        "docker-compose.yml",
        "Dockerfile",
        "requirements.txt",
        ".gitignore",
        "db_init/01_schema.sql",
        "db_init/02_debezium_user.sql",
        "debezium-connector.json",
        "app/cdc/consumer.py",
        "app/cdc/processors/event_processor.py",
        "app/cdc/validators/event_validator.py",
        "app/business/processor.py",
        "app/business/transaction_validator.py",
    ]

    results = {}

    for file_path in required_files:
        results[file_path] = os.path.exists(file_path)

    return results


def generate_report():
    test_result = run_tests()
    file_results = check_required_files()

    report = {
        "project": "Data Pipeline Project",
        "generated_at": datetime.now().isoformat(),
        "tests": {
            "passed": test_result["success"],
            "output": test_result["output"]
        },
        "required_files": file_results,
        "all_required_files_present": all(file_results.values()),
        "overall_status": (
            "PASSED"
            if test_result["success"] and all(file_results.values())
            else "FAILED"
        )
    }

    os.makedirs("reports", exist_ok=True)

    with open(
        "reports/final_validation_report.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(report, file, indent=4)

    return report


if __name__ == "__main__":
    report = generate_report()

    print("=" * 60)
    print("FINAL DATA PIPELINE VALIDATION")
    print("=" * 60)

    print(f"Project: {report['project']}")
    print(f"Status: {report['overall_status']}")
    print(
        f"All required files present: "
        f"{report['all_required_files_present']}"
    )
    print(
        f"Tests passed: "
        f"{report['tests']['passed']}"
    )

    print("=" * 60)

    if report["overall_status"] == "PASSED":
        print("FINAL VALIDATION SUCCESSFUL")
    else:
        print("FINAL VALIDATION FAILED")
        print("Check the test output and missing files.")