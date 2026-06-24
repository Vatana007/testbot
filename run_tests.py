import os
import sys
import time
import subprocess
import unittest

# Colors for terminal printing
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"


def print_header(title: str):
    print("==================================================")
    print(f"   {title}")
    print("==================================================")


def run_unit_tests() -> bool:
    print_header("Running Unit Test Suites")
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir="tests", pattern="test_*_unit.py")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


def run_e2e_simulation() -> bool:
    print_header("Running E2E Simulation Test")
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir="tests", pattern="test_e2e_simulation.py")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


def run_api_test_suite(api_base: str, admin_user: str, admin_pass: str) -> bool:
    import httpx
    client = httpx.Client(timeout=10.0)

    def report(success: bool, step: str, detail: str = ""):
        if success:
            print(f"[{GREEN}PASS{RESET}] {step} {detail}")
        else:
            print(f"[{RED}FAIL{RESET}] {step} {detail}")
        return success

    # 1. Health Check
    try:
        resp = client.get(f"{api_base}/health")
        if resp.status_code == 200 and resp.json().get("status") == "ok":
            report(True, "Health Check", "-> /health responded successfully")
        else:
            if not report(False, "Health Check", f"-> Unexpected response: {resp.status_code}"):
                return False
    except Exception as e:
        if not report(False, "Health Check", f"-> Could not connect to API: {e}"):
            return False

    # 2. Admin Authentication
    token = None
    try:
        resp = client.post(
            f"{api_base}/api/auth/login",
            data={"username": admin_user, "password": admin_pass}
        )
        if resp.status_code == 200:
            token_data = resp.json()
            token = token_data.get("access_token")
            report(True, "Admin Login", "-> Received JWT access token successfully")
        else:
            if not report(False, "Admin Login", f"-> Failed with status {resp.status_code}: {resp.text}"):
                return False
    except Exception as e:
        if not report(False, "Admin Login", f"-> Exception occurred: {e}"):
            return False

    headers = {"Authorization": f"Bearer {token}"}

    # 3. Create Class (Happy Path)
    test_class_code = "TEST99"
    test_class_id = None
    try:
        cls_list_resp = client.get(f"{api_base}/api/classes")
        if cls_list_resp.status_code == 200:
            for cls in cls_list_resp.json():
                if cls["code"] == test_class_code:
                    client.delete(f"{api_base}/api/classes/{cls['id']}", headers=headers)
                    
        resp = client.post(
            f"{api_base}/api/classes",
            json={"name": "Test Grade 99", "code": test_class_code},
            headers=headers
        )
        if resp.status_code == 201:
            test_class_id = resp.json().get("id")
            report(True, "Create Class", f"-> Created class '{test_class_code}' (ID: {test_class_id})")
        else:
            if not report(False, "Create Class", f"-> Failed: {resp.text}"):
                return False
    except Exception as e:
        if not report(False, "Create Class", f"-> Exception occurred: {e}"):
            return False

    # 4. Get Classes
    try:
        resp = client.get(f"{api_base}/api/classes")
        if resp.status_code == 200: 
            classes = resp.json()
            found = any(c["code"] == test_class_code for c in classes)
            if not report(found, "List Classes", f"-> Found '{test_class_code}' in database classes list"):
                return False
        else:
            if not report(False, "List Classes", f"-> Failed: {resp.text}"):
                return False
    except Exception as e:
        if not report(False, "List Classes", f"-> Exception: {e}"):
            return False

    # 5. Submit Homework
    homework_id = None
    try:
        resp = client.post(
            f"{api_base}/api/homework",
            data={
                "class_code": test_class_code,
                "subject": "Automation Testing",
                "description": "Ensure the system runs smoothly",
                "due_date": "Next Monday",
                "submitted_by": "Test Suite Runner"
            },
            headers=headers
        )
        if resp.status_code == 201:
            homework_id = resp.json().get("id")
            report(True, "Submit Homework", f"-> Submitted homework successfully (ID: {homework_id})")
        else:
            if not report(False, "Submit Homework", f"-> Failed: {resp.text}"):
                return False
    except Exception as e:
        if not report(False, "Submit Homework", f"-> Exception: {e}"):
            return False

    # 6. Retrieve Homework for Specific Class
    try:
        resp = client.get(f"{api_base}/api/homework/{test_class_code}")
        if resp.status_code == 200:
            hw_list = resp.json()
            found = any(h["id"] == homework_id for h in hw_list)
            if not report(found, "Fetch Class Homework", f"-> Successfully retrieved homework for '{test_class_code}'"):
                return False
        else:
            if not report(False, "Fetch Class Homework", f"-> Failed: {resp.text}"):
                return False
    except Exception as e:
        if not report(False, "Fetch Class Homework", f"-> Exception: {e}"):
            return False

    # 7. Retrieve ALL Homework
    try:
        resp = client.get(f"{api_base}/api/homework/ALL")
        if resp.status_code == 200:
            hw_all = resp.json()
            found = any(h["id"] == homework_id for h in hw_all)
            if not report(found, "Fetch ALL Homework", f"-> Successfully fetched unified homework feed (entries count: {len(hw_all)})"):
                return False
        else:
            if not report(False, "Fetch ALL Homework", f"-> Failed: {resp.text}"):
                return False
    except Exception as e:
        if not report(False, "Fetch ALL Homework", f"-> Exception: {e}"):
            return False

    # 8. Manage Holidays
    holiday_id = None
    try:
        resp = client.post(
            f"{api_base}/api/holidays",
            json={
                "title": "API Test Holiday",
                "start_date": "2026-12-25",
                "end_date": "2026-12-26",
                "reason": "Verify holiday endpoint holds up under load"
            },
            headers=headers
        )
        if resp.status_code == 201:
            holiday_id = resp.json().get("id")
            report(True, "Create Holiday", f"-> Added public holiday (ID: {holiday_id})")
        else:
            if not report(False, "Create Holiday", f"-> Failed: {resp.text}"):
                return False
    except Exception as e:
        if not report(False, "Create Holiday", f"-> Exception: {e}"):
            return False

    # 9. Register / Update Subscriber
    test_telegram_id = "99999999"
    try:
        # Register subscriber
        resp = client.post(
            f"{api_base}/api/subscribers",
            json={
                "telegram_id": test_telegram_id,
                "first_name": "TestParent",
                "username": "testparent_tg"
            }
        )
        if resp.status_code == 201:
            report(True, "Register Subscriber", f"-> Registered parent Telegram ID '{test_telegram_id}'")
        else:
            if not report(False, "Register Subscriber", f"-> Failed: {resp.text}"):
                return False

        # Set Class
        resp = client.patch(
            f"{api_base}/api/subscribers/{test_telegram_id}/class",
            json={"telegram_id": test_telegram_id, "class_code": test_class_code}
        )
        if resp.status_code == 200 and resp.json().get("class_code") == test_class_code:
            report(True, "Set Subscriber Class", f"-> Subscriber class bound to '{test_class_code}' successfully")
        else:
            if not report(False, "Set Subscriber Class", f"-> Failed: {resp.text}"):
                return False
    except Exception as e:
        if not report(False, "Subscriber Management", f"-> Exception: {e}"):
            return False

    # 10. Non-blocking Async Broadcast Enqueue
    try:
        resp = client.post(
            f"{api_base}/api/broadcast",
            json={"message": "System Integration Test Message - Please Ignore"},
            headers=headers
        )
        if resp.status_code == 200:
            report(True, "Queue Broadcast Announcement", f"-> Broadcast background task enqueued (Sent estimate: {resp.json().get('sent_to')})")
        else:
            if not report(False, "Queue Broadcast Announcement", f"-> Failed: {resp.text}"):
                return False
    except Exception as e:
        if not report(False, "Queue Broadcast Announcement", f"-> Exception: {e}"):
            return False

    # 11. Clean Up Test Records
    print("--------------------------------------------------")
    print("Cleaning up test records from local DB...")
    try:
        if holiday_id:
            client.delete(f"{api_base}/api/holidays/{holiday_id}", headers=headers)
        if homework_id:
            client.delete(f"{api_base}/api/homework/{homework_id}", headers=headers)
        if test_class_id:
            client.delete(f"{api_base}/api/classes/{test_class_id}", headers=headers)
        print("Cleanup finished successfully.")
    except Exception as e:
        print(f"Warning: Cleanup failed with error: {e}")

    return True


