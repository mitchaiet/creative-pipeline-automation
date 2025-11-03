# Features

Complete overview of Creative Automation Pipeline capabilities.

---

##  Campaign Configuration

### Interactive World Map
- Visual representation mapping 6 regions to 100+ countries
- Click regions directly on the map
- Country coverage displayed with hover tooltips

### 6 Target Regions
- **North America**: USA, Canada, Mexico
- **Europe**: UK, France, Germany, Italy, Spain, and more
- **Asia Pacific**: China, Japan, India, Australia, Southeast Asia
- **Latin America**: Brazil, Argentina, Colombia, and more
- **Middle East & Africa**: UAE, Saudi Arabia, South Africa, and more
- **Oceania**: Australia, New Zealand, Pacific Islands

### 8 Target Audiences
- **Health-Conscious Millennials**: Wellness-focused, ages 25-40
- **Busy Parents**: Time-pressed families with children
- **Gen Z Trendsetters**: Digital natives, ages 18-25
- **Active Seniors**: Healthy retirees, ages 60+
- **Fitness Enthusiasts**: Athletic, performance-driven
- **Eco-Conscious Consumers**: Sustainability-focused
- **Young Professionals**: Career-driven, ages 25-35
- **Budget-Conscious Shoppers**: Value-seeking consumers

### Cultural Context
Each region includes:
- Visual preferences (colors, imagery styles)
- Messaging tone recommendations
- Cultural considerations
- Top 4 regional languages

---

##  Messaging & Translation

### Campaign Message Editor
- Real-time character counter
- Multi-line text support
- Message persistence across tabs

### Google Translate Integration
- Automatic translation to regional languages
- Top 4 languages per selected region
- Examples:
  - **North America**: English, Spanish, French, Chinese
  - **Europe**: English, German, French, Spanish
  - **Asia Pacific**: Chinese, Hindi, Japanese, Korean

### Sample Messages
- 20 curated campaign message templates
- Randomize button for inspiration
- Industry-specific examples (health, tech, lifestyle)

---

##  Environment Generation

### AI-Powered Background Creation
- Generate 4 variations per prompt
- Square 1:1 aspect ratio optimized for product compositing
- Professional studio-quality environments

### Preset Environment Prompts
20 ready-to-use scene templates:
- **Interior Spaces**: Modern kitchen, cozy living room, minimalist bedroom
- **Commercial Settings**: Trendy cafe, fitness gym, yoga studio
- **Outdoor Scenes**: Sunlit park, mountain landscape, beach sunset
- **Lifestyle Contexts**: Office desk, home office, urban rooftop

### Interactive Selection
- Click-to-select gallery interface
- Selected images move to dedicated preview
- Multi-select support for variety

### Output
- Saved to campaign folder: `outputs/{CAMPAIGN_ID}/environments/`
- Files: `environment_1_{timestamp}.png` through `environment_4_{timestamp}.png`

---

##  Product Management

### Multi-Product Selection
- Dropdown with all available products
- Multi-select capability
- Live preview of product photos and logos

### Two Generation Modes

#### Separate Mode (Default)
**What it does:**
- Generates individual 6-view sets for each selected product
- Each product photographed independently

**Output:**
- Saved to `outputs/{CAMPAIGN_ID}/products/{product-slug}/`
- 6 views per product: front, back, left, right, top-down, bottom-up

**Best for:**
- Individual product catalogs
- E-commerce product pages
- SKU-specific imagery

#### Combined Mode
**What it does:**
- Generates 6 views showing ALL products together
- Products arranged aesthetically in single compositions

**Output:**
- Saved to `outputs/{CAMPAIGN_ID}/products/combined/`
- 6 views total (all products in each image)

**Best for:**
- Product bundles and gift sets
- Cross-sell imagery
- Campaign visuals with multiple products

### 6 Product Views

1. **Front View**: Straight-on, camera facing front at eye level
2. **Back View**: 180° opposite, shows rear/ingredients
3. **Left Side View**: 90° left profile, shows depth
4. **Right Side View**: 90° right profile
5. **Top-Down View**: Directly overhead perspective
6. **Bottom-Up View**: From below, shows base

### AI Consistency
- Maintains exact appearance from reference photos
- Preserves colors, branding, and labels
- Realistic 3D representation across angles

---

##  Logo Integration

