"""
Python MCP 共用套版：以 FastMCP 建立伺服器並註冊示範 Tool。

複製此專案後請將模組名稱、工具函式與說明改為你的業務邏輯。
"""

from __future__ import annotations

import os
import sys
from typing import Literal

from mcp.server.fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse


def build_mcp_server() -> FastMCP:
    """
    建立並回傳設定好的 FastMCP 實例。

    環境變數（可選）：
      MCP_HOST：綁定位址，預設 127.0.0.1
      MCP_PORT：埠號，預設 8000
    """
    host: str = os.environ.get("MCP_HOST", "127.0.0.1")
    port: int = int(os.environ.get("MCP_PORT", "8000"))

    instructions: str = (
        "此為套版示範 MCP。請替換為你的伺服器用途與使用說明（給模型與開發者參考）。"
    )

    mcp: FastMCP = FastMCP(
        "mcp-template",
        instructions=instructions,
        host=host,
        port=port,
    )

    @mcp.tool()
    def ping() -> str:
        """套版預設工具：回傳固定字串，確認 MCP 已連線。"""
        return "pong"

    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(_request: Request) -> JSONResponse:
        """HTTP 健康檢查（非 MCP 協定），便於負載平衡或 Docker HEALTHCHECK。"""
        return JSONResponse({"status": "ok", "service": "mcp-template"})

    return mcp


def main() -> None:
    """CLI 進入點：依 MCP_TRANSPORT 選擇傳輸層。"""
    transport: Literal["stdio", "sse", "streamable-http"] = _parse_transport(
        os.environ.get("MCP_TRANSPORT", "stdio")
    )
    server: FastMCP = build_mcp_server()
    server.run(transport=transport)


def _parse_transport(
    raw: str,
) -> Literal["stdio", "sse", "streamable-http"]:
    value: str = raw.strip().lower().replace("_", "-")
    if value in ("stdio", "sse", "streamable-http"):
        return value  # type: ignore[return-value]
    print(f"不支援的 MCP_TRANSPORT={raw!r}，請使用 stdio、sse 或 streamable-http", file=sys.stderr)
    sys.exit(2)


if __name__ == "__main__":
    main()