def run_api_integration_tests() -> bool:
    print_header("Running Live API Integration Tests")
    
    # Load dotenv in test runner to determine matching credentials
    from dotenv import load_dotenv
    load_dotenv()
    admin_user = os.getenv("ADMIN_USERNAME") or "admin"
    admin_pass = os.getenv("ADMIN_PASSWORD") or "admin123"

    # 1. Prepare environment variables for test server
    env = os.environ.copy()
    env["DATABASE_URL"] = "sqlite:///./test_runner.db"
    env["ADMIN_USERNAME"] = admin_user
    env["ADMIN_PASSWORD"] = admin_pass
    env["API_SECRET_KEY"] = os.getenv("API_SECRET_KEY") or "integration-runner-secret-key"
    env["TELEGRAM_BOT_TOKEN"] = os.getenv("TELEGRAM_BOT_TOKEN") or "123456789:dummyfortests"
    env["API_BASE_URL"] = "http://127.0.0.1:8001"
    env["RUN_BOT"] = "false"  # Disable live Telegram bot thread

    # 2. Launch the backend FastAPI server on test port 8001
    backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "backend"))
    print(f"Starting backend test server in '{backend_dir}' on port 8001...")
    
    server_cmd = [
        sys.executable,
        "-m",
        "uvicorn",
        "main:app",
        "--port",
        "8001",
        "--host",
        "127.0.0.1",
    ]
    
    server_proc = subprocess.Popen(
        server_cmd,
        cwd=backend_dir,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    server_healthy = False
    
    try:
        # Wait up to 10 seconds for the server to start and respond to health check
        print("Waiting for server to become healthy...")
        import httpx
        for i in range(50):  # 50 * 0.2s = 10s
            time.sleep(0.2)
            # Check if server terminated early
            if server_proc.poll() is not None:
                stdout, stderr = server_proc.communicate()
                print(f"{RED}Server exited prematurely with code {server_proc.returncode}{RESET}")
                print(f"Stdout:\n{stdout}\nStderr:\n{stderr}")
                return False
            
            try:
                resp = httpx.get("http://127.0.0.1:8001/health", timeout=1.0)
                if resp.status_code == 200 and resp.json().get("status") == "ok":
                    server_healthy = True
                    print(f"{GREEN}Server is up and healthy!{RESET}")
                    break
            except Exception:
                continue
        
        if not server_healthy:
            print(f"{RED}Server failed to start or respond to health checks in 10s.{RESET}")
            return False

        # 3. Execute the API Integration test suite logic directly
        print("Running API Integration test suite...")
        return run_api_test_suite("http://127.0.0.1:8001", admin_user, admin_pass)

    finally:
        # 4. Terminate the server process safely
        print("Stopping backend test server...")
        server_proc.terminate()
        try:
            server_proc.wait(timeout=3.0)
            print("Server stopped successfully.")
        except subprocess.TimeoutExpired:
            print("Force killing server...")
            server_proc.kill()
            server_proc.wait()

        # 5. Clean up the test database file created in the backend directory
        db_path = os.path.join(backend_dir, "test_runner.db")
        if os.path.exists(db_path):
            print(f"Cleaning up temporary database: {db_path}")
            try:
                os.remove(db_path)
            except Exception as e:
                print(f"Warning: Failed to delete temporary database: {e}")


def main():
    print_header("SmartEdu Bot - Test Automation Runner")
    print(f"Python interpreter: {sys.executable}")
    print(f"Current workspace: {os.path.abspath(os.path.dirname(__file__))}")
    print("==================================================")
    
    start_time = time.time()
    
    # 1. Run Unit Tests
    unit_success = run_unit_tests()
    if not unit_success:
        print(f"\n{RED}[FAIL] UNIT TESTS FAILED. Aborting.{RESET}")
        sys.exit(1)
    print(f"\n{GREEN}[PASS] Unit tests passed successfully!{RESET}\n")

    # 2. Run E2E Simulation
    e2e_success = run_e2e_simulation()
    if not e2e_success:
        print(f"\n{RED}[FAIL] E2E SIMULATION FAILED. Aborting.{RESET}")
        sys.exit(1)
    print(f"\n{GREEN}[PASS] E2E simulation tests passed successfully!{RESET}\n")

    # 3. Run Live API Integration Tests
    integration_success = run_api_integration_tests()
    if not integration_success:
        print(f"\n{RED}[FAIL] LIVE API INTEGRATION TESTS FAILED.{RESET}")
        sys.exit(1)
    print(f"\n{GREEN}[PASS] Live API integration tests passed successfully!{RESET}\n")

    duration = time.time() - start_time
    print_header(f"{GREEN}[PASS] ALL TEST SUITES PASSED SUCCESSFULLY! (Time: {duration:.2f}s){RESET}")


if __name__ == "__main__":
    main()
