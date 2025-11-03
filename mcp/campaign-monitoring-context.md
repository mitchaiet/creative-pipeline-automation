# Campaign Monitoring Agent - Model Context Protocol

Note: This is a non-functional design document synthesized from the functionality of the codebase and represents the various information that will be needed to draft LLM alerts and responses based on the social/advertising creative workflow.


## Purpose

This document defines the information structure that an AI agent needs to monitor creative campaigns, track asset generation, and identify issues requiring human attention.

---

## Core Monitoring Capabilities

The AI monitoring agent is designed to perform the following key functions:

### 1. Monitor Incoming Campaign Briefs
- **What to check:** Campaign configuration completeness (region, audience, message)
- **Data source:** `campaign_config.json` → `campaign`, `targeting`, `messaging` sections
- **Validation:** Ensure all required fields are present and valid
- **Alert on:** Missing region, missing audience, empty message, invalid campaign ID format

### 2. Trigger Automated Generation Tasks
- **What to monitor:** Workflow progression through all generation phases
- **Phases to track:**
  1. Translation generation (2-5 seconds)
  2. Environment generation (30-60 seconds, 4 images)
  3. Product generation (60-120 seconds per product, 6 views each)
  4. Ad composition (30-60 seconds per aspect ratio)
- **Alert on:** Phase timeout (>10 minutes total), stuck phases, generation errors

### 3. Track Count and Diversity of Creative Variants
- **Asset counts to monitor:**
  - **Environments:** Minimum 1, recommended 3+ for variety
  - **Products:** Expected 6 views per product (front, back, left, right, top-down, bottom-up)
  - **Ads:** Calculate expected count based on aspect ratios × localizations
    ```
    Expected ads = Σ(aspect_ratios) × (languages if localization enabled, else 1)
    Example: 3 ratios × 4 languages = 12 ad variants
    ```
- **Alert on:**
  - Fewer than 3 environment variants (insufficient diversity)
  - Fewer than 3 ad variants per aspect ratio (insufficient for A/B testing)
  - Missing product views (incomplete generation)

### 4. Flag Missing or Insufficient Assets
- **Critical thresholds:**
  - Environments: Alert if < 1, warn if < 3
  - Products: Alert if any product has < 6 views
  - Ads: Alert if total variants < expected count
- **Quality checks:**
  - File existence validation
  - File size > 0 bytes (detect failed generations)
  - Image dimensions match expected (1080×1080, 1080×1920, 1920×1080)

### 5. Alert and Logging Mechanism
- **Alert severity levels:**
  - **❌ CRITICAL:** Blocks campaign launch (no assets, missing required data, generation failure)
  - **⚠️ WARNING:** Doesn't block but needs review (low variant count, long generation time)
  - **ℹ️ INFO:** Status updates (generation complete, assets refreshed)
- **Human-readable alert format:**
  ```
  Campaign {campaign_id} for {region} {audience} audience:
  Status: {generation_complete/failed/in_progress}

  Assets Generated:
  - Environments: {count} (recommended: 3+)
  - Products: {count} views across {n} products
  - Ads: {count} variants across {n} aspect ratios

  Alerts:
  - [CRITICAL/WARNING/INFO] {specific issue description}

  Action Required: {specific recommendation}
  ```

---

## System Overview
The Creative Automation Pipeline uses an automated workflow that triggers sequential generation when a campaign JSON is loaded:

1. **JSON Load** → Campaign configuration populates UI
2. **Auto-Translate** → Message translated to regional languages
3. **Auto-Generate Environments** → 4 background scenes created
4. **Auto-Generate Products** → 6 views per product synthesized
5. **Preview** → All assets displayed for review
6. **Generate Ads** → Final ads created in 3 aspect ratios

All campaigns use timestamp-based IDs (format: `YYYYMMDD_HHMMSS`) for chronological organization.

---

## Campaign Context Structure

### 1. Campaign Brief

The core campaign configuration that defines targeting and messaging:

```json
{
  "campaign": {
    "name": "Campaign 20251103_150000",
    "id": "20251103_150000",
    "created_at": "2025-11-03T15:00:00.123456",
    "source": "manual",
    "type": "manual_generation",
    "status": "in_progress"
  },
  "targeting": {
    "region": "north_america",
    "audience": "health_conscious"
  },
  "messaging": {
    "primary_message": "Transform your wellness routine with natural ingredients",
    "translations": {
      "en": "Transform your wellness routine with natural ingredients",
      "es": "Transforma tu rutina de bienestar con ingredientes naturales",
      "fr": "Transformez votre routine bien-être avec des ingrédients naturels",
      "zh-CN": "用天然成分改变您的健康习惯"
    }
  }
}
```

