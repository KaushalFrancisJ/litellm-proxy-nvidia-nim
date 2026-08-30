# LiteLLM NVIDIA NIM Proxy

A LiteLLM proxy configuration providing high-throughput routing, failover, and load balancing across multiple NVIDIA NIM API keys.

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.10+
- NVIDIA NIM API keys

### 2. Environment Setup

Create and activate a virtual environment:

```powershell
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy the example `.env` file and fill in your API credentials:

```powershell
Copy-Item .env.example .env
```

Edit `.env`:

```env
NVIDIA_API_KEY1=nvapi-xxxx
NVIDIA_API_KEY2=nvapi-xxxx
NVIDIA_API_KEY3=nvapi-xxxx
LITELLM_MASTER_KEY=sk-litellm-local-key
```

---

## ⚙️ Running the LiteLLM Proxy

Start the proxy server using the configuration file:

```powershell
litellm --config .\config.yaml
```

The proxy will start locally on `http://localhost:4000`.

---

## 🧠 Configured Models

The proxy routes requests across multiple NVIDIA NIM endpoints with `least-busy` routing and automatic retries:

| Model Alias | Target Model (`nvidia_nim/`) | RPM | Key Pool |
|---|---|---|---|
| `nvidia-nemotron-lightning` | `nvidia/nemotron-3.5-lightning-30b-a3b` | 40 | Key 1, 2, 3 |
| `nvidia-deepseek-ultra` | `deepseek-ai/deepseek-v4-flash` | 40 | Key 1, 2, 3 |
| `nvidia-nemotron-nano` | `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning` | 40 | Key 1, 2, 3 |
| `nvidia-kimi-omni` | `moonshotai/kimi-k2.6` | 40 | Key 1, 2, 3 |

---

## 🧪 Load Testing

A concurrent asynchronous benchmark script is included to test latency and rate limits:

```powershell
python test_load.py
```

---

## 🔌 Client Integration (e.g. Claude Code)

Refer to `settings.json` for sample client configuration pointing Anthropic / OpenAI compatible endpoints to the local LiteLLM proxy:

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "http://localhost:4000",
    "ANTHROPIC_API_KEY": "sk-litellm-local-key",
    "ANTHROPIC_MODEL": "nvidia-deepseek-ultra",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "nvidia-mistral-super",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "nvidia-kimi-omni",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "nvidia-nemotron-nano"
  }
}
```
