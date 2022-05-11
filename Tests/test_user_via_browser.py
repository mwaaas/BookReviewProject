import pytest
import subprocess
import time
import socket

def wait_for_port(port, host='localhost', timeout=5.0, only_once=False):
    """Wait until a port starts accepting TCP connections.
    Args:
        port (int): Port number.
        host (str): Host address on which the port should exist.
        timeout (float): In seconds. How long to wait before raising errors.
    Raises:
        TimeoutError: The port isn't accepting connection after time specified in `timeout`.
    """
    start_time = time.perf_counter()
    while True:
        try:
            with socket.create_connection((host, port), timeout=timeout):
                break
            if only_once:
                raise TimeoutError(f"Waited once for port {port} on host {host}")
        except OSError as ex:
            time.sleep(0.01)
            if time.perf_counter() - start_time >= timeout:
                raise TimeoutError(f'Waited too long for the port {port} on host {host} to start accepting '
                                   'connections.') from ex


@pytest.fixture(scope="package")
def server_fixture():
    print("Starting server at host 0.0.0.0:5055")
    process = subprocess.Popen([
        "python",
        "manage.py",
        "run_server",
        "--host=0.0.0.0",
        "--port=5055"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    wait_for_port(5055)
    yield
    print("Terminating server")
    process.kill()

class TestLoginViaBrowser():
    base_url = "http://localhost:5055"

    def test_landing_page_title(self, page, server_fixture):
        page.goto(self.base_url)
        assert page.title() == "BookReview"
