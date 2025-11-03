# Creative Automation Pipeline

Generate professional, localized advertising creatives with multi-product support, regional targeting, and automated translation.

---

## Quick Start

### 1. Install Dependencies

**Requirements**: Python 3.12 or 3.13 (3.14+ not yet supported)

```bash
# Clone the repository
git clone https://github.com/mitchaiet/creative-pipeline-automation.git
cd creative-pipeline-automation

# Install uv (if not already installed)
# On macOS and Linux:
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows:
# powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Install project dependencies using uv (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

### 2. Get Your API Key

1. Visit [Google AI Studio](https://ai.google.dev/)
2. Sign in and click "Get API Key"
3. Copy your API key

### 3. Configure

```bash
# Create environment file
cp .env.example .env

# Edit .env and add your key
GOOGLE_API_KEY=your_api_key_here
```

### 4. Run

```bash
uv run python src/app.py
```

Open your browser to **http://localhost:7860**

---

## Basic Usage

### Create a Campaign

1. **Campaign Tab**: Select your target region and audience
2. **Messaging Tab**: Enter your campaign message
3. **Environments Tab**: Generate background scenes
4. **Products Tab**: Choose products and generate views
5. **Generate Tab**: Create final ads in 3 aspect ratios

### Output

All assets are saved to `outputs/{CAMPAIGN_ID}/`:
- `environments/` - Background images
- `products/` - Product photography
- `ads/1_1/` - Square ads (Instagram, Facebook)
- `ads/9_16/` - Vertical ads (Stories, Reels, TikTok)
- `ads/16_9/` - Landscape ads (YouTube)
- `campaign_config.json` - Full campaign configuration
