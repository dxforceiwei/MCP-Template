# How to Quick Start

以最短路徑跑起 **example-mcp**（範例）或 **template**（套版），並可選用 **Docker** 在 **80** 埠提供服務。

## 前置需求

- **Python 3.10+**
- （可選）**Docker**、**Docker Compose**，用於容器部署

---

## 一、本機執行範例（約 2 分鐘）

在專案根目錄下：

```bash
cd example
python3 -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -e .
```

以 **Streamable HTTP** 啟動（適合瀏覽器／HTTP 客戶端測試）：

```bash
export MCP_TRANSPORT=streamable-http
example-mcp
```

預設監聽 **`127.0.0.1:8000`**。

**驗證健康檢查**（另開終端機）：

```bash
curl -s http://127.0.0.1:8000/health
```

預期回傳 JSON，內含 `"status":"ok"`。

**MCP 端點**：Streamable HTTP 預設路徑為 **`/mcp`**（完整 URL 範例：`http://127.0.0.1:8000/mcp`，實際以客戶端設定為準）。

---

## 二、本機使用 stdio（給 Cursor / 支援 MCP 的 IDE）

不需 HTTP，使用標準輸入輸出。未設定 `MCP_TRANSPORT` 時，**預設即為 `stdio`**：

```bash
cd example
source .venv/bin/activate
example-mcp
```

若需明確指定：

```bash
export MCP_TRANSPORT=stdio
example-mcp
```

在編輯器的 MCP 設定中，將啟動指令指向虛擬環境內的 **`example-mcp`**（完整路徑，例如 `.../example/.venv/bin/example-mcp`），必要時加上環境變數 `MCP_TRANSPORT=stdio`。

---

## 三、Docker（對外 80）

在**專案根目錄**（與 `Dockerfile` 同層）：

```bash
docker build -t example-mcp:latest .
docker run --rm -p 80:80 example-mcp:latest
```

驗證：

```bash
curl -s http://127.0.0.1/health
```

或使用 Compose：

```bash
docker compose up --build
```

映像內已設定 **`MCP_HOST=0.0.0.0`**、**`MCP_PORT=80`**、**`MCP_TRANSPORT=streamable-http`**。

---

## 四、從套版開新專案

1. 複製整個 **`template/`** 目錄。
2. 修改 **`pyproject.toml`** 的專案名稱與 **`[project.scripts]`** 指令名稱。
3. 將 **`src/mcp_template/`** 重新命名為你的套件名，並更新檔案內的 `import`。
4. 在 **`server.py`** 中替換 `instructions`、Tool 與業務邏輯。

安裝與執行方式與範例相同：`pip install -e .`，再執行對應的 console script。

---

## 下一步

- 傳輸層、環境變數與安全注意事項：**[MCP-Python-Template.md](./MCP-Python-Template.md)**
- 專案總覽與目錄說明：上層 **[README.md](../README.md)**
