# Development Log - Creative Automation Pipeline

## Project Overview
Automated creative asset generation for social ad campaigns using Google's Gemini 2.5 Flash Image (Nano Banana) AI model.

---

## Development Timeline

### Session 1: Core Infrastructure & Multi-Product Generation

#### Initial Setup
- Created Gradio web interface with tabbed navigation
- Integrated Google Gemini API (gemini-2.5-flash-image)
- Set up uv package manager for dependency management
- Created basic project structure with products, config, and outputs directories

#### Multi-Product Selection & Generation
- **Feature**: Multi-select product dropdown
- **Feature**: Two generation modes:
  - **Separate Mode**: Generate individual 6-view sets for each product
  - **Combined Mode**: Generate 6 views showing all products together
- **Output Structure**:
  - Separate: `products/{product-slug}/photos/generated/`
  - Combined: `outputs/combined_{timestamp}/`

#### Campaign Configuration
- **Interactive World Map**: Plotly visualization mapping 6 regions to 100+ countries
  - Auto-highlighting selected regions in dark blue
  - Hover tooltips with region names
- **Quick Select Region Buttons**: One-click region selection with emoji indicators
- **6 Target Regions**: North America, Europe, Asia Pacific, Latin America, Middle East & Africa, Oceania
- **8 Target Audiences**: Health-Conscious Millennials, Busy Parents, Gen Z Trendsetters, Active Seniors, Fitness Enthusiasts, Eco-Conscious Consumers, Young Professionals, Budget-Conscious Shoppers
- **Enhanced Campaign Summary**: Rich markdown display with cultural context, visual preferences, audience demographics

#### Messaging & Translation
- **Campaign Message Input**: Text area with character counter
- **Randomize Feature**: 20 curated sample messages
- **Google Translate Integration**: Auto-translate to top 4 languages per region
- **Languages Configuration**: Added top_languages to regions.yaml (English, Spanish, French, Chinese, etc.)

#### Environment Generation
- **AI Background Generation**: Generate 4 environment variations (1:1 aspect ratio)
- **Randomize Feature**: 20 environment prompts (kitchens, cafes, gyms, etc.)
- **Output**: `outputs/environments/`

#### Asset Selection System
- **Click-to-Select**: Gallery-based selection for environments, products, and logos
- **Visual Feedback**: Separate preview and selected galleries
- **Toggle Selection**: Click to select/deselect
- **Clear Selection**: Individual clear buttons per asset type

---

### Session 2: Tab Organization & Workflow

#### Logo Management
- **Dedicated Logos Tab**: Separated from Products tab
- **Auto-Population**: Logos auto-populate based on selected products
- **Selection System**: Click-to-select with gallery view

#### Navigation System
- **Next/Previous Buttons**: Added to all tabs for workflow progression
- **Tab Navigation Fix**: Implemented proper Gradio 5.x tab navigation
  - Added unique IDs to all tabs (campaign, messaging, environments, products, logos, preview, generate, settings)
  - Used `gr.update(selected="tab_id")` pattern instead of integer indices
  - Fixed navigation buttons that weren't switching tabs

#### Preview Tab
- **Campaign Overview**: Complete summary of all settings
- **Asset Preview**: Display selected environments, products, and logos
- **Refresh Button**: Update preview with current selections
- **JSON Export**: Save campaign configuration to `outputs/campaigns/`

---

### Session 3: Ad Generation & Localization

#### Generate Tab - Initial Implementation
- **Three Aspect Ratios**:
  - 1:1 Square (1080x1080) - Instagram feed, Facebook posts
  - 9:16 Vertical (1080x1920) - Instagram Stories, TikTok, Reels
  - 16:9 Landscape (1920x1080) - YouTube, desktop ads
- **AI Synthesis**: Nano Banana composites product into environment with messaging overlay
- **Output**: `outputs/ads/`

#### Aspect Ratio Enforcement
- **Problem**: AI wasn't respecting aspect ratios from prompt alone
- **Solution**: Implemented proper Gemini API aspect ratio parameters
  - Added `from google.genai import types`
  - Used `GenerateContentConfig` with `ImageConfig(aspect_ratio="...")`
  - Applied to all generation functions (ads, environments, product views)
