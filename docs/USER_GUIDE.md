# User Guide

Complete step-by-step instructions for using the Creative Automation Pipeline.

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Configure Campaign](#1-configure-campaign-campaign-tab)
3. [Create Messaging](#2-create-messaging-messaging-tab)
4. [Generate Environments](#3-generate-environments-environments-tab)
5. [Manage Products](#4-manage-products-products-tab)
6. [Manage Logos](#5-manage-logos-logos-tab)
7. [Preview Campaign](#6-preview-campaign-preview-tab)
8. [Generate Ads](#7-generate-ads-generate-tab)
9. [Configure Settings](#8-configure-settings-settings-tab)

---

## Getting Started

### First Time Setup

1. **Configure API Key** (required):
   - Go to **Settings** tab
   - Enter your Google Gemini API key
   - Click **Save API Key**
   - Verify status shows 

2. **Understand the Workflow**:
   - The interface uses a 7-tab progressive workflow
   - Each tab builds on the previous one
   - Use **Next** and **Previous** buttons to navigate
   - All selections are saved as you go

---

## 1. Configure Campaign (Campaign Tab)

Set up your target region and audience for the campaign.

### Select Target Region

You have three ways to select a region:

**Option A: Use the Interactive Map**
- Click directly on any country
- The region will be automatically selected
- Countries highlight on hover

**Option B: Use the Dropdown**
- Click the **Target Region** dropdown
- Select from 6 available regions

**Available Regions:**
- North America
- Europe
- Asia Pacific
- Latin America
- Middle East & Africa
- Oceania

### Select Target Audience

1. Click the **Target Audience** dropdown
2. Choose from 8 audience segments:
   - Health-Conscious Millennials
   - Busy Parents
   - Gen Z Trendsetters
   - Active Seniors
   - Fitness Enthusiasts
   - Eco-Conscious Consumers
   - Young Professionals
   - Budget-Conscious Shoppers

### Review Campaign Summary

After selecting region and audience, you'll see:
- **Region Details**: Countries covered, cultural context
- **Audience Profile**: Demographics, messaging preferences
- **Visual Preferences**: Recommended colors and imagery styles
- **Messaging Tone**: Suggested communication approach

### Next Steps

Click **Next** to proceed to the Messaging tab.

---

## 2. Create Messaging (Messaging Tab)

Create your campaign message and optionally translate it to regional languages.

### Enter Campaign Message

1. Type your message in the **Campaign Message** text box
2. Watch the character counter update
3. Keep it concise and impactful

**Tips:**
- Aim for 50-100 characters for social ads
- Focus on one key benefit or call-to-action
- Use the randomize button for inspiration

### Use Sample Messages (Optional)

1. Click **Randomize Message** to see preset examples
2. Keep clicking for more options
3. Edit the generated message to fit your needs

**Sample categories include:**
- Health & wellness
- Technology & innovation
- Lifestyle & comfort
- Sustainability & eco-friendly

### Translate Message (Optional)

1. Click **Translate Message**
2. View translations in the top 4 languages for your region
3. Translations appear below the button

**Example for North America:**
- English
- Spanish
- French
- Chinese (Simplified)

### Next Steps

Click **Next** to proceed to the Environments tab.

---

## 3. Generate Environments (Environments Tab)

Create AI-generated background environments for your ads.

### Enter Environment Prompt

**Option A: Write Your Own**
1. Describe the scene you want (e.g., "Modern minimalist kitchen with natural light")
2. Be specific about style, lighting, and atmosphere

**Option B: Use Preset Prompts**
1. Click **Randomize Environment Prompt**
2. Browse 20+ preset options
3. Click multiple times to see different scenes

**Preset categories:**
- Interior spaces (kitchens, living rooms, bedrooms)
- Commercial settings (cafes, gyms, offices)
- Outdoor scenes (parks, beaches, mountains)
- Lifestyle contexts (home offices, urban settings)

### Generate Backgrounds

1. Click **Generate Environments**
2. Wait for generation (about 30-60 seconds)
3. 4 variations will appear in the gallery

**What you get:**
- 4 unique variations of your prompt
- 1:1 square aspect ratio
- Professional studio quality
- Pure white background option

### Select Environments

1. **Click images** in the gallery to select them
2. Selected images move to **Selected Environments** gallery
3. Select as many as you want (1-4 recommended)

**Tips:**
- Select multiple for variety in final ads
- Choose environments that match your product context
- Consider your target audience's lifestyle

### Next Steps

Click **Next** to proceed to the Products tab.

---

## 4. Manage Products (Products Tab)

Select products and optionally generate new product views.

### Select Products

1. Click the **Select Products** dropdown
2. Multi-select products by clicking them
3. Click again to deselect

**Available Products:**
- eco-cleaner
- gourmet-coffee
- herbal-tea
- noise-cancelling-headphones
- protein-bar
- running-shoes
- smart-watch
- sparkling-water
- travel-backpack
- yoga-mat

### Preview Product Assets

After selecting products, you'll see:
- **Product Photos**: All photos from selected products
- **Logo Assets**: Company logos from selected products

### Generate Product Views (Optional)

If you want new AI-generated product photography:

#### Choose Generation Mode

**Separate Mode** (default):
- Generates 6 individual views for each product
- Products photographed independently
- Best for: Product catalogs, e-commerce listings

**Combined Mode**:
- Generates 6 views with all products together
- Products arranged in compositions
- Best for: Product bundles, gift sets, campaign visuals

#### Generate the Views

1. Select your desired mode
2. Click **Generate All Product Views**
3. Wait for generation (varies by product count)

**What you get:**
- 6 camera angles: front, back, left, right, top-down, bottom-up
- Maintains product appearance from reference photos
- Professional lighting and white background
- Saved to campaign folder

### Select Product Images

1. **Click images** in the product gallery to select them
2. Selected images move to **Selected Products** gallery
3. You can select from:
   - Existing product photos
   - Newly generated views
   - Mix of both

**Tips:**
- Choose the best angles for your campaign
- Select 1-2 images per product
- Consider which angle best shows the product benefit

### Next Steps

Click **Next** to proceed to the Logos tab.

---

## 5. Manage Logos (Logos Tab)

Review and select brand logos for ad placement.

### Auto-Populated Logos

Logos automatically load from your selected products:
- Each product's company logo appears in the gallery
- Logos sourced from `products/{slug}/photos/logo/`

### Select Logos

1. **Click logos** in the gallery to select them
2. Selected logos move to **Selected Logos** gallery
3. These logos will be available for ad generation

**When to use logos:**
- Strengthen brand identity
- Professional corporate campaigns
- Multi-brand campaigns

**When to skip logos:**
- Product-focused campaigns
- Minimalist aesthetic
- When product already shows branding

### Next Steps

Click **Next** to proceed to the Preview tab.

---

## 6. Preview Campaign (Preview Tab)

Review your complete campaign setup before generating ads.

### Campaign Summary

View all settings at a glance:
- **Campaign Configuration**: Region and audience
- **Campaign Message**: Your message and translations
- **Environments**: Selected backgrounds (with count)
- **Products**: Selected product images (with count)
- **Logos**: Selected brand assets (with count)

### Preview Galleries

Visual previews of all selected assets:
- Environment thumbnails
- Product image thumbnails
- Logo thumbnails

### Refresh Preview

If you made changes in other tabs:
1. Click **Refresh Preview**
2. All counts and previews update

### Load Campaign from JSON

To load a previously saved campaign:
1. Use the **Load Campaign JSON** file picker
2. Select a `campaign_config.json` file
3. The system will:
   - Automatically populate all fields
   - Switch to Preview tab
   - Refresh all previews

**JSON files are located at:**
`outputs/{CAMPAIGN_ID}/campaign_config.json`

### Next Steps

Click **Next** to proceed to the Generate tab.

---

## 7. Generate Ads (Generate Tab)

Create final ad creatives in multiple aspect ratios and languages.

### Before Generating

**Required:**
- At least one selected environment
- At least one selected product

**Optional but recommended:**
- Campaign message entered
- Logos selected (if desired)

### Configure Generation Options

#### Include Logo
- **Checked**: Adds selected logo to each ad format
- **Unchecked**: Ads show only product + environment + message

**Logo placement:**
- Subtle corner positioning
- Professional sizing
- Doesn't overwhelm the composition

#### Generate Localizations
- **Checked**: Creates one ad per language in regional top 4
- **Unchecked**: Creates only English ads

**Example with localizations:**
- North America region = 4 languages
- 3 aspect ratios
- Total: 12 images (3 × 4)

**Without localizations:**
- 3 aspect ratios
- Total: 3 images

### Generate Ads

1. Configure your options
2. Click **Generate All Ad Formats**
3. Wait for generation (varies by options)

**Generation time:**
- Without localizations: ~1-2 minutes
- With localizations: ~3-5 minutes

### Review Output

Generated ads appear in the gallery below, organized by:
- Aspect ratio (1:1, 9:16, 16:9)
- Language (if localizations enabled)

**File naming:**
- Non-localized: `ad_1_1_{timestamp}.png`
- Localized: `ad_1_1_es_{timestamp}.png` (Spanish example)

### Output Structure

All ads saved to your campaign folder:

```
outputs/{CAMPAIGN_ID}/
  ads/
    1_1/          # Square ads (Instagram feed)
    9_16/         # Vertical ads (Stories, Reels)
    16_9/         # Landscape ads (YouTube)
```

### Next Steps

All generated files are saved to `outputs/{CAMPAIGN_ID}/` folder for easy access.

---

## 8. Configure Settings (Settings Tab)

Manage API keys and application settings.

### API Key Configuration

#### First Time Setup

1. Go to [Google AI Studio](https://ai.google.dev/)
2. Sign in with your Google account
3. Click "Get API Key"
4. Create a new API key
5. Copy the key

#### Add Key to Application

**Option A: Settings Tab**
1. Paste key in **Google Gemini API Key** field
2. Click **Save API Key**
3. Key saved to `.env` file
4. Status shows  API Key configured

**Option B: Environment File**
1. Edit `.env` file in project root
2. Set `GOOGLE_API_KEY=your_key_here`
3. Restart application
4. Status shows  API Key configured

### API Key Status

** API Key configured**
- Key is valid and ready to use
- All generation features available

** API Key not configured**
- Need to add key before generating
- Settings tab will show warning
- Generation buttons disabled

### Environment Variables

The application uses:
- `GOOGLE_API_KEY` - Required for image generation
- `PORT` - Optional, defaults to 7860

---

## Tips & Best Practices

### Campaign Creation

1. **Start with clear goals**: Know your target audience before configuring
2. **Use cultural context**: Review region-specific recommendations
3. **Test multiple messages**: Try the randomize feature for ideas
4. **Generate variety**: Create 4 environments for different contexts

### Asset Selection

1. **Quality over quantity**: Select your best 1-2 products per campaign
2. **Match context**: Choose environments that fit product use case
3. **Consider composition**: Select products with complementary colors
4. **Think mobile-first**: Vertical (9:16) is critical for social

### Generation

1. **Start without localizations**: Test your campaign in English first
2. **Use logos selectively**: Not every ad needs a logo
3. **Batch similar campaigns**: Generate multiple products with same environment
4. **Save configurations**: Export JSON for successful campaign templates

### Troubleshooting

**"Please configure your API key first"**
- Go to Settings tab and add your Gemini API key

**"Please select at least one environment"**
- Go to Environments tab and click images to select

**"No existing product photos found"**
- Selected product needs photos in `products/{slug}/photos/product/`

**Generation is slow**
- Localizations multiply generation time
- Multiple products in Separate mode takes longer
- This is normal - AI generation takes time

**Wrong aspect ratio**
- Ensure using latest version
- API enforces aspect ratios correctly

---

## Keyboard Shortcuts

- **Tab**: Navigate between fields
- **Enter**: Submit in text fields
- **Click**: Select/deselect images in galleries
- **Scroll**: Browse long galleries

---

## Next Steps

- Review [FEATURES.md](FEATURES.md) for complete feature details
- Check [MULTI_PRODUCT_GUIDE.md](MULTI_PRODUCT_GUIDE.md) for advanced product workflows
- See [CAMPAIGN_CONFIG_GUIDE.md](CAMPAIGN_CONFIG_GUIDE.md) for region/audience details
- Read [DEVELOPMENT.md](DEVELOPMENT.md) to extend the system
