# Python MCP 共用套版說明

本文說明本倉庫中 **template**（套版）與 **example**（範例）的設計、環境變數、傳輸層選擇，以及以 **Docker** 在 **80** 埠部署時的注意事項。

## 1. 為何使用 FastMCP

官方 Python SDK（套件名稱 `mcp`）內建 **FastMCP**，可用裝飾器註冊 `tool`、`resource`、`prompt`，並支援：

- **stdio**：本機與 Cursor、Claude Desktop 等透過標準輸入輸出通訊（最常見的本機整合方式）。
- **sse**：以 Server-Sent Events 承載 MCP（舊版網路傳輸，仍可使用）。
- **streamable-http**：較新的 HTTP 串流傳輸（適合容器與遠端部署）。

本專案套版與範例均以 `mcp.server.fastmcp.FastMCP` 建立伺服器。

## 2. 目錄與職責

### 2.1 `template/`

- **目的**：給團隊複製後改名的最小可行骨架。
- **內容**：`ping` 工具、`GET /health`、讀取 `MCP_HOST` / `MCP_PORT` / `MCP_TRANSPORT`。
- **套件進入點**：安裝後可執行 `mcp-template`（見該目錄 `pyproject.toml`）。

### 2.2 `example/`

- **目的**：示範多個 Tool、型別註記、時區處理，以及與 Docker 搭配時的預設環境變數慣例。
- **進入點**：`example-mcp`。

## 3. 環境變數

| 變數 | 說明 | 範例預設（程式內） | Docker 映像建議 |
|------|------|-------------------|-----------------|
| `MCP_HOST` | 服務綁定位址 | `127.0.0.1` | `0.0.0.0`（對外監聽） |
| `MCP_PORT` | 埠號 | `8000` | `80` |
| `MCP_TRANSPORT` | `stdio` / `sse` / `streamable-http` | 依使用情境 | `streamable-http` |

說明：

- 本機開發若使用 **streamable-http**，不需 root 即可使用 **8000** 埠。
- 容器內使用 **80** 埠時，映像預設以 **root** 程序綁定，一般不需額外權限；若改為非特權使用者，請改用 **1024 以上** 埠並以 `docker run -p 80:8080` 等方式對應。

## 4. HTTP 路徑慣例

- **Streamable HTTP**：MCP 協定預設掛在 **`/mcp`**（`FastMCP` 的 `streamable_http_path` 預設值）。
- **SSE**：預設與 **`/sse`**、**`/messages/`** 等路徑相關（依 `FastMCP` 設定）。
- **健康檢查**：範例與套版皆提供 **`GET /health`**，回傳 JSON，供 **Kubernetes liveness** 或 **Docker HEALTHCHECK** 使用。

實際路徑以執行中程序與 `FastMCP` 建構參數為準；部署前請用瀏覽器或 `curl` 確認。

## 5. 客戶端連線提示

- **Cursor / IDE**：若使用遠端 MCP URL，請確認客戶端支援的傳輸類型（例如 **Streamable HTTP** 與 **SSE** 設定方式可能不同）。
- **stdio**：在設定檔中通常填「執行指令」與引數，而非 URL。

## 6. Docker 建置與執行

專案根目錄 `Dockerfile` 以 **`example/`** 為內容建置，並設定：

- `MCP_HOST=0.0.0.0`
- `MCP_PORT=80`
- `MCP_TRANSPORT=streamable-http`

建置與執行範例：

```bash
docker build -t example-mcp:latest .
docker run --rm -p 80:80 example-mcp:latest
```

`docker-compose.yml` 將主機 **80** 對應到容器 **80**，便於本機以 `http://localhost/health` 測試。

## 7. 複製套版後的檢查清單

1. 重新命名 Python 套件目錄與 `pyproject.toml` 中的 `name`。
2. 修改 `FastMCP` 第一個引數（伺服器顯示名稱）與 `instructions`。
3. 依需求刪除或擴充 `tool` / `resource` / `prompt`。
4. 若對外部署，設定 `MCP_HOST`、`MCP_PORT`，並選擇 `sse` 或 `streamable-http`。
5. 若置於反向代理之後，確認 **Host**、**Origin** 與 **TLS** 是否符合安全需求（生產環境請參考官方 **transport_security** 與驗證相關文件）。

## 8. 疑難排解

- **無法從另一台機器連線**：確認 `MCP_HOST` 為 `0.0.0.0`，且防火牆與雲端安全群組已開放對應埠。
- **本機 80 埠需要管理者權限**：改用 `MCP_PORT=8000` 或僅在容器內使用 80。
- **客戶端顯示連線失敗**：核對傳輸類型（`MCP_TRANSPORT`）與 URL 路徑是否與伺服器一致。

---

以上文件與程式範例旨在加速建立團隊內共用的 Python MCP 服務；正式上線前請再補上驗證、日誌與資源限制等營運需求。