- **Result**: Accurate 1:1, 9:16, and 16:9 outputs

#### Logo Integration
- **Include Logo Checkboxes**: One per aspect ratio format
- **Conditional Logo Placement**: AI places logo in corner when enabled
- **Logo in Preview Tab**: Display selected logos in preview
- **Multi-Modal Input**: Pass logo as third reference image to AI

#### Localization System
- **Generate Localizations Checkboxes**: One per aspect ratio format
- **Translation Function**: `get_message_translations()` returns list of language/text pairs
- **Batch Generation**: Generate one ad per language when localization enabled
- **File Naming**: `ad_1_1_en_timestamp.png`, `ad_1_1_es_timestamp.png`, etc.
- **Gallery Display**: Changed from single Image to Gallery for showing multiple localized versions
- **Status Reporting**: Shows count and "(localized)" indicator

#### Simplified Messaging
- **Removed Custom Ad Copy Fields**: Eliminated optional ad copy textboxes for 1:1 and 16:9 formats
- **Unified Message Source**: All formats now use campaign message from Messaging tab
- **Consistent Workflow**: Single message → optional translations → localized ads

---

### Session 4: Enhanced Product Integration

#### Upgraded AI Prompting
**Problem**: Product perspective sometimes mismatched environment, products not prominent enough

**Solution**: Comprehensive prompt engineering improvements

#### Product Prominence & Focus
- Product as HERO/FOCAL POINT - prominently featured
- Position in FOREGROUND - taking up 40-60% of frame
- Medium-close composition highlighting product details
- Slightly closer to camera for depth and emphasis

#### Perspective Matching
- Match perspective EXACTLY to environment's viewing angle
- Align product orientation with scene's vanishing point and horizon line
- Product must physically exist within 3D space
- Maintain consistent scale - realistically sized
- Natural surface placement (on tables, counters, ground)
- Realistic shadows matching environment's lighting direction
- Reflections and highlights matching light sources

#### Lighting & Visual Coherence
- Product lighting MUST match environment exactly (color temp, intensity, direction)
- Match ambient light color - warm/cool tones consistent
- Align highlights and shadows with environment's light sources
- Add subtle environmental reflections on product surfaces

#### Typography Improvements
- Text prominently placed but not obscuring product
- Placement in top or bottom third, avoiding product area
- Visual hierarchy with bold headline and smaller body text
- Text complements not competes with product
- High contrast colors for readability

#### Final Output Checklist
1. Product as clear hero with prominent placement
2. Seamless integration with perfect perspective matching
3. Natural, realistic lighting and shadows
4. Clear, compelling advertising copy
5. Premium commercial campaign quality

---

## Technical Stack

### Core Technologies
- **Python 3.12+**
- **uv**: Fast Python package manager
- **Gradio 5.49.1**: Interactive web interface with tabbed navigation
- **Google Gemini 2.5 Flash Image**: AI image generation (nano banana model)
- **Pillow 11.3.0**: Image processing
- **PyYAML 6.0.3**: Configuration parsing
- **python-dotenv 1.1.1**: Environment variable management

### AI & Translation
- **google-genai 1.46.0**: Gemini API client
- **deep-translator 1.11.4**: Google Translate integration

### Visualization
- **Plotly 6.3.1**: Interactive world map visualization

---

## Architecture

### Directory Structure
```
creative-automation-pipeline/
├── app.py                          # Main Gradio application
├── config/                         # Campaign configuration
│   ├── regions.yaml                # 6 target regions with cultural context
│   └── audiences.yaml              # 8 target audiences with demographics
├── products/                       # Product assets
│   └── {product-slug}/
│       ├── config.yaml             # Product metadata
│       └── photos/
│           ├── product/            # Reference photos
│           ├── logo/               # Company logos
│           └── generated/          # AI-generated views
├── outputs/                        # Generated assets
│   ├── ads/                        # Final ad creatives
│   ├── campaigns/                  # Campaign config exports
│   ├── combined_{timestamp}/       # Combined product views
│   └── environments/               # Generated backgrounds
├── .env                            # API keys (not in git)
├── .env.example                    # Environment template
├── pyproject.toml                  # Dependencies
└── README.md                       # Documentation
```

