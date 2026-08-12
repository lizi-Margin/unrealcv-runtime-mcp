#!/usr/bin/env python3
"""Call UnrealCV Runtime MCP over UnrealCV's framed TCP transport."""

from __future__ import annotations

import argparse
import json
import socket
import struct
from typing import Any


MAGIC = 0x9E2B83C1
HEADER = struct.Struct("=II")


def _receive_exact(connection: socket.socket, size: int) -> bytes:
    chunks = []
    remaining = size
    while remaining:
        chunk = connection.recv(remaining)
        if not chunk:
            raise ConnectionError("Runtime MCP closed the connection")
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)


class RuntimeMCPClient:
    def __init__(self, host: str = "127.0.0.1", port: int = 29998, timeout: float = 30.0):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.connection: socket.socket | None = None
        self.request_id = 0

    def __enter__(self) -> "RuntimeMCPClient":
        self.connection = socket.create_connection((self.host, self.port), self.timeout)
        self.connection.settimeout(self.timeout)
        self.initialize()
        return self

    def __exit__(self, exc_type: Any, exc: Any, traceback: Any) -> None:
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def request(self, method: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        if self.connection is None:
            raise RuntimeError("RuntimeMCPClient must be used as a context manager")

        self.request_id += 1
        message: dict[str, Any] = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method,
        }
        if params is not None:
            message["params"] = params

        payload = json.dumps(message, separators=(",", ":")).encode("utf-8")
        self.connection.sendall(HEADER.pack(MAGIC, len(payload)) + payload)

        magic, payload_size = HEADER.unpack(_receive_exact(self.connection, HEADER.size))
        if magic != MAGIC:
            raise RuntimeError(f"Unexpected frame magic: 0x{magic:08x}")

        response = json.loads(_receive_exact(self.connection, payload_size).decode("utf-8"))
        if response.get("id") != self.request_id:
            raise RuntimeError(f"Unexpected JSON-RPC response id: {response.get('id')!r}")
        if "error" in response:
            error = response["error"]
            raise RuntimeError(f"JSON-RPC {error.get('code')}: {error.get('message')}")
        return response["result"]

    def initialize(self) -> dict[str, Any]:
        return self.request(
            "initialize",
            {
                "protocolVersion": "2025-03-26",
                "capabilities": {},
                "clientInfo": {"name": "unrealcv-runtime-mcp-example", "version": "1.0.0"},
            },
        )

    def list_tools(self) -> list[dict[str, Any]]:
        return self.request("tools/list").get("tools", [])

    def call_tool(self, name: str, arguments: dict[str, Any] | None = None) -> dict[str, Any]:
        return self.request("tools/call", {"name": name, "arguments": arguments or {}})


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=29998)
    parser.add_argument("--timeout", type=float, default=30.0)
    subparsers = parser.add_subparsers(dest="operation", required=True)

    subparsers.add_parser("ping", help="Check the Runtime MCP connection")
    subparsers.add_parser("tools", help="List tools exposed by this runtime")

    call_parser = subparsers.add_parser("call", help="Call an MCP tool")
    call_parser.add_argument("name")
    call_parser.add_argument("--arguments", default="{}", help="JSON object")

    exec_parser = subparsers.add_parser("exec", help="Execute an UnrealCV command")
    exec_parser.add_argument("command")
    return parser.parse_args()


def main() -> int:
    args = parse_arguments()
    with RuntimeMCPClient(args.host, args.port, args.timeout) as client:
        if args.operation == "ping":
            result = client.request("ping")
        elif args.operation == "tools":
            result = client.list_tools()
        elif args.operation == "call":
            arguments = json.loads(args.arguments)
            if not isinstance(arguments, dict):
                raise ValueError("--arguments must decode to a JSON object")
            result = client.call_tool(args.name, arguments)
        else:
            result = client.call_tool("unrealcv.exec", {"command": args.command})

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