**Agent Monitoring Considerations:**
- Is the campaign brief complete? (Has region, audience, message)
- Are translations available for all required languages?
- Does the message align with the target audience profile?
- **Campaign ID Format:** Must be `YYYYMMDD_HHMMSS` for proper organization

---

### 2. Generation Configuration

Technical specifications for asset generation:

```json
{
  "generation_config": {
    "environment_prompt": "Modern minimalist kitchen with marble countertops and natural sunlight streaming through large windows",
    "product_slugs": ["eco-cleaner", "yoga-mat"],
    "product_mode": "combined",
    "logo_paths": [
      "products/eco-cleaner/photos/logo/greenclean-logo.png",
      "products/yoga-mat/photos/logo/zenflow-logo.png"
    ]
  }
}
```

**Agent Monitoring Considerations:**
- Are all product slugs valid? (Check against available products in `products/` directory)
- Do all logo paths exist and are accessible?
- Is the environment prompt descriptive enough? (Min 10 words recommended)
- Product mode: "separate" generates individual views, "combined" generates products together

---

### 3. Ad Settings & Format Requirements

Specifies which aspect ratios and features are enabled:

```json
{
  "ad_settings": {
    "aspect_ratios": ["1:1", "9:16", "16:9"],
    "localization": {
      "enabled": true,
      "per_format": {
        "1:1": true,
        "9:16": true,
        "16:9": false
      }
    },
    "include_logo": {
      "1:1": true,
      "9:16": true,
      "16:9": false
    }
  }
}
```

**Agent Monitoring Considerations:**
- **Expected Variant Count Calculation:**
  ```
  For each aspect ratio:
    if localization enabled: variants = number_of_translations
    else: variants = 1

  Total variants = sum of all aspect ratio variants
  ```
- **Minimum Recommended:** 3 variants per aspect ratio for A/B testing
- **Logo Requirements:** If `include_logo` is true, verify logo paths exist

---

### 4. Asset Inventory

Track generated and available assets:

```json
{
  "assets": {
    "environments": {
      "generated_count": 4,
      "paths": [
        "outputs/20251103_150000/environments/env_001.png",
        "outputs/20251103_150000/environments/env_002.png",
        "outputs/20251103_150000/environments/env_003.png",
        "outputs/20251103_150000/environments/env_004.png"
      ],
      "minimum_required": 1,
      "recommended": 3
    },
    "products": {
      "generated_count": 12,
      "views_per_product": {
        "eco-cleaner": ["front", "back", "left", "right", "top-down", "bottom-up"],
        "yoga-mat": ["front", "back", "left", "right", "top-down", "bottom-up"]
      },
      "paths": [
        "outputs/20251103_150000/products/eco-cleaner_front.png",
        "outputs/20251103_150000/products/eco-cleaner_back.png",
        "..."
      ],
      "expected_views_per_product": 6,
      "minimum_required": 1
    },
    "ads": {
      "1:1": {
        "count": 3,
        "paths": [
          "outputs/20251103_150000/ads/1_1/ad_en.png",
          "outputs/20251103_150000/ads/1_1/ad_es.png",
          "outputs/20251103_150000/ads/1_1/ad_fr.png"
        ]
      },
      "9:16": {
        "count": 3,
        "paths": [
          "outputs/20251103_150000/ads/9_16/ad_en.png",
          "outputs/20251103_150000/ads/9_16/ad_es.png",
          "outputs/20251103_150000/ads/9_16/ad_fr.png"
        ]
      },
      "16:9": {
        "count": 1,
        "paths": [
          "outputs/20251103_150000/ads/16_9/ad_original.png"
        ]
      }
    }
  }
}
```

**Agent Monitoring Considerations:**
- **Environment Assets:**
  - Minimum required: 1
  - Recommended: 3+ for variety
  - Alert if 0 environments generated

- **Product Assets:**
  - Expected: 6 views per product (front, back, left, right, top-down, bottom-up)
  - Alert if any product is missing views
  - Check if paths exist on filesystem

- **Ad Creatives:**
  - Compare generated count vs expected count from localization settings
  - Alert if count < 3 per aspect ratio (insufficient for A/B testing)
  - Verify aspect ratio matches: 1:1 = 1080x1080, 9:16 = 1080x1920, 16:9 = 1920x1080

---

### 5. Campaign Status & Metrics

Track generation progress and quality:

```json
{
  "status": {
    "phase": "generation_complete",
    "progress": 100,
    "errors": [],
    "warnings": [
      "Only 2 environment variants generated (recommended: 3+)"
    ]
  },
  "metrics": {
    "total_assets_generated": 20,
    "generation_time_seconds": 245,
    "api_calls_made": 20,
    "estimated_cost_usd": 0.40,
    "variant_diversity": {
      "environments": 4,
      "products": 12,
      "ad_creatives": 7,
      "total_variants": 23
    }
  }
}
```