### Key Functions

#### Image Generation
- `generate_environments()`: Create 4 background variations with 1:1 aspect ratio
- `generate_product_views()`: Generate 6-view product shots (separate or combined mode)
- `generate_ad_compositions()`: Synthesize final ads in 3 aspect ratios with optional localization

#### Translation & Localization
- `translate_message()`: Display translations in Messaging tab
- `get_message_translations()`: Return list of translations for programmatic use
- Supports top 4 languages per region

#### Configuration
- `load_regions_config()`: Load regions.yaml
- `load_audiences_config()`: Load audiences.yaml
- `load_product_config()`: Load product-specific config.yaml
- `export_campaign_config()`: Export campaign to JSON

---

## API Integration

### Gemini 2.5 Flash Image
- **Model**: `gemini-2.5-flash-image`
- **Image-to-Image Generation**: Pass reference images + prompt
- **Aspect Ratio Control**: `ImageConfig(aspect_ratio="1:1"|"9:16"|"16:9")`
- **Multi-Modal Input**: Text prompt + environment image + product image + optional logo

### Google Translate
- **Library**: deep-translator with GoogleTranslator
- **Auto-detect source language**
- **Regional language sets**: Top 4 languages per region

---

## Configuration Schema

### regions.yaml
```yaml
region_key:
  name: "Region Name"
  description: "Brief description"
  countries: ["Country1", "Country2", ...]
  cultural_context:
    - "Context point 1"
    - "Context point 2"
  visual_preferences:
    colors: ["Color palette"]
    imagery: ["Image style"]
  messaging:
    tone: ["Tone characteristics"]
    themes: ["Common themes"]
  top_languages:
    - code: "en"
      name: "English"
    - code: "es"
      name: "Spanish"
```

### audiences.yaml
```yaml
audience_key:
  name: "Audience Name"
  age_range: "25-40"
  demographics:
    - "Demographic info"
  psychographics:
    - "Psychographic info"
  messaging_preferences:
    tone: ["Tone style"]
    themes: ["Themes that resonate"]
```

### Product config.yaml
```yaml
product:
  name: "Product Name"
  description: "Product description"
  category: "Category"
company:
  name: "Company Name"
  tagline: "Company tagline"
```

---

## Feature Highlights

### 1. Multi-Product Generation
- Select 1 or more products
- Generate individual views OR combined product bundles
- Automatic output organization

### 2. Campaign Targeting
- Visual world map with 100+ countries
- 6 regions × 8 audiences = 48 targeting combinations
- Cultural context and messaging guidance

### 3. Localization at Scale
- Translate campaign message to 4 languages
- Generate localized ads with one click
- Example: 3 formats × 4 languages = 12 ad variations

### 4. Professional Quality
- AI-powered product integration with proper perspective
- Environment-aware lighting and shadows
- Typography that complements product
- Commercial-ready output

### 5. Workflow Efficiency
- Tab-based progressive workflow
- Preview before generation
- JSON export for campaign tracking
- Randomize buttons for creative inspiration

---

### Session 5: Repository Preparation & GitHub Integration

#### Enhanced Product Integration (Continued)
**Date**: October 26, 2024

**Problem Identified**: Product shots not well-integrated - perspective mismatches and products not prominent enough

**Solution Implemented**: Comprehensive prompt engineering overhaul

#### Upgraded AI Prompting - Product Focus
- **Product Prominence Requirements**:
  - Product as HERO/FOCAL POINT of composition
  - Position in FOREGROUND taking up 40-60% of frame
  - Medium-close composition highlighting product details
  - Slightly closer to camera for depth and emphasis

#### Perspective Matching Improvements
- **Exact Perspective Alignment**:
  - Match product perspective to environment's viewing angle
  - Align orientation with scene's vanishing point and horizon line
  - Product must physically exist within 3D space
  - Maintain consistent scale - realistically sized
  - Natural surface placement (on tables, counters, ground)
  - Realistic shadows matching lighting direction
  - Reflections and highlights matching light sources