### Asset Management
- Dedicated logo library per product
- Auto-population from selected products
- Preview gallery with selection interface

### Ad Placement
- Optional logo inclusion in generated ads
- Subtle corner placement
- Professional sizing that doesn't overwhelm
- Maintains brand identity without distraction

---

##  Campaign Preview

### Complete Overview
View all campaign settings in one place:
- Campaign configuration (region, audience)
- Campaign message and translations
- Selected environments (with count)
- Selected products (with count)
- Selected logos (with count)

### JSON Export
- Save complete campaign configuration
- Includes all settings and selections
- Saved to `outputs/{CAMPAIGN_ID}/campaign_config.json`

### Auto-Load & Preview
- Loading campaign JSON automatically populates fields
- Auto-switches to Preview tab
- Instantly refreshes all previews

---

##  Ad Generation

### Three Aspect Ratios

#### 1:1 Square (1080x1080)
- Instagram feed posts
- Facebook posts
- Twitter/X image posts

#### 9:16 Vertical (1080x1920)
- Instagram Stories
- TikTok
- Facebook/Instagram Reels
- Snapchat

#### 16:9 Landscape (1920x1080)
- YouTube thumbnails
- Desktop display ads
- LinkedIn posts
- Facebook cover images

### AI-Powered Synthesis

Each generated ad includes:
- **Product as Hero**: 40-60% of frame, prominently featured
- **Perfect Perspective**: Product angle matches environment
- **Environment Integration**: Realistic shadows, lighting, reflections
- **Professional Typography**: Campaign message with optimal readability
- **Logo Placement** (optional): Subtle brand identity

### Localization Support

Generate ads in multiple languages automatically:
- One-click generation for all regional languages
- Separate files per language with language codes
- Example output:
  - `ad_1_1_en_{timestamp}.png` (English)
  - `ad_1_1_es_{timestamp}.png` (Spanish)
  - `ad_1_1_fr_{timestamp}.png` (French)
  - `ad_1_1_zh-CN_{timestamp}.png` (Chinese)

### Gallery View
- All variations displayed together
- Organized by aspect ratio
- Localized versions clearly labeled

### Output Structure
```
outputs/{CAMPAIGN_ID}/
  ads/
    1_1/
      ad_1_1_en_{timestamp}.png
      ad_1_1_es_{timestamp}.png
    9_16/
      ad_9_16_en_{timestamp}.png
      ad_9_16_es_{timestamp}.png
    16_9/
      ad_16_9_en_{timestamp}.png
      ad_16_9_es_{timestamp}.png
```

---

##  Workflow Navigation

### Tab-Based Interface
Progressive workflow across 7 tabs:
1. **Campaign** - Configure region and audience
2. **Messaging** - Create and translate campaign message
3. **Environments** - Generate and select backgrounds
4. **Products** - Select and generate product views
5. **Logos** - Review and select brand assets
6. **Preview** - Review complete campaign setup
7. **Generate** - Create final ad creatives

### Navigation Buttons
- **Next** button on each tab
- **Previous** button to go back
- Guided process from setup to generation

### State Persistence
- All selections saved across tabs
- Campaign ID maintained throughout session
- Easy to iterate and refine

---

##  Settings

### API Key Management
- Configure Google Gemini API key
- Persistent storage in `.env` file
- Status indicator ( configured,  missing)
- Secure key handling

### Environment Variables
- `GOOGLE_API_KEY` - Gemini API authentication
- Can be set via Settings tab or `.env` file
- Environment variable takes precedence

---

##  Advanced Capabilities

### Multi-Modal AI Input
- Text prompts for precise instructions
- Reference images for visual consistency
- Combined input for optimal results

### Aspect Ratio Enforcement
- API-level aspect ratio control (not just prompt-based)
- Guaranteed correct dimensions
- No cropping or stretching artifacts

### Batch Processing
- Generate multiple products simultaneously (Separate mode)
- Multiple aspect ratios in one generation
- Multiple languages automatically

### Self-Contained Campaigns
- All assets for a campaign in single folder
- `outputs/{CAMPAIGN_ID}/` structure
- Easy to share, archive, or deploy

### Image Quality
- High resolution (1080p minimum)
- Professional studio lighting
- Sharp focus, photorealistic rendering
- Pure white backgrounds (#FFFFFF) for easy compositing