**Agent Monitoring Considerations:**
- **Phase Values:**
  - `configuration` - Campaign being set up
  - `environment_generation` - Generating background scenes
  - `product_generation` - Generating product views
  - `ad_composition` - Creating final ads
  - `generation_complete` - All assets generated
  - `failed` - Generation failed

- **Quality Checks:**
  - Are there any errors? (Automatic alert)
  - Warnings should be reviewed but may not block
  - Generation time > 600 seconds may indicate issues
  - Variant diversity below thresholds triggers alerts

---

## Alert Triggers & Thresholds

### Critical Alerts (Immediate Action Required)

1. **No Assets Generated**
   ```
   Condition: assets.ads[*].count == 0
   Message: "Campaign {campaign_id} failed to generate any ad creatives. Check API key and configuration."
   ```

2. **Incomplete Product Views**
   ```
   Condition: Any product has < 6 views
   Message: "Product {product_slug} missing views: {missing_views}. Generation may have failed."
   ```

3. **Generation Failure**
   ```
   Condition: status.phase == "failed" OR len(status.errors) > 0
   Message: "Campaign {campaign_id} generation failed: {error_message}"
   ```

4. **Missing Required Translations**
   ```
   Condition: localization.enabled && missing translations
   Message: "Campaign {campaign_id} has localization enabled but missing translations for {languages}"
   ```

### Warning Alerts (Review Recommended)

1. **Low Variant Count**
   ```
   Condition: assets.ads[aspect_ratio].count < 3
   Message: "Campaign {campaign_id} has only {count} variants for {aspect_ratio}. Recommended minimum: 3 for A/B testing."
   ```

2. **Insufficient Environment Diversity**
   ```
   Condition: assets.environments.generated_count < 3
   Message: "Campaign {campaign_id} has only {count} environment backgrounds. Consider generating more for variety."
   ```

3. **Single Product Mode**
   ```
   Condition: len(generation_config.product_slugs) == 1 && product_mode == "combined"
   Message: "Only one product specified with 'combined' mode. Consider using 'separate' mode instead."
   ```

4. **Long Generation Time**
   ```
   Condition: metrics.generation_time_seconds > 600
   Message: "Campaign {campaign_id} took {time}s to generate. Consider optimizing settings or checking API performance."
   ```

5. **Invalid Campaign ID Format**
   ```
   Condition: campaign_id does not match YYYYMMDD_HHMMSS format
   Message: "Campaign {campaign_id} uses invalid ID format. Expected timestamp format: YYYYMMDD_HHMMSS (e.g., 20251103_152000)"
   ```

---

## Automated Generation Workflow

The system uses Gradio's `.then()` chaining to automatically execute generation steps:

### Workflow Sequence

```python
# Triggered when JSON file is loaded
load_json_file.change()          # 1. Load configuration
  .then(translate_message)        # 2. Generate translations
  .then(generate_environments)    # 3. Generate 4 environments
  .then(generate_product_views)   # 4. Generate product views
  .then(switch_to_preview_tab)    # 5. Show all assets
```

### Expected Generation Times

- **Translations:** ~2-5 seconds (4 languages via Google Translator)
- **Environments:** ~30-60 seconds (4 images via Gemini 2.5 Flash)
- **Products:** ~60-120 seconds (6 views per product via Gemini 2.5 Flash)
- **Total for typical campaign:** 2-3 minutes

### Monitoring the Workflow

An agent should track:
1. **Workflow Progress:** Which step is currently executing?
2. **Step Completion:** Did each step succeed?
3. **Asset Counts:** Are all expected assets generated?
4. **Error Detection:** Did any step fail or timeout?

### Expected Outputs by Step

| Step | Output | Count | Location |
|------|--------|-------|----------|
| Load JSON | Config populated | 1 | Memory (Gradio state) |
| Translations | Language variants | 4-6 | `messaging.translations` |
| Environments | Background images | 4 | `outputs/{id}/environments/` |
| Products | Product views | 6 × num_products | `outputs/{id}/products/` |

### Failure Scenarios

**Scenario 1: Translation Failure**
- Cause: Invalid region key or API error
- Impact: Localized ads cannot be generated
- Detection: Empty `translations` object

**Scenario 2: Environment Generation Failure**
- Cause: API quota exceeded, invalid prompt
- Impact: No background scenes for ads
- Detection: `outputs/{id}/environments/` is empty or < 4 images

**Scenario 3: Product Generation Failure**
- Cause: Invalid product slug, missing reference photos
- Impact: Cannot create product-focused ads
- Detection: `outputs/{id}/products/` missing views or < 6 per product

