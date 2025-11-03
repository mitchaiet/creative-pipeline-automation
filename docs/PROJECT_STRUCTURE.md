# Project Structure

Detailed overview of the Creative Automation Pipeline architecture and file organization.

---

## Directory Tree

```
creative-automation-pipeline/
├── src/
│   └── app.py                  # Main Gradio application (5000+ lines)
├── pyproject.toml              # uv project configuration
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variable template
├── .env                        # Environment variables (API keys)
├── .gitignore                  # Git ignore rules
│
├── config/                     # Campaign configuration files
│   ├── regions.yaml            # 6 target regions with cultural context
│   └── audiences.yaml          # 8 target audience profiles
│
├── products/                   # Product asset library
│   ├── eco-cleaner/
│   │   ├── config.yaml         # Product metadata
│   │   └── photos/
│   │       ├── product/        # Reference product photos
│   │       ├── logo/           # Company logos
│   │       └── generated/      # AI-generated product views
│   ├── gourmet-coffee/
│   ├── herbal-tea/
│   ├── noise-cancelling-headphones/
│   ├── protein-bar/
│   ├── running-shoes/
│   ├── smart-watch/
│   ├── sparkling-water/
│   ├── travel-backpack/
│   └── yoga-mat/
│
├── outputs/                    # Generated campaign outputs
│   ├── {CAMPAIGN_ID}/          # Self-contained campaign folder
│   │   ├── environments/       # Generated environment backgrounds
│   │   │   └── environment_*_{timestamp}.png
│   │   ├── products/           # Generated product views
│   │   │   ├── {product-slug}/ # Individual product views (Separate mode)
│   │   │   │   └── {view}_{timestamp}.png
│   │   │   └── combined/       # Combined product views (Combined mode)
│   │   │       └── combined_{view}_{timestamp}.png
│   │   ├── ads/                # Final ad creatives
│   │   │   ├── 1_1/            # Square ads (1080x1080)
│   │   │   │   └── ad_1_1_{lang}_{timestamp}.png
│   │   │   ├── 9_16/           # Vertical ads (1080x1920)
│   │   │   │   └── ad_9_16_{lang}_{timestamp}.png
│   │   │   └── 16_9/           # Landscape ads (1920x1080)
│   │   │       └── ad_16_9_{lang}_{timestamp}.png
│   │   └── campaign_config.json # Complete campaign configuration
│   │
│   └── {ANOTHER_CAMPAIGN_ID}/  # Another campaign folder
│
├── docs/                       # Documentation
│   ├── FEATURES.md             # Complete feature overview
│   ├── USER_GUIDE.md           # Step-by-step usage instructions
│   ├── PROJECT_STRUCTURE.md    # This file
│   ├── TECHNICAL_REFERENCE.md  # API, tech stack, naming conventions
│   ├── DEVELOPMENT.md          # Development and contribution guide
│   ├── MULTI_PRODUCT_GUIDE.md  # Multi-product generation guide
│   ├── CAMPAIGN_CONFIG_GUIDE.md # Regions and audiences reference
│   ├── GENERATION_GUIDE.md     # Camera angles and prompt strategies
│   ├── AGENTIC_SYSTEM.md       # Agentic workflow documentation
│   └── DEVELOPMENT_LOG.md      # Detailed development history
│
├── old/                        # Legacy/unused files
│   ├── test_agent.py
│   ├── test_images.py
│   ├── test_app.py
│   ├── demo_agent.py
│   ├── run_agent.py
│   └── agent/                  # Old monitoring module
│
└── .claude/                    # Claude Code configuration
    └── settings.local.json     # Local permissions
```

---

## Core Application

### src/app.py

The main application file containing all functionality:

**Structure:**
- ~5000+ lines of Python
- Gradio 5.49.1 interface
- Single-file architecture for simplicity

**Key Sections:**

#### 1. Imports & Setup (Lines 1-50)
- Library imports
- Environment variable loading
- API client initialization
- Constants and configuration

