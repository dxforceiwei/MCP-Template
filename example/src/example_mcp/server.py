"""
範例 MCP 伺服器：示範 Tool 註冊、環境變數與 HTTP 健康檢查路由。

部署於 Docker 時請設定 MCP_HOST=0.0.0.0、MCP_PORT=80 與 MCP_TRANSPORT=streamable-http（或 sse）。
"""

from __future__ import annotations

import os
import sys
from datetime import datetime, timezone
from typing import Literal
from zoneinfo import ZoneInfo

from mcp.server.fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse


def build_example_mcp() -> FastMCP:
    """
    建立範例 FastMCP：含 echo、加法、時間查詢與 /health。

    環境變數：
      MCP_HOST：預設 127.0.0.1；Docker 映像中設為 0.0.0.0
      MCP_PORT：預設 8000；Docker 映像中設為 80
    """
    host: str = os.environ.get("MCP_HOST", "127.0.0.1")
    port: int = int(os.environ.get("MCP_PORT", "8000"))

    instructions: str = (
        "範例 MCP：提供 echo、整數加法與指定時區時間。"
        "HTTP 端點：Streamable HTTP 預設路徑見 MCP 設定 streamable_http_path（預設 /mcp）。"
    )

    mcp: FastMCP = FastMCP(
        "example-mcp",
        instructions=instructions,
        host=host,
        port=port,
    )

    @mcp.tool()
    def echo(message: str) -> str:
        """原樣回傳輸入字串，用於測試連線與參數傳遞。"""
        return message

    @mcp.tool()
    def add_integers(a: int, b: int) -> int:
        """將兩個整數相加並回傳結果。"""
        return a + b

    @mcp.tool()
    def current_time(timezone_name: str = "Asia/Taipei") -> str:
        """
        回傳指定 IANA 時區的目前時間（ISO 8601 字串）。
        若時區名稱無效，會回傳錯誤說明字串。
        """
        try:
            tz: ZoneInfo = ZoneInfo(timezone_name)
        except Exception:
            return f"無效的時區名稱: {timezone_name}"
        now: datetime = datetime.now(timezone.utc).astimezone(tz)
        return now.isoformat()

    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(_request: Request) -> JSONResponse:
        """Kubernetes / Docker 可用的存活探測。"""
        payload: dict[str, str] = {
            "status": "ok",
            "service": "example-mcp",
            "utc": datetime.now(timezone.utc).isoformat(),
        }
        return JSONResponse(payload)

    return mcp


def main() -> None:
    """CLI：依 MCP_TRANSPORT 啟動對應傳輸層。"""
    transport: Literal["stdio", "sse", "streamable-http"] = _parse_transport(
        os.environ.get("MCP_TRANSPORT", "stdio")
    )
    server: FastMCP = build_example_mcp()
    server.run(transport=transport)


def _parse_transport(
    raw: str,
) -> Literal["stdio", "sse", "streamable-http"]:
    value: str = raw.strip().lower().replace("_", "-")
    if value in ("stdio", "sse", "streamable-http"):
        return value  # type: ignore[return-value]
    print(
        f"不支援的 MCP_TRANSPORT={raw!r}，請使用 stdio、sse 或 streamable-http",
        file=sys.stderr,
    )
    sys.exit(2)


if __name__ == "__main__":
    main()
