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

### Option 1: Create New Campaign

1. **Campaign Tab**: Select your target region and audience
2. **Messaging Tab**: Enter your campaign message and get translations
3. **Environments Tab**: Describe and generate background scenes
4. **Products Tab**: Choose products and generate views
5. **Logos Tab**: Upload brand logos
6. **Preview Tab**: Review all assets
7. **Generate Tab**: Create final ads in 3 aspect ratios

### Option 2: Load from JSON

1. **Campaign Tab**: Click "Load Campaign JSON" and select a `campaign_config.json` file
2. **Automatic workflow triggers:**
   - Translations generated for target region
   - 4 environment backgrounds created
   - Product views generated (6 per product)
3. **Preview Tab**: Review auto-generated assets
4. **Generate Tab**: Create final ads

### Output

All campaigns are organized by timestamp in `outputs/YYYYMMDD_HHMMSS/`:
- `environments/` - 4 AI-generated background scenes
- `products/` - 6 views per product (front, back, left, right, top-down, bottom-up)
- `ads/1_1/` - Square ads (1080×1080 for Instagram, Facebook)
- `ads/9_16/` - Vertical ads (1080×1920 for Stories, Reels, TikTok)
- `ads/16_9/` - Landscape ads (1920×1080 for YouTube)
- `campaign_config.json` - Complete campaign configuration with portable paths
