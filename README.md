# Creative Automation Pipeline

Automated creative asset generation for social ad campaigns using Google's Gemini 2.5 Flash Image AI (Nano Banana).

Generate professional, localized advertising creatives at scale with AI-powered product integration, multi-language support, and campaign-specific targeting.

---

## Features

### 🎯 Campaign Configuration
- **Interactive World Map**: Visual representation mapping 6 regions to 100+ countries
- **6 Target Regions**: North America, Europe, Asia Pacific, Latin America, Middle East & Africa, Oceania
- **8 Target Audiences**: Health-Conscious Millennials, Busy Parents, Gen Z Trendsetters, Active Seniors, Fitness Enthusiasts, Eco-Conscious Consumers, Young Professionals, Budget-Conscious Shoppers
- **Cultural Context**: Region-specific insights on visual preferences, messaging tone, and cultural considerations

### 💬 Messaging & Translation
- Campaign message editor with character counter
- Google Translate integration for regional languages
- Top 4 languages per region (English, Spanish, French, Chinese, etc.)
- 20 curated sample messages with randomize feature

### 🌄 Environment Generation
- AI-powered background environment creation
- Generate 4 variations per prompt in 1:1 aspect ratio
- 20 preset environment prompts (kitchens, cafes, gyms, outdoor scenes, etc.)
- Click-to-select gallery for choosing backgrounds

### 📦 Product Management
- **Multi-Product Selection**: Choose one or more products
- **Two Generation Modes**:
  - **Separate**: Individual 6-view sets per product
  - **Combined**: All products together in single images
- **6 Product Views**: front, back, left, right, top-down, bottom-up
- AI maintains consistent appearance, colors, and branding

### 🏷️ Logo Integration
- Dedicated logo asset management
- Auto-population from selected products
- Optional logo placement in generated ads
- Subtle corner placement that doesn't overwhelm

### 👁️ Campaign Preview
- Complete overview of all campaign settings
- Preview selected assets (environments, products, logos)
- JSON export for campaign configuration
- Refresh to update with current selections

### 🎨 Ad Generation
- **Three Aspect Ratios**:
  - 1:1 Square (1080x1080) - Instagram feed, Facebook posts
  - 9:16 Vertical (1080x1920) - Instagram Stories, TikTok, Reels
  - 16:9 Landscape (1920x1080) - YouTube, desktop ads
- **AI-Powered Synthesis**:
  - Product as hero (40-60% of frame)
  - Perfect perspective matching
  - Environment-aware lighting and shadows
  - Professional typography
- **Localization Support**: Generate ads in multiple languages
  - One-click generation for all regional languages
  - Separate files per language
  - Gallery view for all variations

### 🔄 Workflow Navigation
- Tab-based progressive workflow
- Next/Previous buttons on all tabs
- Guided process from campaign setup to generation

---

