import importlib.util
import json
import socket
import threading
from pathlib import Path


CLIENT_PATH = Path(__file__).parents[1] / "examples" / "runtime_mcp_client.py"
SPEC = importlib.util.spec_from_file_location("runtime_mcp_client", CLIENT_PATH)
CLIENT_MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(CLIENT_MODULE)


def receive_exact(connection, size):
    chunks = []
    while size:
        chunk = connection.recv(size)
        if not chunk:
            raise ConnectionError("client closed connection")
        chunks.append(chunk)
        size -= len(chunk)
    return b"".join(chunks)


def serve(listener, requests):
    connection, _ = listener.accept()
    with connection:
        while len(requests) < 3:
            magic, size = CLIENT_MODULE.HEADER.unpack(
                receive_exact(connection, CLIENT_MODULE.HEADER.size)
            )
            assert magic == CLIENT_MODULE.MAGIC
            request = json.loads(receive_exact(connection, size))
            requests.append(request)

            if request["method"] == "initialize":
                result = {"protocolVersion": "2025-03-26", "capabilities": {}}
            elif request["method"] == "tools/list":
                result = {"tools": [{"name": "scene.overview"}]}
            else:
                result = {"isError": False, "content": [{"type": "text", "text": "ok"}]}

            payload = json.dumps(
                {"jsonrpc": "2.0", "id": request["id"], "result": result}
            ).encode("utf-8")
            connection.sendall(
                CLIENT_MODULE.HEADER.pack(CLIENT_MODULE.MAGIC, len(payload)) + payload
            )


def test_initialize_list_and_call_round_trip():
    requests = []
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        listener.listen(1)
        thread = threading.Thread(target=serve, args=(listener, requests), daemon=True)
        thread.start()

        with CLIENT_MODULE.RuntimeMCPClient(
            "127.0.0.1", listener.getsockname()[1], timeout=2
        ) as client:
            assert client.list_tools() == [{"name": "scene.overview"}]
            result = client.call_tool("unrealcv.exec", {"command": "vget /unrealcv/status"})

        thread.join(timeout=2)

    assert not thread.is_alive()
    assert [request["method"] for request in requests] == [
        "initialize",
        "tools/list",
        "tools/call",
    ]
    assert result["isError"] is False
    assert requests[-1]["params"]["arguments"]["command"] == "vget /unrealcv/status"