#### 2. Helper Functions (Lines 51-200)
- File management utilities
- Image processing functions
- Campaign ID generation
- Translation helpers

#### 3. Configuration Loading (Lines 201-300)
- `load_regions()` - Load regions.yaml
- `load_audiences()` - Load audiences.yaml
- `load_product_config()` - Parse product configs
- Region/audience data structures

#### 4. Product Generation (Lines 301-500)
- `generate_product_views()` - Main product generation
- Separate mode implementation
- Combined mode implementation
- Multi-product handling

#### 5. Environment Generation (Lines 501-700)
- `generate_environments()` - Background generation
- Preset prompts
- Image saving logic

#### 6. Ad Generation (Lines 701-1000)
- `generate_ad_compositions()` - Final ad creation
- Multi-aspect ratio handling
- Localization support
- Logo integration

#### 7. Campaign Management (Lines 1001-1300)
- `save_campaign_config()` - Export to JSON
- `load_campaign_from_json()` - Import from JSON
- Campaign preview logic
- Outputs browser

#### 8. UI Components (Lines 1301-2000)
- World map creation (Plotly)
- Gallery interfaces
- Dropdown menus
- Text inputs and buttons

#### 9. Tab Definitions (Lines 2001-2500)
- Campaign tab
- Messaging tab
- Environments tab
- Products tab
- Logos tab
- Preview tab
- Generate tab
- Settings tab

#### 10. Event Handlers (Lines 2501-3000)
- Button click handlers
- Dropdown change handlers
- Gallery selection logic
- Navigation between tabs
- State management

#### 11. App Launch (Lines 3001-3100)
- Gradio interface assembly
- Server configuration
- Port binding

---

## Configuration Files

### config/regions.yaml

Defines 6 target regions with rich cultural context:

```yaml
north_america:
  name: "North America"
  description: "United States, Canada, Mexico"
  countries: ["USA", "Canada", "Mexico"]
  cultural_context:
    - "Direct and value-driven messaging"
    - "Emphasis on innovation and convenience"
    - "Diverse multicultural audience"
  visual_preferences:
    colors: ["Bold primaries", "Clean whites", "Corporate blues"]
    imagery: ["Aspirational lifestyles", "Modern minimalism", "Urban energy"]
  messaging:
    tone: ["Confident", "Aspirational", "Direct"]
    themes: ["Freedom", "Innovation", "Quality of life"]
  top_languages:
    - code: "en"
      name: "English"
    - code: "es"
      name: "Spanish"
    - code: "fr"
      name: "French"
    - code: "zh-CN"
      name: "Chinese (Simplified)"
```

**Used for:**
- Region selection dropdown
- World map country mapping
- Cultural messaging guidance
- Language translation options

### config/audiences.yaml

Defines 8 target audience segments:

```yaml
health_conscious_millennials:
  name: "Health-Conscious Millennials"
  demographics:
    age_range: "25-40"
    characteristics: ["Wellness-focused", "Active lifestyle", "Social media savvy"]
  messaging_preferences:
    tone: ["Authentic", "Informative", "Positive"]
    themes: ["Wellness", "Sustainability", "Community"]
    key_values: ["Transparency", "Natural ingredients", "Social responsibility"]
  visual_preferences:
    colors: ["Earth tones", "Fresh greens", "Natural palettes"]
    imagery: ["Lifestyle shots", "Natural settings", "Clean aesthetics"]
```

**Used for:**
- Audience selection dropdown
- Campaign configuration
- Messaging tone guidance
- Visual style recommendations

---

## Product Assets

### Product Folder Structure

Each product has a standardized folder structure:

```
products/{product-slug}/
├── config.yaml           # Product metadata
└── photos/
    ├── product/          # Reference photos (required)
    │   ├── photo1.jpg
    │   ├── photo2.png
    │   └── ...
    ├── logo/             # Company logos (optional)
    │   ├── logo.png
    │   └── ...
    └── generated/        # AI-generated views (created by app)
        ├── front_{timestamp}.png
        ├── back_{timestamp}.png
        └── ...
```