#### Lighting & Visual Coherence
- **Environment-Aware Lighting**:
  - Product lighting MUST match environment exactly (color temp, intensity, direction)
  - Match ambient light color - warm/cool tones consistent
  - Align highlights and shadows with environment's light sources
  - Add subtle environmental reflections on product surfaces

#### Typography & Layout Enhancements
- **Improved Text Placement**:
  - Text prominently placed but not obscuring product
  - Placement in top or bottom third, avoiding product area
  - Visual hierarchy with bold headline and smaller body text
  - Text complements not competes with product
  - High contrast colors for readability

#### Localization System Implementation
**Feature**: Generate ads in multiple languages automatically

**Implementation**:
1. **Created `get_message_translations()` helper function**:
   - Returns list of translations for region's top languages
   - Each translation includes language name, code, and text
   - Handles translation errors gracefully
   - Reuses Google Translate integration

2. **Added Localization Checkboxes**:
   - One checkbox per aspect ratio format (1:1, 9:16, 16:9)
   - Info tooltip: "Generate versions in all regional languages"
   - Positioned next to "Include Logo" checkbox

3. **Updated Generation Logic**:
   - Check if any format has localization enabled
   - Fetch translations from selected region (top 4 languages)
   - For each localized format, generate one ad per language
   - For non-localized formats, generate single ad
   - File naming: `ad_1_1_es_timestamp.png`, `ad_1_1_fr_timestamp.png`, etc.

4. **Changed Preview Components to Galleries**:
   - Changed from single `gr.Image` to `gr.Gallery` for each format
   - Configured with 3 columns, 2 rows
   - Supports displaying albums of localized images

5. **Enhanced Progress Tracking**:
   - Calculates total generations (accounting for localizations)
   - Shows language during generation: "Generating 1:1 ad (Spanish)..."
   - Improved status messages showing count and "(localized)" indicator

**Example Output**:
- Without localization: 3 images (1 per format)
- With 1:1 localized: 6 images (4 for 1:1 + 1 each for 9:16 and 16:9)
- With full localization: 12 images (4 languages × 3 formats)

#### Simplified Messaging Workflow
**Change**: Removed optional ad copy textboxes

**Rationale**:
- Simplify user experience
- Ensure consistency across all formats
- Single source of truth for messaging

**Implementation**:
- Removed `ad_copy_1_1` and `ad_copy_16_9` textbox components
- Updated all formats to use campaign message from Messaging tab
- Updated function signature to remove custom copy parameters
- All ads now consistently use the same messaging

#### Repository Preparation for GitHub

**GitHub CLI Installation**:
- Installed GitHub CLI via Homebrew: `brew install gh`
- Version 2.82.1 successfully installed

**Comprehensive .gitignore Creation**:
- **Excluded**: Environment variables and secrets (.env, *.key, *.pem, credentials.json)
- **Excluded**: Python artifacts (__pycache__, *.pyc, build/, dist/, *.egg-info)
- **Excluded**: Virtual environments (.venv/, venv/, ENV/)
- **Excluded**: IDEs and editors (.vscode/, .idea/, *.swp, .DS_Store)
- **Excluded**: Generated images and outputs:
  - `products/*/photos/generated/**` (150 files)
  - `outputs/**` (111 files)
- **Included**: Product reference images and logos (30 files)
  - `products/*/photos/product/**`
  - `products/*/photos/logo/**`

**Documentation Created**:
1. **DEVELOPMENT_LOG.md** (14,724 bytes):
   - Comprehensive development history
   - Technical implementation details
   - Lessons learned and best practices
   - Version history

2. **Updated README.md** (14,319 bytes):
   - Complete feature overview
   - Quick start guide
   - Step-by-step usage instructions
   - API configuration guide
   - Troubleshooting section
   - Repository URL: https://github.com/mitchaiet/creative-pipeline-automation

3. **LICENSE** (MIT License):
   - Standard MIT License for open source

4. **.env.example** (135 bytes):
   - Template with `GOOGLE_API_KEY=your_api_key_here`
   - Safe to commit (no actual secrets)

