# Python MCP 共用套版與範例

本專案提供可複製的 **FastMCP** 骨架（`template/`）、可執行的完整範例（`example/`），以及 **Docker** 於 **80** 埠部署 **Streamable HTTP** 的預設設定。

## 目錄結構

| 路徑                          | 說明                                     |
| ----------------------------- | ---------------------------------------- |
| `template/`                   | 套版：最小 Tool、`/health`、環境變數慣例 |
| `example/`                    | 範例：`echo`、加法、時區時間、健康檢查   |
| `Docs/Quick-Start.md`         | 最短步驟：本機、stdio、Docker、套版      |
| `Docs/MCP-Python-Template.md` | 詳細說明（傳輸層、環境變數、客戶端連線） |
| `Dockerfile`                  | 建置 `example-mcp`，對外 **80**          |
| `docker-compose.yml`          | 本機對應 `80:80`                         |

## 本機快速開始（範例）

```bash
cd example
python3 -m venv .venv && source .venv/bin/activate
pip install -e .
MCP_TRANSPORT=streamable-http example-mcp
```

預設為 `127.0.0.1:8000`。另開終端機測試健康檢查：

```bash
curl -s http://127.0.0.1:8000/health
```

MCP Streamable HTTP 預設路徑為 `/mcp`（見官方 `FastMCP` 的 `streamable_http_path`）。

## Docker（對外 80）

於專案根目錄：

```bash
docker build -t example-mcp:latest .
docker run --rm -p 80:80 example-mcp:latest
```

或使用 Compose：

```bash
docker compose up --build
```

驗證：

```bash
curl -s http://127.0.0.1/health
```

## 套版用法

複製 `template/` 目錄，修改 `pyproject.toml` 的專案名稱、`src` 下套件名稱與 `server.py` 內容；細節見 `Docs/MCP-Python-Template.md`。

## 依賴

- Python **3.10+**
- # 核心套件：`mcp`、`uvicorn`（FastMCP 的 SSE / Streamable HTTP 會透過 uvicorn 提供）

# MCP-Template

MCP套版