### config.yaml Format

```yaml
product:
  name: "Eco-Friendly All-Purpose Cleaner"
  description: "Plant-based cleaning solution in recyclable packaging"
  category: "Home & Cleaning"

company:
  name: "GreenClean Co."
  tagline: "Clean Conscience, Clean Home"
```

**Fields:**
- `product.name` - Display name for UI
- `product.description` - Used in AI prompts
- `product.category` - Organizational metadata
- `company.name` - Brand name
- `company.tagline` - Optional marketing tagline

---

## Output Structure

### Campaign Folder Anatomy

Each campaign generates a self-contained folder:

```
outputs/{CAMPAIGN_ID}/
├── campaign_config.json        # Complete campaign configuration
├── environments/               # Generated backgrounds
│   ├── environment_1_{timestamp}.png
│   ├── environment_2_{timestamp}.png
│   ├── environment_3_{timestamp}.png
│   └── environment_4_{timestamp}.png
├── products/
│   ├── eco-cleaner/           # Separate mode outputs
│   │   ├── front_{timestamp}.png
│   │   ├── back_{timestamp}.png
│   │   ├── left_{timestamp}.png
│   │   ├── right_{timestamp}.png
│   │   ├── top-down_{timestamp}.png
│   │   └── bottom-up_{timestamp}.png
│   └── combined/              # Combined mode outputs
│       ├── combined_front_{timestamp}.png
│       ├── combined_back_{timestamp}.png
│       └── ...
└── ads/
    ├── 1_1/                   # Square ads
    │   ├── ad_1_1_en_{timestamp}.png
    │   ├── ad_1_1_es_{timestamp}.png
    │   └── ...
    ├── 9_16/                  # Vertical ads
    │   ├── ad_9_16_en_{timestamp}.png
    │   └── ...
    └── 16_9/                  # Landscape ads
        ├── ad_16_9_en_{timestamp}.png
        └── ...
```

### campaign_config.json Structure

```json
{
  "campaign": {
    "name": "Campaign E2E6K6",
    "id": "E2E6K6",
    "created_at": "2025-11-02T13:45:00",
    "source": "manual",
    "type": "manual_generation"
  },
  "targeting": {
    "region": {
      "key": "north_america",
      "name": "North America",
      "countries": ["USA", "Canada", "Mexico"]
    },
    "audience": {
      "key": "health_conscious_millennials",
      "name": "Health-Conscious Millennials"
    }
  },
  "messaging": {
    "primary": "Transform your wellness routine with natural ingredients",
    "translations": {
      "en": "Transform your wellness routine...",
      "es": "Transforma tu rutina de bienestar...",
      "fr": "Transformez votre routine bien-être...",
      "zh-CN": "用天然成分改变您的健康习惯..."
    }
  },
  "assets": {
    "environments": [
      "outputs/E2E6K6/environments/environment_1_20251102_134500.png"
    ],
    "products": [
      "products/eco-cleaner/photos/product/bottle-front.jpg"
    ],
    "logos": [
      "products/eco-cleaner/photos/logo/greenclean-logo.png"
    ]
  },
  "generation_settings": {
    "aspect_ratios": ["1_1", "9_16", "16_9"],
    "localization_enabled": true,
    "logo_inclusion": true
  }
}
```

---

## Data Flow

### Campaign Creation Flow

```
1. User selects region → Updates campaign state
2. User selects audience → Updates campaign state
3. User enters message → Saves to state
4. User generates environments → Saves to outputs/{ID}/environments/
5. User selects products → Loads product configs
6. User generates product views → Saves to outputs/{ID}/products/
7. User selects logos → Tracks in state
8. User previews campaign → Displays all state
9. User generates ads → Saves to outputs/{ID}/ads/
10. System saves campaign_config.json → outputs/{ID}/
```

