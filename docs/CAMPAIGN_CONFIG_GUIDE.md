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

### In the Gradio Interface

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