## Quick Start

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager
- [Google Gemini API key](https://ai.google.dev/)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/mitchaiet/creative-pipeline-automation.git
cd creative-pipeline-automation
```

2. Install dependencies:
```bash
uv sync
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

4. Run the application:
```bash
uv run python app.py
```

5. Open your browser to `http://localhost:7860`

---

## Usage Guide

### 1. Configure Campaign (Campaign Tab)

1. **Select Target Region**:
   - Use the interactive world map
   - Click quick-select region buttons, or
   - Choose from dropdown menu

2. **Select Target Audience**:
   - Choose from 8 predefined audience segments
   - Review demographics and messaging preferences

3. **Review Campaign Summary**:
   - See cultural context and visual preferences
   - Understand messaging tone and themes

### 2. Create Messaging (Messaging Tab)

1. **Enter Campaign Message**:
   - Write your campaign copy
   - Use the randomize button for inspiration

2. **Translate (Optional)**:
   - Click "Translate Message" to see regional languages
   - View translations in top 4 languages for your selected region

### 3. Generate Environments (Environments Tab)

1. **Enter Environment Prompt**:
   - Describe the background scene you want
   - Use the randomize button for preset options

2. **Generate Backgrounds**:
   - Click "Generate Environments"
   - 4 variations created in 1:1 aspect ratio

3. **Select Environment**:
   - Click images to select
   - Selected images move to "Selected Images" gallery

### 4. Manage Products (Products Tab)

1. **Select Products**:
   - Multi-select from dropdown
   - Preview product photos and logos

2. **Generate Product Views (Optional)**:
   - Choose Separate or Combined mode
   - Generate 6-angle views with AI
   - Uses existing photos as reference

3. **Select Product Images**:
   - Click to select specific product shots
   - Selected images move to dedicated gallery

### 5. Manage Logos (Logos Tab)

1. **Review Auto-Populated Logos**:
   - Logos load automatically from selected products

2. **Select Logos**:
   - Click to select which logos to use
   - Selected logos available for ad generation

### 6. Preview Campaign (Preview Tab)

1. **Review Settings**:
   - Campaign configuration summary
   - Messaging and translations
   - Selected assets preview

2. **Refresh**:
   - Click "Refresh Preview" to update

3. **Export (Optional)**:
   - Save campaign configuration to JSON
   - File saved to `outputs/campaigns/`

### 7. Generate Ads (Generate Tab)

1. **Configure Options**:
   - **Include Logo**: Check to add logo to each format
   - **Generate Localizations**: Check to create language variations

2. **Generate Ads**:
   - Click "Generate All Ad Formats"
   - Creates ads in 1:1, 9:16, and 16:9 aspect ratios

3. **Review Output**:
   - Gallery displays all generated variations
   - Localized versions shown when enabled
   - Files saved to `outputs/ads/`

### 8. Configure Settings (Settings Tab)

1. **API Key**:
   - Enter Google Gemini API key
   - Click "Save API Key"
   - Verify status shows ✅

---

## Project Structure

```
creative-automation-pipeline/
├── app.py                          # Main Gradio application
├── config/                         # Campaign configuration
│   ├── regions.yaml                # 6 target regions with cultural context
│   └── audiences.yaml              # 8 target audiences
├── products/                       # Product assets
│   └── {product-slug}/
│       ├── config.yaml             # Product metadata
│       └── photos/
│           ├── product/            # Reference photos
│           ├── logo/               # Company logos
│           └── generated/          # AI-generated views
├── outputs/                        # Generated assets
│   ├── ads/                        # Final ad creatives
│   ├── campaigns/                  # Campaign config exports (JSON)
│   ├── combined_{timestamp}/       # Combined product views
│   └── environments/               # Generated backgrounds
├── pyproject.toml                  # Dependencies
├── .env.example                    # Environment template
├── .gitignore                      # Git ignore rules
├── README.md                       # This file
├── DEVELOPMENT_LOG.md              # Detailed development notes
├── MULTI_PRODUCT_GUIDE.md          # Multi-product feature guide
└── CAMPAIGN_CONFIG_GUIDE.md        # Campaign configuration guide
```

---

## Available Products

- `eco-cleaner` - Eco-friendly cleaning solution
- `gourmet-coffee` - Premium coffee beans
- `herbal-tea` - Organic herbal tea
- `noise-cancelling-headphones` - Premium headphones
- `protein-bar` - High-protein energy bar
- `running-shoes` - Athletic running shoes
- `smart-watch` - Fitness smartwatch
- `sparkling-water` - Flavored sparkling water
- `travel-backpack` - Durable travel backpack
- `yoga-mat` - Premium yoga mat

---

## Technology Stack

- **Python 3.12+**: Core language
- **uv**: Fast Python package manager
- **Gradio 5.49.1**: Interactive web interface
- **Google Gemini 2.5 Flash Image**: AI image generation
- **Plotly 6.3.1**: Interactive world map
- **deep-translator 1.11.4**: Google Translate integration
- **Pillow 11.3.0**: Image processing
- **PyYAML 6.0.3**: Configuration parsing
- **python-dotenv 1.1.1**: Environment management

---

## API Configuration

### Getting a Gemini API Key

1. Go to [Google AI Studio](https://ai.google.dev/)
2. Sign in with your Google account
3. Click "Get API Key"
4. Create a new API key
5. Copy the key to your `.env` file

### API Usage Notes

- Free tier available with usage limits
- Image generation uses Gemini 2.5 Flash Image model
- Aspect ratios enforced via API parameters (1:1, 9:16, 16:9)
- Multi-modal input: text prompts + reference images

---

## File Naming Conventions

### Product Views
- Separate mode: `{view}_{timestamp}.png`
  - Example: `front_20251026_120000.png`
- Combined mode: `combined_{view}_{timestamp}.png`
  - Example: `combined_front_20251026_120000.png`

### Environments
- Format: `environment_{number}_{timestamp}.png`
- Example: `environment_1_20251026_120000.png`

### Generated Ads
- Non-localized: `ad_{ratio}_{timestamp}.png`
  - Example: `ad_1_1_20251026_120000.png`
- Localized: `ad_{ratio}_{language-code}_{timestamp}.png`
  - Example: `ad_1_1_es_20251026_120000.png` (Spanish)
  - Example: `ad_9_16_fr_20251026_120000.png` (French)

---

## Advanced Features

### Localization

Generate ads in multiple languages automatically:

1. Select region in Campaign tab
2. Enter campaign message in Messaging tab
3. In Generate tab, check "Generate Localizations"
4. AI creates one ad per language (English, Spanish, French, Chinese, etc.)
5. Files saved with language codes: `_en`, `_es`, `_fr`, `_zh-CN`

**Example Output**:
- `ad_1_1_en_20251026_120000.png`
- `ad_1_1_es_20251026_120000.png`
- `ad_1_1_fr_20251026_120000.png`
- `ad_1_1_zh-CN_20251026_120000.png`

### Multi-Product Generation

See [MULTI_PRODUCT_GUIDE.md](MULTI_PRODUCT_GUIDE.md) for detailed instructions on:
- Separate vs Combined modes
- Use cases for each mode
- Output structure
- Best practices

### Campaign Configuration

See [CAMPAIGN_CONFIG_GUIDE.md](CAMPAIGN_CONFIG_GUIDE.md) for detailed information on:
- Available regions and their characteristics
- Target audiences and demographics
- Cultural context and messaging guidance
- Adding custom regions/audiences

---

## Troubleshooting

### Common Issues

**"Please configure your API key in Settings tab first"**
- Go to Settings tab
- Enter valid Google Gemini API key
- Click "Save API Key"

**"No existing product photos found"**
- Ensure selected products have photos in `products/{slug}/photos/product/`
- At least one reference photo required

**"Please select at least one environment/product"**
- Use click-to-select in Environments/Products tabs
- Selected images show in "Selected" galleries

**Generation takes too long**
- Generating localized ads creates multiple images (1 per language)
- Example: 3 formats × 4 languages = 12 images
- Consider disabling localization for faster generation

**Aspect ratios incorrect**
- Ensure using latest version with API aspect ratio enforcement
- Previous versions relied on prompt alone (less reliable)

---

## Development

### Running Tests
```bash
uv run python test_app.py
```

### Adding New Products

1. Create product folder: `products/{product-slug}/`
2. Add `config.yaml`:
```yaml
product:
  name: "Product Name"
  description: "Product description"
  category: "Category"
company:
  name: "Company Name"
  tagline: "Company tagline"
```
3. Add reference photos to `products/{product-slug}/photos/product/`
4. Add logos to `products/{product-slug}/photos/logo/`

### Adding New Regions

Edit `config/regions.yaml`:
```yaml
new_region:
  name: "Region Name"
  description: "Brief description"
  countries: ["Country1", "Country2"]
  cultural_context:
    - "Context point"
  visual_preferences:
    colors: ["Color palette"]
    imagery: ["Image style"]
  messaging:
    tone: ["Tone"]
    themes: ["Themes"]
  top_languages:
    - code: "en"
      name: "English"
```

---

## Roadmap

### Completed ✅
- [x] Campaign configuration (regions/audiences)
- [x] Interactive world map
- [x] Multi-product selection
- [x] Environment generation
- [x] Product view generation (6 angles)
- [x] Multi-aspect ratio ads (1:1, 9:16, 16:9)
- [x] Logo integration
- [x] Localization support
- [x] Campaign preview & JSON export
- [x] Enhanced product integration prompts

### Planned 🚀
- [ ] Scene generation with target region/audience context
- [ ] Advanced text overlay controls
- [ ] Logo positioning controls
- [ ] Batch generation across product/environment matrices
- [ ] A/B testing variant generation
- [ ] Campaign performance tracking
- [ ] Video/animation support
- [ ] Custom brand style guides

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- Google Gemini 2.5 Flash Image ("Nano Banana") for AI image generation
- Gradio for the excellent web interface framework
- uv for blazing-fast Python package management

---

## Support

For issues, questions, or feature requests:
- Open an issue on GitHub
- Check the [DEVELOPMENT_LOG.md](DEVELOPMENT_LOG.md) for detailed technical notes
- Review guides: [MULTI_PRODUCT_GUIDE.md](MULTI_PRODUCT_GUIDE.md), [CAMPAIGN_CONFIG_GUIDE.md](CAMPAIGN_CONFIG_GUIDE.md)

---

## Citation

If you use this project in your research or work, please cite:

```
Creative Automation Pipeline
AI-Powered Social Ad Campaign Generation
https://github.com/mitchaiet/creative-pipeline-automation
```