### State Management

Gradio state variables track:
- `campaign_id_state` - Current campaign ID (persists across tabs)
- `selected_env_state` - List of selected environment image paths
- `selected_product_state` - List of selected product image paths
- `selected_logo_state` - List of selected logo image paths
- Region and audience selections (via dropdowns)

### File Naming Patterns

**Timestamps:**
- Format: `YYYYMMDD_HHMMSS`
- Example: `20251102_134500`
- Used for: Individual file naming within folders

**Campaign IDs:**
- Format: 6 alphanumeric characters (uppercase)
- Example: `E2E6K6`, `K24SAG`, `UL8M9Y`
- Generated: Random on first generation
- Used for: Folder naming

**Language Codes:**
- ISO 639-1 format (2 letters) or extended
- Examples: `en`, `es`, `fr`, `zh-CN`
- Used for: Localized ad file names

---

## Technology Integration

### Gradio Interface

**Components used:**
- `gr.Dropdown` - Region, audience, product selection
- `gr.Textbox` - Message input, prompts
- `gr.Gallery` - Image selection and preview
- `gr.Button` - Generation triggers, navigation
- `gr.Markdown` - Info displays, summaries
- `gr.JSON` - Configuration preview
- `gr.Plot` - Interactive world map (Plotly)
- `gr.File` - JSON upload
- `gr.State` - Persistent data across tabs
- `gr.Tabs` - Workflow organization

### Google Gemini API

**Integration:**
- Library: `google-genai` SDK
- Model: `gemini-2.5-flash-image`
- Input: Multi-modal (text + images)
- Output: Generated PNG images

**Generation functions:**
- `generate_environments()` - Text-to-image
- `generate_product_views()` - Image-to-image with text
- `generate_ad_compositions()` - Multi-modal synthesis

### Translation API

**Integration:**
- Library: `deep-translator`
- Service: Google Translate
- Input: Campaign message + target language
- Output: Translated strings

---

## Deployment Configuration

### Local Development

**Requirements:**
- Python 3.12+
- uv package manager
- `.env` file with API key

**Run command:**
```bash
uv run python src/app.py
```

---

## Extension Points

### Adding New Products

1. Create folder: `products/{new-product-slug}/`
2. Add `config.yaml` with product metadata
3. Add reference photos to `photos/product/`
4. Add logos to `photos/logo/`
5. Product auto-appears in dropdown

### Adding New Regions

1. Edit `config/regions.yaml`
2. Add new region with required fields
3. Update world map country mapping (in app.py)
4. Region auto-appears in dropdown

### Adding New Audiences

1. Edit `config/audiences.yaml`
2. Add new audience with demographics
3. Audience auto-appears in dropdown

### Adding New Features

Key areas to modify in `app.py`:
- **UI Components** - Lines 1301-2000
- **Event Handlers** - Lines 2501-3000
- **Generation Logic** - Lines 301-1000
- **State Management** - Gradio State variables

---

## File Size Considerations

### Generated Images

**Typical sizes:**
- Environment: ~500KB - 2MB (1:1 square)
- Product view: ~300KB - 1MB (white background)
- Ad creative: ~1MB - 3MB (complex composition)

**Campaign totals:**
- Minimal (no localizations): ~10-20MB
- With localizations (4 languages): ~50-100MB
- Large multi-product: ~100-200MB

### Storage Management

**Cleanup strategies:**
- Old campaigns can be deleted manually
- Keep campaign JSON for reproducibility
- Archive successful campaigns externally
- Clear unused environment variations

---

## Security Considerations

### API Key Storage

- Stored in `.env` file (gitignored)
- Can also be stored via Settings tab
- Never committed to repository

### File Upload

- JSON loading validates structure
- File paths validated before access
- No arbitrary code execution

### User Input

- Prompts sanitized before API calls
- File paths validated
- No SQL injection risk (no database)
