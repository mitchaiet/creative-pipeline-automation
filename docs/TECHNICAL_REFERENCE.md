# Technical Reference

Detailed technical documentation for the Creative Automation Pipeline.

---

## Table of Contents

1. [Technology Stack](#technology-stack)
2. [API Configuration](#api-configuration)
3. [File Naming Conventions](#file-naming-conventions)
4. [Aspect Ratios](#aspect-ratios)
5. [Image Specifications](#image-specifications)
6. [Language Codes](#language-codes)
7. [Environment Variables](#environment-variables)
8. [Dependencies](#dependencies)

---

## Technology Stack

### Core Technologies

#### Python 3.12+
- **Role**: Primary programming language
- **Requirement**: Python 3.12 or higher
- **Package Manager**: uv (fast alternative to pip)

#### uv Package Manager
- **Version**: Latest stable
- **Purpose**: Fast Python package installation and management
- **Installation**: See [astral-sh/uv](https://github.com/astral-sh/uv)
- **Benefits**:
  - 10-100x faster than pip
  - Better dependency resolution
  - Project-based package management

### Web Framework

#### Gradio 5.49.1
- **Role**: Web interface framework
- **Features Used**:
  - `gr.Interface` - Main app structure
  - `gr.Blocks` - Custom layouts
  - `gr.Tabs` - Multi-step workflow
  - `gr.Gallery` - Image selection
  - `gr.Plot` - Interactive world map
  - `gr.State` - Session persistence
- **Server**:
  - Built-in Flask-based server
  - WebSocket support for real-time updates
  - Automatic responsive design

### AI & Image Generation

#### Google Gemini 2.5 Flash Image
- **Model ID**: `gemini-2.5-flash-image`
- **Nickname**: "Nano Banana"
- **API Library**: `google-genai` (official SDK)
- **Version**: 1.0.0+
- **Capabilities**:
  - Text-to-image generation
  - Image-to-image transformation
  - Multi-modal input (text + images)
  - Aspect ratio enforcement
  - High-resolution output

**Input modes:**
- Text prompt only (environments)
- Text + reference images (product views)
- Text + multiple images (ad compositions)

**Output:**
- PNG format
- RGB color mode
- High resolution (1080p+)

### Visualization

#### Plotly 6.3.1
- **Role**: Interactive world map
- **Component**: `plotly.graph_objects`
- **Features Used**:
  - Choropleth map
  - Country boundaries
  - Interactive hover
  - Click event handling
  - Custom styling

### Translation

#### deep-translator 1.11.4
- **Service**: Google Translate API
- **Supported Languages**: 100+
- **Usage**: Campaign message localization
- **Integration**: Automatic based on region selection

### Image Processing

#### Pillow 11.3.0
- **Role**: Image manipulation
- **Operations**:
  - Image loading and saving
  - Format conversion
  - Resizing (if needed)
  - Metadata extraction

### Configuration

#### PyYAML 6.0.3
- **Role**: Configuration file parsing
- **Files Parsed**:
  - `config/regions.yaml`
  - `config/audiences.yaml`
  - `products/*/config.yaml`

#### python-dotenv 1.1.1
- **Role**: Environment variable management
- **File**: `.env`
- **Usage**: API key storage

---

## API Configuration

### Google Gemini API

#### Getting an API Key

1. **Visit Google AI Studio**
   - URL: [https://ai.google.dev/](https://ai.google.dev/)
   - Sign in with Google account

2. **Create API Key**
   - Click "Get API Key"
   - Create new project or select existing
   - Generate API key

3. **Configure in Application**
   - **Option A**: Settings tab in UI
   - **Option B**: Add to `.env` file

#### API Endpoints

**Base URL**: Managed by `google-genai` SDK

**Model**: `gemini-2.5-flash-image`

**Authentication**: API key via header

#### Request Format

```python
response = client.models.generate_images(
    model='gemini-2.5-flash-image',
    prompt="Your detailed prompt here",
    config={
        'numberOfImages': 1,
        'aspectRatio': '1:1',  # or '9:16', '16:9'
        'negativePrompt': 'low quality, blurry'
    }
)
```

#### Multi-Modal Input

```python
# With reference images
response = client.models.generate_images(
    model='gemini-2.5-flash-image',
    prompt="Generate product view",
    config={
        'numberOfImages': 1,
        'aspectRatio': '1:1',
        'referenceImages': [
            {'imageBytes': image1_bytes},
            {'imageBytes': image2_bytes}
        ]
    }
)
```

#### Rate Limits

**Free Tier:**
- 10 requests per minute
- 500 requests per day
- Subject to change - check [Google AI pricing](https://ai.google.dev/pricing)

**Paid Tier:**
- Higher limits available
- Pay-per-use pricing

#### Error Handling

Common errors:
- `401 Unauthorized`: Invalid API key
- `429 Too Many Requests`: Rate limit exceeded
- `400 Bad Request`: Invalid parameters

### Translation API

#### Deep Translator

Uses Google Translate backend (no separate API key required):

```python
from deep_translator import GoogleTranslator

translated = GoogleTranslator(
    source='en',
    target='es'
).translate("Your campaign message")
```

**Supported Language Codes**: ISO 639-1 standard

---

## File Naming Conventions

### Campaign Folders

**Format**: `{CAMPAIGN_ID}`
**Pattern**: 6 alphanumeric uppercase characters
**Examples**: `E2E6K6`, `K24SAG`, `UL8M9Y`

**Generation**:
```python
campaign_id = ''.join(random.choices(
    string.ascii_uppercase + string.digits,
    k=6
))
```

### Timestamps

**Format**: `YYYYMMDD_HHMMSS`
**Examples**:
- `20251102_134500`
- `20251026_120000`

**Generation**:
```python
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
```

### Environment Images

**Pattern**: `environment_{number}_{timestamp}.png`

**Examples**:
- `environment_1_20251102_134500.png`
- `environment_2_20251102_134500.png`
- `environment_3_20251102_134500.png`
- `environment_4_20251102_134500.png`

**Location**: `outputs/{CAMPAIGN_ID}/environments/`

### Product Views (Separate Mode)

**Pattern**: `{view}_{timestamp}.png`

**Views**: `front`, `back`, `left`, `right`, `top-down`, `bottom-up`

**Examples**:
- `front_20251102_134500.png`
- `back_20251102_134500.png`
- `left_20251102_134500.png`

**Location**: `outputs/{CAMPAIGN_ID}/products/{product-slug}/`

### Product Views (Combined Mode)

**Pattern**: `combined_{view}_{timestamp}.png`

**Examples**:
- `combined_front_20251102_134500.png`
- `combined_back_20251102_134500.png`

**Location**: `outputs/{CAMPAIGN_ID}/products/combined/`

### Ad Creatives

**Pattern (non-localized)**: `ad_{ratio}_{timestamp}.png`
**Pattern (localized)**: `ad_{ratio}_{lang}_{timestamp}.png`

**Ratio formats**: `1_1`, `9_16`, `16_9` (underscore separator)

**Examples**:
- `ad_1_1_20251102_134500.png` (English, no localization)
- `ad_1_1_en_20251102_134500.png` (English, with localization)
- `ad_9_16_es_20251102_134500.png` (Spanish, vertical)
- `ad_16_9_fr_20251102_134500.png` (French, landscape)

**Location**: `outputs/{CAMPAIGN_ID}/ads/{ratio}/`

### Campaign Configuration

**Filename**: `campaign_config.json`

**Location**: `outputs/{CAMPAIGN_ID}/campaign_config.json`

---

## Aspect Ratios

### Supported Ratios

| Ratio | Dimensions | Description | Use Cases |
|-------|------------|-------------|-----------|
| 1:1 | 1080 × 1080 | Square | Instagram feed, Facebook posts, Twitter |
| 9:16 | 1080 × 1920 | Vertical/Portrait | Instagram Stories, TikTok, Reels, Snapchat |
| 16:9 | 1920 × 1080 | Landscape | YouTube, Desktop ads, LinkedIn |

### API Enforcement

Aspect ratios are enforced at the API level:

```python
config = {
    'aspectRatio': '1:1'  # API enforces exact ratio
}
```

**Previous approach** (deprecated):
- Relied on prompt alone: "Generate in 1:1 aspect ratio"
- Less reliable, required cropping/validation

**Current approach**:
- API parameter ensures correct ratio
- No post-processing needed
- Guaranteed dimensions

### Folder Naming

Aspect ratio folders use **underscore format**:
- `1_1/` (not `1x1/`)
- `9_16/` (not `9x16/`)
- `16_9/` (not `16x9/`)

---

## Image Specifications

### Environments

**Dimensions**: 1080 × 1080 (1:1)
**Format**: PNG
**Background**: Varies (realistic scenes)
**Lighting**: Professional studio-quality
**Style**: Photorealistic

**Typical file size**: 500KB - 2MB

### Product Views

**Dimensions**: 1080 × 1080 (1:1)
**Format**: PNG
**Background**: Pure white (#FFFFFF)
**Lighting**: Professional studio lighting
**Style**: Photorealistic product photography

**Typical file size**: 300KB - 1MB

### Ad Creatives

**Dimensions**: Varies by aspect ratio
- 1:1 → 1080 × 1080
- 9:16 → 1080 × 1920
- 16:9 → 1920 × 1080

**Format**: PNG
**Background**: Environment scene
**Elements**:
- Product (40-60% of frame)
- Environment background
- Campaign message (typography)
- Logo (optional, corner placement)

**Typical file size**: 1MB - 3MB

### Quality Requirements

All generated images must meet:
- **Resolution**: 1080p minimum
- **Color mode**: RGB
- **Bit depth**: 8-bit per channel
- **Format**: PNG (lossless)
- **Compression**: Standard PNG compression
- **Artifacts**: None (no JPEG compression artifacts)

---

## Language Codes

### ISO 639-1 Standard

Used for localized ad file naming:

| Code | Language | Example Region |
|------|----------|----------------|
| `en` | English | North America, Europe |
| `es` | Spanish | Latin America, North America |
| `fr` | French | Europe, North America |
| `de` | German | Europe |
| `it` | Italian | Europe |
| `zh-CN` | Chinese (Simplified) | Asia Pacific |
| `zh-TW` | Chinese (Traditional) | Asia Pacific |
| `ja` | Japanese | Asia Pacific |
| `ko` | Korean | Asia Pacific |
| `hi` | Hindi | Asia Pacific |
| `ar` | Arabic | Middle East & Africa |
| `pt` | Portuguese | Latin America |

### Regional Top Languages

**North America**:
1. `en` - English
2. `es` - Spanish
3. `fr` - French
4. `zh-CN` - Chinese (Simplified)

**Europe**:
1. `en` - English
2. `de` - German
3. `fr` - French
4. `es` - Spanish

**Asia Pacific**:
1. `zh-CN` - Chinese (Simplified)
2. `hi` - Hindi
3. `ja` - Japanese
4. `ko` - Korean

**Latin America**:
1. `es` - Spanish
2. `pt` - Portuguese
3. `en` - English
4. `fr` - French

**Middle East & Africa**:
1. `ar` - Arabic
2. `en` - English
3. `fr` - French
4. `sw` - Swahili

**Oceania**:
1. `en` - English
2. `zh-CN` - Chinese (Simplified)
3. `mi` - Māori
4. `sm` - Samoan

---

## Environment Variables

### Required Variables

#### GOOGLE_API_KEY
- **Type**: String
- **Required**: Yes
- **Purpose**: Google Gemini API authentication
- **Format**: API key from Google AI Studio
- **Example**: `AIzaSyA...`

**Setting options:**
1. `.env` file: `GOOGLE_API_KEY=your_key_here`
2. Settings tab in UI

### Optional Variables

#### PORT
- **Type**: Integer
- **Required**: No
- **Default**: 7860
- **Purpose**: Web server port

**Usage**:
```python
port = int(os.getenv("PORT", 7860))
```

---

## Dependencies

### Complete List

From `pyproject.toml` and `requirements.txt`:

```toml
[project]
name = "creative-automation-pipeline"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "gradio==5.49.1",
    "google-genai>=1.0.0",
    "plotly==6.3.1",
    "deep-translator==1.11.4",
    "pillow==11.3.0",
    "pyyaml==6.0.3",
    "python-dotenv==1.1.1"
]
```

### Dependency Details

#### gradio==5.49.1
- **Purpose**: Web UI framework
- **Size**: ~50MB
- **Dependencies**: Flask, pydantic, fastapi
- **Docs**: [gradio.app](https://gradio.app)

#### google-genai>=1.0.0
- **Purpose**: Google Gemini API client
- **Size**: ~5MB
- **Dependencies**: google-auth, protobuf
- **Docs**: [ai.google.dev](https://ai.google.dev)

#### plotly==6.3.1
- **Purpose**: Interactive visualizations (world map)
- **Size**: ~20MB
- **Dependencies**: numpy, pandas (optional)
- **Docs**: [plotly.com](https://plotly.com)

#### deep-translator==1.11.4
- **Purpose**: Translation service integration
- **Size**: ~2MB
- **Dependencies**: beautifulsoup4, requests
- **Docs**: [github.com/nidhaloff/deep-translator](https://github.com/nidhaloff/deep-translator)

#### pillow==11.3.0
- **Purpose**: Image processing
- **Size**: ~5MB
- **Dependencies**: None (pure Python)
- **Docs**: [python-pillow.org](https://python-pillow.org)

#### pyyaml==6.0.3
- **Purpose**: YAML configuration parsing
- **Size**: ~1MB
- **Dependencies**: None
- **Docs**: [pyyaml.org](https://pyyaml.org)

#### python-dotenv==1.1.1
- **Purpose**: Environment variable loading
- **Size**: <1MB
- **Dependencies**: None
- **Docs**: [github.com/theskumar/python-dotenv](https://github.com/theskumar/python-dotenv)

### Total Installation Size

Approximate: **100-150MB** (including all dependencies)

### Installation Methods

**Using uv (recommended)**:
```bash
uv sync
```

**Using pip**:
```bash
pip install -r requirements.txt
```

---

## Performance Characteristics

### Generation Times

**Environment Generation** (4 images):
- Approximate: 30-60 seconds
- Factors: Prompt complexity, API load

**Product View Generation** (per product):
- Separate mode: ~60-90 seconds (6 views)
- Combined mode: ~60-90 seconds (6 views total)
- Factors: Number of reference images, prompt detail

**Ad Creative Generation**:
- Without localizations: ~60-90 seconds (3 ratios)
- With localizations (4 languages): ~3-5 minutes (12 images)
- Factors: Number of languages, image complexity

### Memory Usage

**Application baseline**: ~200-300MB
**Image generation spike**: +500MB - 1GB per generation
**Total recommended RAM**: 2GB minimum, 4GB recommended

### Disk Space

**Per campaign** (typical):
- Minimal: ~10-20MB (3 ads, 1 environment)
- Standard: ~50-100MB (12 localized ads, 4 environments)
- Large: ~100-200MB (multi-product, full localizations)

### Network Bandwidth

**API requests**:
- Outbound: ~1-5MB per request (prompts + reference images)
- Inbound: ~1-3MB per generated image
- Total per campaign: ~50-200MB

---

## Browser Compatibility

### Supported Browsers

- **Chrome/Edge**: v90+ (recommended)
- **Firefox**: v88+
- **Safari**: v14+
- **Mobile browsers**: iOS Safari 14+, Chrome Mobile

### Required Features

- WebSocket support
- ES6 JavaScript
- Flexbox/Grid CSS
- File upload API

---

## Security Considerations

### API Key Storage

- Never commit `.env` to git (included in `.gitignore`)
- Settings tab saves to `.env` with restricted permissions

### Input Validation

- Prompts sanitized before API calls
- File paths validated
- No arbitrary code execution

### Rate Limiting

- Handled by Gemini API
- No local rate limiting implemented
- Consider adding for production deployments

---

## Troubleshooting

### Common Technical Issues

**Import errors**:
```
ModuleNotFoundError: No module named 'gradio'
```
**Solution**: Run `uv sync` or `pip install -r requirements.txt`

**API authentication errors**:
```
401 Unauthorized
```
**Solution**: Check API key in Settings tab or `.env` file

**Port already in use**:
```
OSError: [Errno 48] Address already in use
```
**Solution**: Change PORT in environment or kill process using port 7860

**Out of memory**:
```
MemoryError
```
**Solution**: Increase system RAM or reduce concurrent generations

---

## API Response Format

### Successful Generation

```json
{
  "images": [
    {
      "imageBytes": "base64_encoded_png_data",
      "mimeType": "image/png"
    }
  ]
}
```

### Error Response

```json
{
  "error": {
    "code": 400,
    "message": "Invalid aspect ratio",
    "status": "INVALID_ARGUMENT"
  }
}
```

---

## Version History

### Current Version: 0.1.0

**Release Date**: November 2025

**Major Features**:
- Multi-product selection
- Campaign JSON export/import
- Self-contained campaign folders
- Localization support
- Three aspect ratios
- Interactive world map

See [DEVELOPMENT_LOG.md](DEVELOPMENT_LOG.md) for detailed version history.
