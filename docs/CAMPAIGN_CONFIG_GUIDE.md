# Campaign Configuration Guide

This guide explains the available target regions/markets and target audiences for campaign configuration.

## Target Regions/Markets

### 1. North America
- **Coverage**: United States and Canada
- **Key Traits**: Direct messaging, innovation-focused, health & wellness trends
- **Visual Style**: Bold colors, modern minimalist design, authentic imagery

### 2. Europe
- **Coverage**: Western and Central Europe
- **Key Traits**: Heritage-focused, environmental consciousness, quality over quantity
- **Visual Style**: Muted natural palettes, classic design, lifestyle-rich imagery

### 3. Asia Pacific
- **Coverage**: East and Southeast Asia, Australia, New Zealand
- **Key Traits**: Tradition meets innovation, community-oriented, tech-savvy
- **Visual Style**: Vibrant cultural colors, clean compositions, group settings

### 4. Latin America
- **Coverage**: Mexico, Central and South America
- **Key Traits**: Family-centered, vibrant lifestyle, celebration culture
- **Visual Style**: Bold saturated colors, festive imagery, family scenes

### 5. Middle East & Africa
- **Coverage**: Middle East and North Africa, Sub-Saharan Africa
- **Key Traits**: Tradition and modernity, luxury positioning, hospitality
- **Visual Style**: Rich luxurious aesthetics, gold and jewel tones, premium presentation

### 6. Oceania
- **Coverage**: Australia, New Zealand, Pacific Islands
- **Key Traits**: Outdoor active lifestyle, laid-back approach, environmental awareness
- **Visual Style**: Natural sun-drenched imagery, coastal settings, authentic style

## Target Audiences

### 1. Health-Conscious Millennials (25-40)
- **Profile**: Urban professionals prioritizing wellness and self-care
- **Messaging**: Health benefits, clean ingredients, sustainability
- **Context**: Fitness studios, meal prep, outdoor activities, trendy cafes

### 2. Busy Parents & Families (30-50)
- **Profile**: Time-pressed parents managing family needs
- **Messaging**: Time-saving, family-friendly, trust and reliability
- **Context**: Kitchen settings, family activities, school lunch prep

### 3. Gen Z Trendsetters (18-27)
- **Profile**: Digital natives, socially conscious, experience-seekers
- **Messaging**: Bold visuals, social causes, authenticity, humor
- **Context**: College campuses, concerts, coffee shops, urban streets

### 4. Active Seniors & Retirees (60+)
- **Profile**: Health-focused retirees seeking quality of life
- **Messaging**: Clear communication, health and vitality, proven benefits
- **Context**: Walking trails, home gardens, community centers, travel

### 5. Fitness Enthusiasts & Athletes (20-45)
- **Profile**: Goal-oriented individuals focused on performance
- **Messaging**: Performance benefits, specific metrics, intense imagery
- **Context**: Gyms, outdoor workouts, post-workout recovery, competitions

### 6. Eco-Conscious & Sustainable Living (25-55)
- **Profile**: Environmentally aware consumers prioritizing sustainability
- **Messaging**: Sustainability credentials, environmental impact, natural aesthetics
- **Context**: Farmers markets, natural outdoor settings, sustainable homes

### 7. Young Professionals & Urban Dwellers (22-35)
- **Profile**: Career-focused individuals in metropolitan areas
- **Messaging**: Convenience, premium quality, time-saving, sleek aesthetics
- **Context**: Offices, coffee shops, urban apartments, rooftop bars

### 8. Budget-Conscious Value Seekers (25-60)
- **Profile**: Cost-conscious consumers seeking best value
- **Messaging**: Value and affordability, practical benefits, clear communication
- **Context**: Home kitchens, grocery shopping, family meals, everyday settings

## Using Campaign Configuration

### Method 1: Create New Campaign (Manual Configuration)

1. Navigate to the **Campaign** tab
2. View the **Interactive World Map**
   - Visual representation of all 6 regions mapped to 100+ countries
   - Regions are color-coded (light gray for unselected, dark blue for selected)
   - Hover over countries to see which region they belong to