---

## Monitoring Query Examples

### Example 1: Campaign Completion Check

**Query:** "Is campaign 20251103_150000 complete and ready for deployment?"

**Required Context:**
```json
{
  "campaign_id": "20251103_150000",
  "status": {
    "phase": "generation_complete",
    "errors": [],
    "warnings": []
  },
  "assets": {
    "ads": {
      "1:1": {"count": 3},
      "9:16": {"count": 3},
      "16:9": {"count": 1}
    }
  },
  "expected_variants": {
    "1:1": 3,
    "9:16": 3,
    "16:9": 1
  }
}
```

**Expected Response:**
- ✅ Generation complete
- ✅ All expected variants generated
- ✅ No errors or warnings
- **Status:** Ready for deployment

---

### Example 2: Insufficient Assets Alert

**Query:** "Check asset diversity for campaign 20251103_140000"

**Required Context:**
```json
{
  "campaign_id": "20251103_140000",
  "assets": {
    "environments": {"count": 1},
    "ads": {
      "1:1": {"count": 1},
      "9:16": {"count": 1},
      "16:9": {"count": 1}
    }
  },
  "thresholds": {
    "environments": {"recommended": 3},
    "ads_per_format": {"recommended": 3}
  }
}
```

**Expected Response:**
- ⚠️ Only 1 environment background (recommended: 3+)
- ⚠️ Only 1 variant per aspect ratio (recommended: 3+ for A/B testing)
- **Action:** Generate additional variants for better diversity

---

### Example 3: Missing Product Views

**Query:** "Validate product assets for campaign 20251103_130000"

**Required Context:**
```json
{
  "campaign_id": "20251103_130000",
  "products": {
    "eco-cleaner": {
      "expected_views": 6,
      "generated_views": ["front", "back", "left", "right"],
      "missing_views": ["top-down", "bottom-up"]
    },
    "yoga-mat": {
      "expected_views": 6,
      "generated_views": ["front", "back", "left", "right", "top-down", "bottom-up"],
      "missing_views": []
    }
  }
}
```

**Expected Response:**
- ❌ Product "eco-cleaner" missing views: top-down, bottom-up
- ✅ Product "yoga-mat" complete (6/6 views)
- **Action:** Regenerate missing views for eco-cleaner

---

## File System Context

The agent should have access to these directory structures:

```
outputs/{campaign_id}/
├── campaign_config.json          # Complete campaign configuration
├── environments/                 # Background scene images
│   ├── env_001.png
│   ├── env_002.png
│   └── ...
├── products/                     # Product view images
│   ├── {product-slug}_front.png
│   ├── {product-slug}_back.png
│   └── ...
└── ads/                          # Final ad creatives
    ├── 1_1/
    │   ├── ad_{language}.png
    │   └── ...
    ├── 9_16/
    │   └── ...
    └── 16_9/
        └── ...
```

**Monitoring Checks:**
- Verify campaign_config.json exists and is valid JSON
- Count files in each directory
- Check file sizes (0 bytes = failed generation)
- Verify image files are valid (can be opened by PIL/Pillow)

---

## Region & Audience Reference

Available targeting options that should be validated:

**Regions:**
- `north_america` → Languages: en, es, fr
- `europe` → Languages: en, de, fr, es, it
- `asia_pacific` → Languages: en, zh-CN, ja, ko, th
- `latin_america` → Languages: es, pt, en
- `middle_east_africa` → Languages: ar, en, fr
- `oceania` → Languages: en

**Audiences:**
- `tech_enthusiasts`
- `health_conscious`
- `budget_shoppers`
- `luxury_buyers`
- `eco_conscious`
- `families`
- `professionals`
- `students`

---

## Summary: Key Monitoring Points

An AI monitoring agent should check:

1. **Campaign Completeness**
   - All required fields present in configuration
   - Valid region and audience selections
   - Translations available for target region

2. **Asset Counts**
   - Environments: ≥1 (warn if <3)
   - Products: 6 views per product
   - Ads: Match expected variant count from localization settings

3. **Quality Checks**
   - No generation errors
   - All files exist and are non-zero size
   - Generation completed in reasonable time (<10 minutes)

4. **Diversity Metrics**
   - At least 3 variants per aspect ratio for A/B testing
   - Multiple environment backgrounds for variety
   - Complete product view coverage

5. **Configuration Validation**
   - Product slugs exist in products directory
   - Logo paths are valid
   - Aspect ratio settings are consistent

This context structure enables the LLM to generate human-readable alerts like:

> "Campaign 20251103_150000 for North America health-conscious audience is complete with 7 ad variants across 3 formats. However, only 2 environment backgrounds were generated (recommended: 3+). Consider generating additional environments for better creative diversity."