**Security Verification**:
-  Verified no hardcoded API keys in codebase
-  Verified `.env` excluded via `.gitignore`
-  Verified `.env.example` contains placeholder only
-  Searched for common API key patterns (AIza, sk-, pk-, ghp_) - none found
-  All sensitive outputs excluded from repository

**File Statistics**:
- **To be included**: 30 reference images (product photos and logos)
- **To be excluded**: 261 generated images (150 product views + 111 outputs)
- **Documentation**: 5 markdown files (README, DEVELOPMENT_LOG, 3 guides)
- **Code**: app.py (87,891 bytes), configuration files, test files

**Git Repository Setup**:
1. Initialized git repository in clean codebase
2. Copied critical files from working directory:
   - `.gitignore` (1,256 bytes) - prevents pushing sensitive data
   - `.env.example` (135 bytes) - template for users
3. Staged all files: `git add .`
4. Created initial commit with comprehensive message
5. Added remote: `https://github.com/mitchaiet/creative-pipeline-automation.git`

**GitHub Push Challenges**:
- **Issue**: HTTP 400 error when pushing
- **Cause**: Large binary files (product images up to 2.7MB)
- **Solution Attempted**: Increased git http buffer to 500MB
  ```bash
  git config http.postBuffer 524288000
  ```
- **Status**: Commit created locally, push pending resolution

**Files Ready for Repository**:
-  107 files modified/added
-  3,759 lines of code added
-  All documentation complete
-  Security verified
-  .gitignore properly configured

---

## Known Limitations & Future Improvements

### Current Limitations
- Single environment/product per ad generation (uses first selected)
- No batch processing across multiple environment/product combinations
- No A/B testing variations
- No video/animation support

### Planned Enhancements
- [ ] Scene generation with target region/audience context (Step 2)
- [ ] Multi-aspect ratio outputs in single generation
- [ ] Advanced text overlay controls (Step 3)
- [ ] Logo positioning controls (Step 4)
- [ ] Output organization system (Step 5)
- [ ] Agentic monitoring system (Task 2)
- [ ] Batch generation across product/environment matrices
- [ ] A/B testing variant generation
- [ ] Campaign performance tracking

---

## Development Notes

### Lessons Learned

1. **Gradio 5.x Tab Navigation**: Must use string IDs and `gr.update(selected="id")`, not integer indices
2. **Aspect Ratio Enforcement**: AI prompt alone insufficient; must use API parameters
3. **Prompt Engineering**: Detailed, structured prompts with specific percentages (40-60% frame) yield better results
4. **Multi-Modal AI**: Order matters - prompt first, then reference images in logical sequence
5. **Localization UX**: Gallery view better than single image for showing language variations

### Best Practices Established

1. **Progressive Workflow**: Tab navigation guides user through campaign setup → generation
2. **Preview Before Generate**: Let users verify selections before expensive AI calls
3. **Status Messages**: Clear, detailed status with counts and indicators
4. **File Naming**: Descriptive names with timestamps and language codes
5. **Error Handling**: Check API keys, selections, and provide helpful error messages

---

## Version History

### v0.1.0 - Initial Release
- Core Gradio interface
- Product view generation (6 angles)
- Multi-product support (separate/combined modes)
- Campaign configuration (regions/audiences)
- Environment generation
- Basic ad synthesis

### v0.2.0 - Enhanced Workflow
- Tab navigation system
- Logo management
- Preview tab with JSON export
- Asset selection system
- Translation integration

### v0.3.0 - Advanced Generation
- Aspect ratio enforcement
- Logo integration in ads
- Localization system
- Enhanced product integration prompts
- Gallery-based preview for variations

### v0.4.0 - Repository Release (October 26, 2024)
- Comprehensive prompt engineering for better product integration
- Multi-language localization with gallery view
- Simplified messaging workflow (single source of truth)
- Complete documentation suite (README, DEVELOPMENT_LOG, guides)
- MIT License
- Security-hardened .gitignore
- GitHub repository preparation
- 30 example product assets included

---

## Contributors
- Initial development and feature implementation
- AI prompt engineering and optimization
- Gradio interface design

---

## License
See LICENSE file for details

---

## Contact & Support
For issues, feature requests, or contributions, please see the main README.md