3. **Select a Target Region** using one of three methods:
   - **Quick Select Buttons**: Click emoji-labeled region buttons (🌎 North America, 🇪🇺 Europe, etc.)
   - **Dropdown**: Select from the Target Region/Market dropdown
   - Both methods automatically update the map, dropdown, and region details
4. View **Region Details**:
   - Region name and description
   - Cultural context highlights
   - Visual preferences
   - Seasonal considerations
5. Select a **Target Audience** from the dropdown
   - View detailed demographics, psychographics, and messaging preferences
6. Review the **Enhanced Campaign Summary** showing:
   - Full region information (name, description, cultural context, visual preferences)
   - Complete audience profile (name, age range, messaging preferences)
   - Formatted in easy-to-read markdown
7. **Proceed to Messaging Tab** to enter campaign message and generate translations
8. **Proceed to Environments Tab** to generate background scenes
9. **Proceed to Products Tab** to generate product views
10. **Preview Tab** to review all assets
11. **Generate Tab** to create final ads

### Method 2: Load from JSON (Automated Workflow)

Load a previously saved campaign configuration for instant regeneration:

1. Navigate to the **Campaign** tab
2. Click **"Load Campaign JSON"** and select a `campaign_config.json` file
3. **Automatic workflow triggers:**
   - Campaign configuration populates all UI fields
   - Translations automatically generated for target region languages
   - 4 environment backgrounds automatically created
   - Product views automatically generated (6 per product)
   - Preview tab opens with all generated assets

**Campaign Configuration Format:**

All campaigns are organized by timestamp-based IDs (format: `YYYYMMDD_HHMMSS`) in `outputs/`:

```
outputs/20251103_153045/
├── campaign_config.json          # Complete campaign configuration
├── environments/                 # 4 AI-generated background scenes
│   ├── env_001.png
│   ├── env_002.png
│   ├── env_003.png
│   └── env_004.png
├── products/                     # 6 views per product
│   ├── eco-cleaner_front.png
│   ├── eco-cleaner_back.png
│   ├── eco-cleaner_left.png
│   ├── eco-cleaner_right.png
│   ├── eco-cleaner_top-down.png
│   └── eco-cleaner_bottom-up.png
└── ads/                          # Final ad creatives
    ├── 1_1/                      # Square (1080×1080)
    ├── 9_16/                     # Vertical (1080×1920)
    └── 16_9/                     # Landscape (1920×1080)
```

**JSON Structure:**

The `campaign_config.json` file contains all campaign settings and uses project-relative paths for portability:

```json
{
  "campaign": {
    "id": "20251103_153045",
    "created_at": "2025-11-03T15:30:45.123456"
  },
  "targeting": {
    "region": "north_america",
    "audience": "health_conscious"
  },
  "messaging": {
    "primary_message": "Transform your wellness routine",
    "translations": {
      "en": "Transform your wellness routine",
      "es": "Transforma tu rutina de bienestar",
      "fr": "Transformez votre routine bien-être"
    }
  },
  "generation_config": {
    "environment_prompt": "Modern minimalist kitchen...",
    "product_slugs": ["eco-cleaner"],
    "product_mode": "separate",
    "logo_paths": ["products/eco-cleaner/photos/logo/logo.png"]
  },
  "ad_settings": {
    "aspect_ratios": ["1:1", "9:16", "16:9"],
    "localization": {
      "1:1": true,
      "9:16": true,
      "16:9": false
    },
    "include_logo": {
      "1:1": true,
      "9:16": true,
      "16:9": false
    }
  }
}
```

**Expected Generation Times:**
- **Translations:** 2-5 seconds (4 languages)
- **Environments:** 30-60 seconds (4 images)
- **Products:** 60-120 seconds (6 views per product)
- **Total:** 2-3 minutes for typical campaign

### For Future Scene Generation (Step 2)

The selected region and audience will be used to:
- Generate scene variations that resonate with the target market
- Apply appropriate cultural context and visual styling
- Use relevant settings and scenarios from the audience's lifestyle
- Adapt messaging tone and style to audience preferences

### Customization

To add or modify regions/audiences:
- Edit `config/regions.yaml` for new markets
- Edit `config/audiences.yaml` for new audience segments
- Follow the existing schema structure
- Restart the application to load changes
