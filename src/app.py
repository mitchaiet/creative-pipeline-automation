"""
Creative Automation Pipeline - Gradio Interface
"""
import os
import json
from pathlib import Path
import gradio as gr
from typing import List, Tuple, Optional
from dotenv import load_dotenv, set_key
from google import genai
from google.genai import types
import yaml
from datetime import datetime
from PIL import Image
from io import BytesIO
import plotly.graph_objects as go
import plotly.express as px
from deep_translator import GoogleTranslator
import random
import string

# Load environment variables
load_dotenv()

# Base directories
PRODUCTS_DIR = Path("products")
CONFIG_DIR = Path("config")
ENV_FILE = Path(".env")

# Product views to generate with detailed angle descriptions
PRODUCT_VIEWS = {
    "front": "straight-on front view, camera directly facing the front of the product at eye level, showing the primary face/label",
    "back": "straight-on back/rear view, camera directly facing the back of the product at eye level, 180 degrees opposite from the front",
    "left": "left side profile view, camera positioned 90 degrees to the left of the front view, showing the left edge/side panel",
    "right": "right side profile view, camera positioned 90 degrees to the right of the front view, showing the right edge/side panel",
    "top-down": "top view looking straight down from directly above the product, showing the top surface as if the camera is mounted on the ceiling",
    "bottom-up": "bottom view looking straight up from directly below the product, showing the bottom/base surface"
}

# Region to country codes mapping for map visualization
REGION_COUNTRIES = {
    "north_america": ["USA", "CAN"],
    "europe": ["GBR", "FRA", "DEU", "ITA", "ESP", "NLD", "BEL", "CHE", "AUT", "SWE", "NOR", "DNK", "FIN", "POL", "CZE", "IRL", "PRT", "GRC"],
    "asia_pacific": ["CHN", "JPN", "KOR", "IND", "IDN", "THA", "VNM", "PHL", "MYS", "SGP", "AUS", "NZL", "TWN", "HKG"],
    "latin_america": ["MEX", "BRA", "ARG", "CHL", "COL", "PER", "VEN", "ECU", "GTM", "CUB", "HTI", "DOM", "HND", "BOL", "PRY", "URY", "CRI", "PAN", "NIC", "SLV"],
    "middle_east_africa": ["SAU", "ARE", "QAT", "KWT", "OMN", "BHR", "EGY", "MAR", "DZA", "TUN", "LBY", "ZAF", "NGA", "KEN", "ETH", "GHA", "TZA", "UGA", "ISR", "JOR", "LBN", "IRQ", "IRN"],
    "oceania": ["AUS", "NZL", "FJI", "PNG", "NCL", "PYF", "GUM", "SLB"]
}


def generate_campaign_id() -> str:
    """Generate a unique 6-digit alphanumeric campaign ID."""
    # Use uppercase letters and digits, excluding similar-looking characters (0, O, I, 1)
    chars = '23456789ABCDEFGHJKLMNPQRSTUVWXYZ'
    return ''.join(random.choices(chars, k=6))


def load_regions_config() -> dict:
    """Load regions configuration from YAML file."""
    config_path = CONFIG_DIR / "regions.yaml"
    if not config_path.exists():
        return {}

    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
        return config.get('regions', {})


def load_audiences_config() -> dict:
    """Load audiences configuration from YAML file."""
    config_path = CONFIG_DIR / "audiences.yaml"
    if not config_path.exists():
        return {}

    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
        return config.get('audiences', {})


def get_region_choices() -> List[Tuple[str, str]]:
    """Get list of regions as (display_name, key) tuples for dropdown."""
    regions = load_regions_config()
    return [(info['name'], key) for key, info in regions.items()]


def get_audience_choices() -> List[Tuple[str, str]]:
    """Get list of audiences as (display_name, key) tuples for dropdown."""
    audiences = load_audiences_config()
    return [(info['name'], key) for key, info in audiences.items()]


def create_world_map(selected_region: Optional[str] = None):
    """Create an interactive world map with highlighted regions."""

    # Create a mapping of all countries to their region
    country_to_region = {}
    for region_key, countries in REGION_COUNTRIES.items():
        for country in countries:
            country_to_region[country] = region_key

    # Get all unique countries
    all_countries = list(country_to_region.keys())

    # Create data for the map
    region_names = load_regions_config()

    # Assign colors based on selection
    colors = []
    hover_texts = []

    for country in all_countries:
        region_key = country_to_region[country]
        region_info = region_names.get(region_key, {})
        region_name = region_info.get('name', region_key)

        if selected_region == region_key:
            colors.append(1)  # Highlighted
            hover_texts.append(f"{region_name}<br><b>SELECTED</b>")
        else:
            colors.append(0.3)  # Dimmed
            hover_texts.append(region_name)

    # Create the choropleth map
    fig = go.Figure(data=go.Choropleth(
        locations=all_countries,
        z=colors,
        locationmode='ISO-3',
        colorscale=[
            [0, '#E8E8E8'],      # Unselected (light gray)
            [0.5, '#4A90E2'],    # Mid (blue)
            [1, '#2E5C8A']       # Selected (dark blue)
        ],
        showscale=False,
        hovertext=hover_texts,
        hoverinfo='text',
        marker=dict(
            line=dict(
                color='white',
                width=0.5
            )
        )
    ))

    fig.update_geos(
        projection_type="natural earth",
        showland=True,
        landcolor='#F5F5F5',
        showcountries=True,
        countrycolor='white',
        showcoastlines=True,
        coastlinecolor='white',
        showlakes=False,
        showocean=True,
        oceancolor='#E3F2FD',
        bgcolor='#FAFAFA'
    )

    fig.update_layout(
        height=500,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='#FAFAFA',
        geo=dict(
            bgcolor='#FAFAFA'
        )
    )

    return fig


def get_region_from_click(click_data):
    """Extract region key from map click data."""
    if not click_data or not click_data.get('points'):
        return None

    # Get the clicked country code
    point = click_data['points'][0]
    country_code = point.get('location')

    if not country_code:
        return None

    # Find which region this country belongs to
    for region_key, countries in REGION_COUNTRIES.items():
        if country_code in countries:
            return region_key

    return None


def get_available_products() -> List[str]:
    """Get list of all available products from the products directory."""
    if not PRODUCTS_DIR.exists():
        return []

    products = []
    for item in PRODUCTS_DIR.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            products.append(item.name)

    return sorted(products)


def get_product_images(product_slug: str, image_type: str) -> List[str]:
    """Get all images for a product of a specific type (product or logo)."""
    if not product_slug:
        return []

    image_dir = PRODUCTS_DIR / product_slug / "photos" / image_type

    if not image_dir.exists():
        return []

    # Supported image formats
    image_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.gif', '.avif', '.svg', '.bmp'}

    # Files to ignore
    ignore_files = {'.gitkeep', '.ds_store'}

    images = []
    for file in image_dir.iterdir():
        # Skip if it's a directory or should be ignored
        if not file.is_file() or file.name.lower() in ignore_files:
            continue

        # Check if it has a supported image extension
        if file.suffix.lower() in image_extensions:
            images.append(str(file))

    return sorted(images)


def load_product(product_slugs) -> Tuple[List[str], List[str]]:
    """Load product photos and logos for the selected products."""
    if not product_slugs:
        return [], []

    # Handle both single string and list
    if isinstance(product_slugs, str):
        product_slugs = [product_slugs]

    all_product_photos = []
    all_logo_photos = []

    for product_slug in product_slugs:
        product_photos = get_product_images(product_slug, "product")
        logo_photos = get_product_images(product_slug, "logo")
        all_product_photos.extend(product_photos)
        all_logo_photos.extend(logo_photos)

    return all_product_photos, all_logo_photos


def save_api_key(api_key: str) -> str:
    """Save the Google API key to .env file and environment."""
    if not api_key or not api_key.strip():
        return "⚠️ Please enter a valid API key"

    # Create .env file if it doesn't exist
    if not ENV_FILE.exists():
        ENV_FILE.write_text("# Environment Variables\n")

    # Save to .env file
    set_key(str(ENV_FILE), "GOOGLE_API_KEY", api_key.strip())

    # Set in current environment
    os.environ["GOOGLE_API_KEY"] = api_key.strip()

    return "✅ API key saved successfully!"


def get_api_key_status() -> str:
    """Check if API key is configured."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key and api_key != "your_api_key_here":
        masked_key = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "***"
        return f"✅ API Key configured: {masked_key}"
    return "⚠️ API Key not configured"


def load_product_config(product_slug: str) -> Optional[dict]:
    """Load product configuration from YAML file."""
    config_path = PRODUCTS_DIR / product_slug / "config.yaml"
    if not config_path.exists():
        return None

    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def generate_product_views(product_slugs, generation_mode: str, campaign_id: str, progress=gr.Progress()) -> Tuple[str, List[str]]:
    """Generate all product views using Gemini 2.5 Flash Image with existing product photos as reference."""

    # Handle both single string and list
    if isinstance(product_slugs, str):
        product_slugs = [product_slugs]

    # Check products selected
    if not product_slugs:
        return "❌ Error: Please select at least one product first", []

    # Check API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        return "❌ Error: Please configure your API key in Settings tab first", []

    # Create campaign directory structure (use campaign_id only, no timestamp)
    campaign_dir = Path("outputs") / campaign_id

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    generated_images = []

    try:
        # Initialize Gemini client
        client = genai.Client(api_key=api_key)

        if generation_mode == "separate":
            # Generate separate views for each product
            for product_idx, product_slug in enumerate(product_slugs):
                progress((product_idx) / len(product_slugs), desc=f"Processing {product_slug}...")

                # Load product config
                config = load_product_config(product_slug)
                if not config:
                    continue

                product_info = config.get('product', {})
                product_name = product_info.get('name', product_slug)
                description = product_info.get('description', '')

                # Load existing product photos
                existing_photo_paths = get_product_images(product_slug, "product")
                if not existing_photo_paths:
                    continue

                # Load as PIL Images
                reference_images = []
                for photo_path in existing_photo_paths:
                    try:
                        img = Image.open(photo_path)
                        reference_images.append(img)
                    except Exception as e:
                        print(f"Warning: Could not load {photo_path}: {e}")

                if not reference_images:
                    continue

                # Create product directory in campaign folder
                generated_dir = campaign_dir / "products" / product_slug
                generated_dir.mkdir(parents=True, exist_ok=True)

                # Generate each view
                for idx, (view_name, view_description) in enumerate(PRODUCT_VIEWS.items()):
                    total_progress = (product_idx * len(PRODUCT_VIEWS) + idx + 1) / (len(product_slugs) * len(PRODUCT_VIEWS))
                    progress(total_progress, desc=f"{product_slug}: {view_name} view...")

                    prompt = f"""Study the provided reference images of this {product_name} product.

Generate a professional product photography shot with this EXACT camera angle: {view_description}.

Product details: {description}

CRITICAL REQUIREMENTS:
- The product MUST look identical to the reference images (same shape, size, colors, labels, text, branding)
- Pure white background (#FFFFFF)
- Professional studio lighting with soft shadows
- Camera angle: {view_description}
- High resolution, sharp focus
- Photorealistic rendering
- Square aspect ratio (1:1)

Output only the product photograph from the specified angle. Do not include any text, labels, or annotations."""

                    contents = [prompt] + reference_images
                    response = client.models.generate_content(
                        model="gemini-2.5-flash-image",
                        contents=contents,
                        config=types.GenerateContentConfig(
                            response_modalities=["IMAGE"],
                            image_config=types.ImageConfig(
                                aspect_ratio="1:1",
                            )
                        )
                    )

                    image_parts = [
                        part.inline_data.data
                        for part in response.candidates[0].content.parts
                        if part.inline_data
                    ]

                    if image_parts:
                        image = Image.open(BytesIO(image_parts[0]))
                        filename = f"{view_name}_{timestamp}.png"
                        filepath = generated_dir / filename
                        image.save(filepath, "PNG")
                        generated_images.append(str(filepath))

            return f"✅ Successfully generated {len(generated_images)} separate product views for {len(product_slugs)} product(s)!\n\n**Campaign Folder:** `{campaign_dir}/`\n\nProducts saved to: `{campaign_dir / 'products'}/`", generated_images

        else:  # combined mode
            # Load all product configs and images
            all_product_names = []
            all_descriptions = []
            all_reference_images = []

            for product_slug in product_slugs:
                config = load_product_config(product_slug)
                if not config:
                    continue

                product_info = config.get('product', {})
                all_product_names.append(product_info.get('name', product_slug))
                all_descriptions.append(product_info.get('description', ''))

                # Load product photos
                existing_photo_paths = get_product_images(product_slug, "product")
                for photo_path in existing_photo_paths:
                    try:
                        img = Image.open(photo_path)
                        all_reference_images.append(img)
                    except Exception as e:
                        print(f"Warning: Could not load {photo_path}: {e}")

            if not all_reference_images:
                return "❌ Error: Could not load any product photos", []

            # Create output directory for combined images in campaign folder
            combined_dir = campaign_dir / "products" / "combined"
            combined_dir.mkdir(parents=True, exist_ok=True)

            # Generate combined views
            products_str = " and ".join(all_product_names)
            descriptions_str = ". ".join(all_descriptions)

            for idx, (view_name, view_description) in enumerate(PRODUCT_VIEWS.items()):
                progress((idx + 1) / len(PRODUCT_VIEWS), desc=f"Generating combined {view_name} view...")

                prompt = f"""Study the provided reference images showing multiple products: {products_str}.

Generate a professional product photography shot showing ALL products together in a single composition with this EXACT camera angle: {view_description}.

Products: {descriptions_str}

CRITICAL REQUIREMENTS:
- Show ALL products together in the same image
- Each product MUST look identical to its reference images (same shape, size, colors, labels, text, branding)
- Arrange products in an aesthetically pleasing composition
- Pure white background (#FFFFFF)
- Professional studio lighting with soft shadows
- Camera angle: {view_description}
- High resolution, sharp focus
- Photorealistic rendering
- Square aspect ratio (1:1)

Output only the product photograph from the specified angle showing all products together."""

                contents = [prompt] + all_reference_images
                response = client.models.generate_content(
                    model="gemini-2.5-flash-image",
                    contents=contents,
                    config=types.GenerateContentConfig(
                        response_modalities=["IMAGE"],
                        image_config=types.ImageConfig(
                            aspect_ratio="1:1",
                        )
                    )
                )

                image_parts = [
                    part.inline_data.data
                    for part in response.candidates[0].content.parts
                    if part.inline_data
                ]

                if image_parts:
                    image = Image.open(BytesIO(image_parts[0]))
                    filename = f"combined_{view_name}_{timestamp}.png"
                    filepath = combined_dir / filename
                    image.save(filepath, "PNG")
                    generated_images.append(str(filepath))

            return f"✅ Successfully generated {len(generated_images)} combined product views showing {len(product_slugs)} product(s) together!\n\n**Campaign Folder:** `{campaign_dir}/`\n\nProducts saved to: `{combined_dir}/`", generated_images

    except Exception as e:
        return f"❌ Error during generation: {str(e)}", generated_images


def translate_message(message: str, region_key: str) -> str:
    """Translate campaign message to top languages for the selected region."""
    if not message or not message.strip():
        return "⚠️ Please enter a campaign message first"

    if not region_key:
        return "⚠️ Please select a target region in the Campaign tab first"

    # Load regions config
    regions = load_regions_config()
    region = regions.get(region_key, {})

    if not region:
        return "⚠️ Invalid region selected"

    # Get top languages for this region
    top_languages = region.get('top_languages', [])

    if not top_languages:
        return "⚠️ No languages configured for this region"

    # Build translations output
    region_name = region.get('name', region_key)
    output = f"## Translations for {region_name}\n\n"
    output += f"**Original Message:**\n{message}\n\n---\n\n"

    try:
        for lang in top_languages:
            lang_code = lang.get('code')
            lang_name = lang.get('name')

            # Skip English if message is already in English (common case)
            if lang_code == 'en':
                output += f"**{lang_name}:**\n{message}\n\n"
                continue

            try:
                # Translate using GoogleTranslator
                translator = GoogleTranslator(source='auto', target=lang_code)
                translated = translator.translate(message)
                output += f"**{lang_name}:**\n{translated}\n\n"
            except Exception as lang_error:
                output += f"**{lang_name}:**\n⚠️ Translation error: {str(lang_error)}\n\n"

        return output

    except Exception as e:
        return f"❌ Translation error: {str(e)}"


def get_message_translations(message: str, region_key: str) -> List[dict]:
    """Get translations of a message for a region's top languages.

    Returns list of dicts with 'language' and 'text' keys.
    """
    if not message or not message.strip() or not region_key:
        return []

    # Load regions config
    regions = load_regions_config()
    region = regions.get(region_key, {})

    if not region:
        return []

    # Get top languages for this region
    top_languages = region.get('top_languages', [])

    if not top_languages:
        return []

    translations = []

    try:
        for lang in top_languages:
            lang_code = lang.get('code')
            lang_name = lang.get('name')

            # Skip English if message is already in English (use original)
            if lang_code == 'en':
                translations.append({
                    'language': lang_name,
                    'code': lang_code,
                    'text': message
                })
                continue

            try:
                # Translate using GoogleTranslator
                translator = GoogleTranslator(source='auto', target=lang_code)
                translated = translator.translate(message)
                translations.append({
                    'language': lang_name,
                    'code': lang_code,
                    'text': translated
                })
            except Exception as lang_error:
                print(f"Warning: Could not translate to {lang_name}: {lang_error}")
                # Still include the original message if translation fails
                translations.append({
                    'language': lang_name,
                    'code': lang_code,
                    'text': message
                })

        return translations

    except Exception as e:
        print(f"Error getting translations: {e}")
        return []


def generate_random_campaign_message() -> str:
    """Generate a random campaign message."""
    import random

    messages = [
        "Discover the power of nature with our eco-friendly cleaning solution. Made with 100% plant-based ingredients, safe for your family and the planet.",
        "Fuel your day with premium organic energy. Packed with superfoods and zero artificial ingredients. Feel the difference.",
        "Transform your mornings with the perfect cup. Ethically sourced, expertly roasted, delivered fresh to your door.",
        "Your fitness journey starts here. Professional-grade equipment meets innovative design. Achieve your goals faster.",
        "Elevate your wellness routine. Premium ingredients, proven results, trusted by thousands. Experience the difference today.",
        "Adventure awaits with gear built to last. Designed for explorers, tested in extreme conditions. Go further with confidence.",
        "Comfort meets style in every thread. Sustainable fabrics, timeless design, uncompromising quality. Wear what matters.",
        "Unlock your potential with cutting-edge technology. Intuitive design meets powerful performance. Stay ahead of the curve.",
        "Nourish your body, fuel your life. Whole food nutrition made simple. Taste the quality in every bite.",
        "Make every moment count. Precision crafted for those who demand excellence. Your time deserves the best.",
        "Refresh naturally. Pure ingredients, bold flavors, zero compromise. Hydration that tastes as good as it feels.",
        "Sleep better, live better. Premium comfort engineered for perfect rest. Wake up refreshed every morning.",
        "Clean beauty that works. Science-backed formulas, nature-inspired ingredients. Radiance from the inside out.",
        "Your productivity partner. Seamlessly integrate work and life with tools designed for modern achievers.",
        "Taste the tradition. Handcrafted quality passed down through generations. Every sip tells a story.",
        "Protect what matters most. Advanced technology meets peace of mind. Trusted by families everywhere.",
        "Simplify your routine. Smart solutions for everyday challenges. More time for what you love.",
        "Premium performance without the premium price. Quality you can trust, value you can feel.",
        "Join the movement. Sustainable choices that make a real impact. Together, we create change.",
        "Experience luxury you can afford. Sophisticated design meets accessible pricing. Elevate your everyday."
    ]

    return random.choice(messages)


def generate_random_environment() -> str:
    """Generate a random environment prompt."""
    import random

    environments = [
        "Modern minimalist kitchen with marble countertops and natural sunlight",
        "Cozy living room with plush furniture and warm lighting",
        "Urban rooftop terrace with city skyline in the background",
        "Bright and airy home office with plants and wooden desk",
        "Sleek contemporary bathroom with spa-like atmosphere",
        "Trendy coffee shop interior with exposed brick and vintage decor",
        "Outdoor garden patio with lush greenery and comfortable seating",
        "Professional gym with modern equipment and large windows",
        "Beach boardwalk at sunset with ocean views",
        "Mountain cabin interior with stone fireplace and cozy ambiance",
        "High-end restaurant dining area with elegant table settings",
        "Modern yoga studio with bamboo floors and natural light",
        "Stylish bedroom with neutral tones and contemporary furniture",
        "Industrial loft with high ceilings and exposed pipes",
        "Tropical resort poolside with palm trees and lounge chairs",
        "Rustic farmhouse kitchen with wooden beams and vintage appliances",
        "Futuristic tech workspace with LED lighting and glass walls",
        "Serene meditation room with candles and soft textures",
        "Vibrant art gallery with white walls and spotlights",
        "Outdoor camping scene with tent and mountain backdrop"
    ]

    return random.choice(environments)


def generate_environments(prompt: str, campaign_id: str, progress=gr.Progress()) -> Tuple[str, List[str]]:
    """Generate 4 background environment images using Gemini."""
    if not prompt or not prompt.strip():
        return "⚠️ Please enter an environment prompt first", []

    # Check API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        return "❌ Error: Please configure your API key in Settings tab first", []

    # Create campaign directory structure (use campaign_id only, no timestamp)
    campaign_dir = Path("outputs") / campaign_id
    outputs_dir = campaign_dir / "environments"
    outputs_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    generated_images = []

    try:
        # Initialize Gemini client
        client = genai.Client(api_key=api_key)

        # Generate 4 environment variations
        for i in range(4):
            progress((i + 1) / 4, desc=f"Generating environment {i + 1}/4...")

            full_prompt = f"""Create a professional background environment photograph based on this description: {prompt}

CRITICAL REQUIREMENTS:
- Pure photorealistic environment scene
- No products, no people, just the background setting
- Square aspect ratio (1:1)
- High resolution, sharp focus
- Professional photography quality
- Perfect for product placement in post-production
- Clean, uncluttered composition
- Proper lighting and depth

Variation {i + 1}: Add subtle variation in camera angle or lighting while maintaining the same overall scene."""

            response = client.models.generate_content(
                model="gemini-2.5-flash-image",
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE"],
                    image_config=types.ImageConfig(
                        aspect_ratio="1:1",
                    )
                )
            )

            image_parts = [
                part.inline_data.data
                for part in response.candidates[0].content.parts
                if part.inline_data
            ]

            if image_parts:
                image = Image.open(BytesIO(image_parts[0]))
                filename = f"environment_{i+1}_{timestamp}.png"
                filepath = outputs_dir / filename
                image.save(filepath, "PNG")
                generated_images.append(str(filepath))

        return f"✅ Successfully generated {len(generated_images)} environment backgrounds!\n\n**Campaign Folder:** `{campaign_dir}/`\n\nEnvironments saved to: `{outputs_dir}/`", generated_images

    except Exception as e:
        return f"❌ Error during generation: {str(e)}", generated_images


def generate_ad_compositions(selected_envs: List[str], selected_products: List[str], campaign_msg: str, selected_logos: List[str], include_logo_1_1: bool, include_logo_9_16: bool, include_logo_16_9: bool, region_key: str, audience_key: str, localize_1_1: bool, localize_9_16: bool, localize_16_9: bool, campaign_id: str, progress=gr.Progress()) -> Tuple[str, List[str], List[str], List[str], str]:
    """Generate final ad compositions in multiple aspect ratios using AI.

    If localization is enabled for a format, generates versions in all regional languages.
    All formats use the campaign message from the Messaging tab.
    """

    if not selected_envs:
        return "⚠️ Please select at least one environment in the Environments tab", [], [], [], ""

    if not selected_products:
        return "⚠️ Please select at least one product view in the Products tab", [], [], [], ""

    # Check API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        return "❌ Error: Please configure your API key in Settings tab first", [], [], [], ""

    try:
        # Use provided campaign ID for folder naming (no timestamp)
        campaign_dir = Path("outputs") / campaign_id
        campaign_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Create subdirectories for organized content
        environments_dir = campaign_dir / "environments"
        products_dir = campaign_dir / "products"
        ads_dir = campaign_dir / "ads"

        environments_dir.mkdir(parents=True, exist_ok=True)
        products_dir.mkdir(parents=True, exist_ok=True)
        # Note: ads subdirectories will be created when images are saved

        # Load first environment and product (using first selected)
        env_path = selected_envs[0]
        product_path = selected_products[0]

        progress(0.1, desc="Loading reference images...")

        # Load reference images
        env_img = Image.open(env_path)
        product_img = Image.open(product_path)

        # Copy ALL selected environment and product images to campaign folder
        import shutil
        for env in selected_envs:
            env_dest = environments_dir / Path(env).name
            shutil.copy2(env, env_dest)

        for prod in selected_products:
            product_dest = products_dir / Path(prod).name
            shutil.copy2(prod, product_dest)

        # Load logo if available
        logo_img = None
        if selected_logos and len(selected_logos) > 0:
            logo_path = selected_logos[0]
            logo_img = Image.open(logo_path)

        # Initialize Gemini client
        client = genai.Client(api_key=api_key)

        # Define aspect ratios with descriptive names and API aspect ratio values
        aspect_ratios = {
            "1_1": {
                "size": "1:1 square",
                "aspect_ratio": "1:1",
                "dimensions": "1080x1080",
                "description": "Instagram feed and Facebook posts",
                "include_logo": include_logo_1_1,
                "localize": localize_1_1
            },
            "9_16": {
                "size": "9:16 vertical",
                "aspect_ratio": "9:16",
                "dimensions": "1080x1920",
                "description": "Instagram Stories, TikTok, and Reels",
                "include_logo": include_logo_9_16,
                "localize": localize_9_16
            },
            "16_9": {
                "size": "16:9 landscape",
                "aspect_ratio": "16:9",
                "dimensions": "1920x1080",
                "description": "YouTube and desktop ads",
                "include_logo": include_logo_16_9,
                "localize": localize_16_9
            }
        }

        # Build comprehensive campaign configuration
        campaign_config = {
            "campaign": {
                "name": f"Campaign {campaign_id}",
                "id": campaign_id,
                "created_at": datetime.now().isoformat(),
                "source": "manual",
                "type": "manual_generation"
            },
            "targeting": {
                "region": region_key if region_key else None,
                "audience": audience_key if audience_key else None
            },
            "region": region_key if region_key else None,  # Keep for backwards compatibility
            "messaging": {
                "primary_message": campaign_msg,
                "localizations_enabled": {
                    "1:1": localize_1_1,
                    "9:16": localize_9_16,
                    "16:9": localize_16_9
                }
            },
            "assets": {
                "environments": selected_envs,
                "products": selected_products,
                "logos": selected_logos if selected_logos else []
            },
            "generation_settings": {
                "aspect_ratios": {
                    "1:1": {
                        "enabled": True,
                        "include_logo": include_logo_1_1,
                        "localize": localize_1_1
                    },
                    "9:16": {
                        "enabled": True,
                        "include_logo": include_logo_9_16,
                        "localize": localize_9_16
                    },
                    "16:9": {
                        "enabled": True,
                        "include_logo": include_logo_16_9,
                        "localize": localize_16_9
                    }
                }
            }
        }

        # Always fetch translations for documentation (if region is selected)
        translations = []
        if region_key and campaign_msg:
            progress(0.05, desc="Getting translations...")
            translations = get_message_translations(campaign_msg, region_key)

        # Add translations to campaign config (always include for documentation)
        if translations:
            campaign_config["messaging"]["translations"] = translations

        # Save campaign configuration to JSON
        config_file = campaign_dir / "campaign_config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(campaign_config, f, indent=2, ensure_ascii=False)

        # Check if localization is needed for actual generation
        if localize_1_1 or localize_9_16 or localize_16_9:
            if not region_key:
                return "⚠️ Please select a region in Campaign tab to use localization feature.", [], [], [], json.dumps(campaign_config, indent=2, ensure_ascii=False)
            if not translations:
                return "⚠️ Could not get translations. Please select a region in Campaign tab or disable localization.", [], [], [], json.dumps(campaign_config, indent=2, ensure_ascii=False)

        outputs = {
            "1_1": [],
            "9_16": [],
            "16_9": []
        }

        total_generations = 0
        for config in aspect_ratios.values():
            if config['localize'] and translations:
                total_generations += len(translations)
            else:
                total_generations += 1

        generation_count = 0

        for idx, (name, config) in enumerate(aspect_ratios.items()):
            # Check if logo should be included for this format
            should_include_logo = config['include_logo'] and logo_img is not None

            # Determine messages to generate
            messages_to_generate = []
            if config['localize'] and translations:
                # Generate for all translations
                for trans in translations:
                    messages_to_generate.append({
                        'text': trans['text'],
                        'language': trans['language'],
                        'code': trans['code']
                    })
            else:
                # Generate single version with campaign message
                ad_copy = campaign_msg if campaign_msg else "Premium product showcase"
                messages_to_generate.append({
                    'text': ad_copy,
                    'language': 'original',
                    'code': 'original'
                })

            # Generate ad for each message
            for msg_idx, msg_data in enumerate(messages_to_generate):
                generation_count += 1
                lang_desc = f" ({msg_data['language']})" if msg_data['language'] != 'original' else ""
                progress(generation_count / total_generations, desc=f"Generating {config['size']} ad{lang_desc}...")

                ad_copy = msg_data['text']

                # Build reference images list
                reference_list = "1. Background environment setting (use as the scene/backdrop)\n2. Product photograph (integrate naturally into the scene)"
                if should_include_logo:
                    reference_list += "\n3. Company logo (place subtly in corner or appropriate location)"

                # Build logo requirements
                logo_requirements = ""
                if should_include_logo:
                    logo_requirements = """
LOGO PLACEMENT:
- Include the company logo in the composition
- Place logo subtly in a corner or appropriate location
- Logo should be visible but not overwhelming
- Maintain logo clarity and branding
- Typical placement: top-right, top-left, or bottom-right corner
"""

                prompt = f"""Create a professional advertising image for {config['description']} in {config['size']} ({config['dimensions']}) format.

REFERENCE IMAGES PROVIDED:
{reference_list}

CRITICAL COMPOSITION REQUIREMENTS:
- Aspect ratio: {config['size']} ({config['dimensions']})
- Product must be the HERO/FOCAL POINT of the image - prominently featured and clearly visible
- Position product in the FOREGROUND, taking up 40-60% of the frame
- Product should be slightly closer to camera than other scene elements for depth and emphasis
- Use a medium-close composition that highlights product details while showing environment context

PRODUCT INTEGRATION & PERSPECTIVE:
- Match the product's perspective EXACTLY to the environment's viewing angle and camera position
- Ensure product orientation aligns naturally with the scene's vanishing point and horizon line
- The product must appear to physically exist within the 3D space of the environment
- Maintain consistent scale - product should look realistically sized for its placement
- If environment has a surface (table, counter, ground), place product ON that surface naturally
- Product should cast realistic shadows that match the environment's lighting direction
- Reflections and highlights on product must match the environment's light sources

LIGHTING & VISUAL COHERENCE:
- Product lighting MUST match environment lighting exactly (color temperature, intensity, direction)
- Match ambient light color - warm/cool tones should be consistent between product and scene
- Ensure product's highlights and shadows align with environment's light sources
- Add subtle environmental reflections on product surfaces when appropriate
- Professional advertising photography quality with polished, commercial-ready aesthetic
{logo_requirements}
AD COPY TO FEATURE:
"{ad_copy}"

TYPOGRAPHY & TEXT DESIGN:
- Place ad copy text prominently but not obscuring the product
- Text should be clear, readable, and professionally styled
- Use modern, bold, clean typography appropriate for premium advertising
- Text placement: typically top or bottom third, avoiding product area
- Consider visual hierarchy: headline bold and large, body text smaller
- Text should complement not compete with the product
- Use colors that contrast well with background for readability

FINAL OUTPUT REQUIREMENTS:
A polished, professional advertisement that:
1. Features the product as the clear hero with prominent placement
2. Integrates product seamlessly into environment with perfect perspective matching
3. Shows natural, realistic lighting and shadows throughout
4. Includes clear, compelling advertising copy
5. Looks like a premium commercial campaign creative ready for publication"""

                # Prepare content with reference images
                contents = [prompt, env_img, product_img]
                if should_include_logo:
                    contents.append(logo_img)

                # Generate with specific aspect ratio configuration
                response = client.models.generate_content(
                    model="gemini-2.5-flash-image",
                    contents=contents,
                    config=types.GenerateContentConfig(
                        response_modalities=["IMAGE"],
                        image_config=types.ImageConfig(
                            aspect_ratio=config["aspect_ratio"],
                        )
                    )
                )

                # Extract generated image with error handling
                image_parts = []
                if response and response.candidates and len(response.candidates) > 0:
                    candidate = response.candidates[0]
                    if candidate.content and candidate.content.parts:
                        image_parts = [
                            part.inline_data.data
                            for part in candidate.content.parts
                            if part.inline_data
                        ]

                if image_parts:
                    generated_img = Image.open(BytesIO(image_parts[0]))

                    # Save to organized structure: ads/[ratio]/[lang]/
                    ratio_dir = ads_dir / name
                    lang_code = msg_data['code'] if msg_data['code'] != 'original' else 'en'
                    lang_dir = ratio_dir / lang_code
                    lang_dir.mkdir(parents=True, exist_ok=True)

                    # Create filename with timestamp
                    file_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
                    filename = f"ad_{lang_code}_{file_timestamp}.png"
                    filepath = lang_dir / filename

                    generated_img.save(filepath, "PNG")
                    outputs[name].append(str(filepath))

        progress(1.0, desc="Complete!")

        # Build status message
        total_images = sum(len(imgs) for imgs in outputs.values())
        status_parts = [
            f"✅ Successfully generated {total_images} AI-powered ad image(s)!",
            f"\n**Campaign ID:** `{campaign_id}`",
            ""
        ]

        for format_name, images in outputs.items():
            if images:
                localized = len(images) > 1
                status_parts.append(f"- {format_name.replace('_', ':')}: {len(images)} image(s)" + (" (localized)" if localized else ""))

        status_parts.append(f"\n**Saved to:** `{campaign_dir}/`")
        status_parts.append(f"\n📁 Organized by aspect ratio and language")
        status_parts.append(f"📄 Complete JSON configuration saved")
        status = "\n".join(status_parts)

        # Format JSON for display
        json_str = json.dumps(campaign_config, indent=2, ensure_ascii=False)

        return status, outputs.get("1_1", []), outputs.get("9_16", []), outputs.get("16_9", []), json_str

    except Exception as e:
        return f"❌ Error generating ads: {str(e)}", [], [], [], ""


# ============================================================================
# Campaign Preview Functions
# ============================================================================

def build_generate_preview(region_key: str, audience_key: str, message: str) -> str:
    """Build a dynamic campaign preview for the Generate tab.

    Args:
        region_key: Selected region key
        audience_key: Selected audience key
        message: Campaign message

    Returns:
        Formatted markdown string with campaign details
    """
    if not region_key or not audience_key or not message:
        return """
### Campaign Preview

*Configure your campaign in the Campaign and Messaging tabs to see a preview here.*

**Required:**
- Target region (Campaign tab)
- Target audience (Campaign tab)
- Campaign message (Messaging tab)
        """

    # Load region and audience data
    regions = load_regions_config()
    audiences = load_audiences_config()

    region_data = regions.get(region_key, {})
    audience_data = audiences.get(audience_key, {})

    region_name = region_data.get('name', 'Unknown')
    audience_name = audience_data.get('name', 'Unknown')

    # Get top languages
    top_languages = region_data.get('top_languages', [])
    lang_list = ", ".join([lang.get('name', '') for lang in top_languages[:4]])

    # Build preview
    preview = f"""
### Campaign Configuration

**🌍 Target Region:** {region_name}
**👥 Target Audience:** {audience_name}
**💬 Campaign Message:** "{message}"

**🌐 Localization:** {len(top_languages[:4])} languages ({lang_list})

---

*Ready to generate professional ad creatives in 3 aspect ratios*
    """

    return preview.strip()


# ============================================================================
# Campaign JSON Functions
# ============================================================================

def load_campaign_from_json(json_path: str) -> tuple:
    """Load campaign configuration from JSON file and extract settings.

    Returns:
        Tuple of (region_key, audience_key, message, status_message, environments, products)
    """
    if not json_path:
        return None, None, "", "No file selected", [], []

    try:
        with open(json_path, 'r') as f:
            config = json.load(f)

        # Extract region and audience from targeting (new format) or fallback to region (old format)
        targeting = config.get("targeting", {})
        region_key = targeting.get("region") if targeting else config.get("region", None)
        audience_key = targeting.get("audience", None)

        # Extract message
        messaging = config.get("messaging", {})
        message = messaging.get("primary_message", "")

        # Extract asset paths
        assets = config.get("assets", {})
        environments = assets.get("environments", [])
        products = assets.get("products", [])

        # Get campaign info for status message
        campaign_info = config.get("campaign", {})
        campaign_name = campaign_info.get("name", "Campaign")
        campaign_id = campaign_info.get("id", "Unknown")

        status = f"✅ Loaded campaign: **{campaign_name}** (ID: `{campaign_id}`)\n\n"
        status += f"- Region: {region_key or 'Not specified'}\n"
        status += f"- Audience: {audience_key or 'Not specified'}\n"
        status += f"- Message: {len(message)} characters\n"
        status += f"- Environments: {len(environments)} asset(s)\n"
        status += f"- Products: {len(products)} asset(s)\n"

        return region_key, audience_key, message, status, environments, products

    except Exception as e:
        return None, None, "", f"❌ Error loading JSON: {str(e)}", [], []


def export_campaign_config(region_key: str, audience_key: str, message: str, selected_envs: List[str], selected_products: List[str]) -> str:
    """Export campaign configuration to JSON file."""

    # Create outputs directory
    outputs_dir = Path("outputs/campaigns")
    outputs_dir.mkdir(parents=True, exist_ok=True)

    # Build campaign data structure
    campaign_data = {
        "campaign_config": {
            "created_at": datetime.now().isoformat(),
            "region": None,
            "audience": None
        },
        "messaging": {
            "original_message": message if message else "",
        },
        "selected_assets": {
            "environments": selected_envs if selected_envs else [],
            "product_views": selected_products if selected_products else []
        }
    }

    # Load and add region details
    if region_key:
        regions = load_regions_config()
        region = regions.get(region_key, {})
        campaign_data["campaign_config"]["region"] = {
            "key": region_key,
            "name": region.get("name", ""),
            "description": region.get("description", ""),
            "top_languages": region.get("top_languages", [])
        }

    # Load and add audience details
    if audience_key:
        audiences = load_audiences_config()
        audience = audiences.get(audience_key, {})
        campaign_data["campaign_config"]["audience"] = {
            "key": audience_key,
            "name": audience.get("name", ""),
            "age_range": audience.get("age_range", ""),
            "demographics": audience.get("demographics", []),
            "psychographics": audience.get("psychographics", []),
            "messaging_preferences": audience.get("messaging_preferences", [])
        }

    # Generate filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"campaign_{timestamp}.json"
    filepath = outputs_dir / filename

    # Write JSON file
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(campaign_data, f, indent=2, ensure_ascii=False)

        return str(filepath)
    except Exception as e:
        return f"Error: {str(e)}"


def create_interface():
    """Create the Gradio interface."""

    with gr.Blocks(title="Creative Automation Pipeline") as app:
        gr.Markdown("# Creative Automation Pipeline")
        gr.Markdown("Automated creative asset generation for social ad campaigns using GenAI")

        # Tab navigation state
        with gr.Tabs() as tabs:
            # Campaign Configuration Tab
            with gr.Tab("🎯 Campaign", id="campaign"):
                # Top row with Load JSON and Campaign ID
                with gr.Row():
                    with gr.Column(scale=2):
                        gr.Markdown("## Campaign Configuration")
                        gr.Markdown("Configure your campaign target region/market and audience for creative generation.")
                    with gr.Column(scale=1):
                        load_json_file = gr.File(
                            label="📂 Load Campaign JSON",
                            file_types=[".json"],
                            type="filepath",
                            file_count="single"
                        )
                    with gr.Column(scale=1):
                        campaign_id_display = gr.Markdown(
                            value=f"### Campaign ID: `{generate_campaign_id()}`",
                            elem_classes=["campaign-id-display"]
                        )
                        regenerate_id_btn = gr.Button("🔄 New ID", variant="secondary", size="sm")

                load_status = gr.Markdown("")

                # Store campaign ID in state
                campaign_id_state = gr.State(value=generate_campaign_id())

                # Handler to regenerate campaign ID
                def regenerate_campaign_id():
                    new_id = generate_campaign_id()
                    return new_id, f"### Campaign ID: `{new_id}`"

                regenerate_id_btn.click(
                    fn=regenerate_campaign_id,
                    outputs=[campaign_id_state, campaign_id_display]
                )

                # Load JSON handler (will be wired up after all components are defined)
                # Placeholder for now

                with gr.Row():
                    with gr.Column():
                        gr.Markdown("### Target Region/Market")
                        region_dropdown = gr.Dropdown(
                            choices=get_region_choices(),
                            label="Select Region",
                            value=None,
                            interactive=True
                        )
                        region_info = gr.Markdown("")

                    with gr.Column():
                        gr.Markdown("### Target Audience")
                        audience_dropdown = gr.Dropdown(
                            choices=get_audience_choices(),
                            label="Select Audience",
                            value=None,
                            interactive=True
                        )
                        audience_info = gr.Markdown("")

                # World Map
                gr.Markdown("### Interactive World Map")

                world_map = gr.Plot(
                    value=create_world_map(),
                    show_label=False
                )

                # Function to display region details
                def display_region_info(region_key):
                    if not region_key:
                        return ""

                    regions = load_regions_config()
                    region = regions.get(region_key, {})

                    if not region:
                        return ""

                    info = f"**{region.get('name', '')}**\n\n"
                    info += f"*{region.get('description', '')}*\n\n"

                    if 'cultural_context' in region:
                        info += "**Cultural Context:**\n"
                        for item in region['cultural_context']:
                            info += f"- {item}\n"
                        info += "\n"

                    if 'visual_preferences' in region:
                        info += "**Visual Preferences:**\n"
                        for item in region['visual_preferences']:
                            info += f"- {item}\n"
                        info += "\n"

                    return info

                # Function to display audience details
                def display_audience_info(audience_key):
                    if not audience_key:
                        return ""

                    audiences = load_audiences_config()
                    audience = audiences.get(audience_key, {})

                    if not audience:
                        return ""

                    info = f"**{audience.get('name', '')}**\n\n"
                    info += f"*Age Range: {audience.get('age_range', '')}*\n\n"

                    if 'psychographics' in audience:
                        info += "**Psychographics:**\n"
                        for item in audience['psychographics']:
                            info += f"- {item}\n"
                        info += "\n"

                    if 'messaging_preferences' in audience:
                        info += "**Messaging Preferences:**\n"
                        for item in audience['messaging_preferences']:
                            info += f"- {item}\n"
                        info += "\n"

                    return info

                # Handler to update map when dropdown changes
                def update_map_from_dropdown(region_key):
                    return create_world_map(region_key)

                # Event handlers - Dropdown updates both map and info
                region_dropdown.change(
                    fn=display_region_info,
                    inputs=[region_dropdown],
                    outputs=[region_info]
                )

                region_dropdown.change(
                    fn=update_map_from_dropdown,
                    inputs=[region_dropdown],
                    outputs=[world_map]
                )

                audience_dropdown.change(
                    fn=display_audience_info,
                    inputs=[audience_dropdown],
                    outputs=[audience_info]
                )

                gr.Markdown("---")
                gr.Markdown("### Campaign Summary")
                campaign_summary = gr.Markdown("Region and audience selections will appear here...")

                def update_campaign_summary(region_key, audience_key):
                    if not region_key and not audience_key:
                        return "No region or audience selected yet."

                    regions = load_regions_config()
                    audiences = load_audiences_config()

                    summary = ""

                    # Region information
                    if region_key:
                        region = regions.get(region_key, {})
                        region_name = region.get('name', 'Not selected')
                        region_desc = region.get('description', '')

                        summary += f"**Target Region:** {region_name}\n"
                        if region_desc:
                            summary += f"*{region_desc}*\n\n"

                        if 'cultural_context' in region:
                            summary += "**Cultural Context:**\n"
                            for item in region['cultural_context'][:3]:  # First 3 items
                                summary += f"• {item}\n"
                            summary += "\n"

                        if 'visual_preferences' in region:
                            summary += "**Visual Preferences:**\n"
                            for item in region['visual_preferences'][:3]:  # First 3 items
                                summary += f"• {item}\n"
                            summary += "\n"
                    else:
                        summary += "**Target Region:** Not selected\n\n"

                    # Audience information
                    if audience_key:
                        audience = audiences.get(audience_key, {})
                        audience_name = audience.get('name', 'Not selected')
                        age_range = audience.get('age_range', '')

                        summary += f"**Target Audience:** {audience_name}"
                        if age_range:
                            summary += f" ({age_range})\n\n"
                        else:
                            summary += "\n\n"

                        if 'messaging_preferences' in audience:
                            summary += "**Messaging Preferences:**\n"
                            for item in audience['messaging_preferences'][:2]:  # First 2 items
                                summary += f"• {item}\n"
                    else:
                        summary += "**Target Audience:** Not selected"

                    return summary

                region_dropdown.change(
                    fn=update_campaign_summary,
                    inputs=[region_dropdown, audience_dropdown],
                    outputs=[campaign_summary]
                )

                audience_dropdown.change(
                    fn=update_campaign_summary,
                    inputs=[region_dropdown, audience_dropdown],
                    outputs=[campaign_summary]
                )

                # Button click handlers to select regions
                def select_region(region_key):
                    """Select a region and update all related components."""
                    info = display_region_info(region_key)
                    map_fig = create_world_map(region_key)
                    return region_key, map_fig, info

                # Note: Plotly map clicks are not directly supported in Gradio Plot components
                # Users should use the dropdown to select regions
                # The map updates automatically to highlight the selected region

                # Navigation
                gr.Markdown("---")
                with gr.Row():
                    gr.Markdown("")  # Spacer
                    next_to_messaging = gr.Button("Next: Messaging →", variant="primary", size="lg")

            # Messaging Tab
            with gr.Tab("💬 Messaging", id="messaging"):
                gr.Markdown("## Campaign Messaging")
                gr.Markdown("Create and refine your campaign messages and copy for the target audience.")

                with gr.Row():
                    campaign_message = gr.Textbox(
                        label="Campaign Message",
                        placeholder="Enter your campaign message here...\n\nExample: Discover the power of nature with our eco-friendly cleaning solution. Made with 100% plant-based ingredients, safe for your family and the planet.",
                        lines=10,
                        max_lines=20,
                        interactive=True,
                        show_copy_button=True,
                        scale=4
                    )
                    with gr.Column(scale=1):
                        randomize_message_btn = gr.Button("🎲 Randomize", variant="secondary", size="lg")
                        gr.Markdown("")  # Spacer

                with gr.Row():
                    char_count = gr.Markdown("**Character count:** 0")

                gr.Markdown("---")
                gr.Markdown("### Translate to Regional Languages")
                gr.Markdown("Translate your campaign message to the top 4 languages for your selected target region.")

                with gr.Row():
                    translate_btn = gr.Button("🌐 Translate Message", variant="primary", size="lg")

                translations_output = gr.Markdown("Translations will appear here...")

                # Character counter
                def count_characters(text):
                    if not text:
                        return "**Character count:** 0"
                    return f"**Character count:** {len(text)}"

                campaign_message.change(
                    fn=count_characters,
                    inputs=[campaign_message],
                    outputs=[char_count]
                )

                # Randomize message button handler
                randomize_message_btn.click(
                    fn=generate_random_campaign_message,
                    inputs=[],
                    outputs=[campaign_message]
                )

                # Translation button handler - will be connected after region_dropdown is created
                # (defined below in Campaign tab)

                # Navigation
                gr.Markdown("---")
                with gr.Row():
                    prev_to_campaign = gr.Button("← Previous: Campaign", variant="secondary", size="lg")
                    next_to_environments = gr.Button("Next: Environments →", variant="primary", size="lg")

            # Environments Tab
            with gr.Tab("🌄 Environments", id="environments"):
                gr.Markdown("## Background Environments")
                gr.Markdown("Generate professional background environments perfect for product placement.")

                # State to track selected environment images
                selected_env_state = gr.State([])

                with gr.Row():
                    environment_prompt = gr.Textbox(
                        label="Environment Description",
                        placeholder="Describe the environment you want to create...\n\nExample: Modern minimalist kitchen with marble countertops and natural sunlight",
                        lines=5,
                        max_lines=10,
                        interactive=True,
                        show_copy_button=True
                    )

                with gr.Row():
                    generate_env_btn = gr.Button("🎨 Generate Environments", variant="primary", size="lg", scale=4)
                    randomize_env_btn = gr.Button("🎲 Randomize", variant="secondary", size="lg", scale=1)

                environment_status = gr.Markdown("")

                gr.Markdown("### Generated Environments Preview")
                gr.Markdown("*Click on images to select them*")
                environment_gallery = gr.Gallery(
                    label="All Generated Environments",
                    show_label=True,
                    columns=2,
                    rows=2,
                    height="auto",
                    object_fit="contain"
                )

                gr.Markdown("---")
                gr.Markdown("### Selected Environments")
                gr.Markdown("Images you've selected for use in campaigns")

                selected_env_gallery = gr.Gallery(
                    label="Selected Images",
                    show_label=False,
                    columns=4,
                    rows=1,
                    height="auto",
                    object_fit="contain"
                )

                with gr.Row():
                    selected_env_display = gr.Markdown("**Selected:** None")
                    clear_env_selection_btn = gr.Button("Clear Selection", size="sm", variant="secondary")

                # Generate environments handler
                generate_env_btn.click(
                    fn=generate_environments,
                    inputs=[environment_prompt, campaign_id_state],
                    outputs=[environment_status, environment_gallery]
                )

                # Randomize prompt handler
                randomize_env_btn.click(
                    fn=generate_random_environment,
                    inputs=[],
                    outputs=[environment_prompt]
                )

                # Selection handlers
                def select_environment(evt: gr.SelectData, selected_list):
                    """Handle environment image selection."""
                    if evt.value:
                        image_path = evt.value['image']['path'] if isinstance(evt.value, dict) else evt.value

                        # Toggle selection
                        if image_path in selected_list:
                            selected_list.remove(image_path)
                        else:
                            selected_list.append(image_path)

                        if selected_list:
                            display = f"**Selected:** {len(selected_list)} image(s)"
                        else:
                            display = "**Selected:** None"

                        return selected_list, selected_list, display
                    return selected_list, selected_list, "**Selected:** None"

                def clear_env_selection():
                    """Clear environment selection."""
                    return [], [], "**Selected:** None"

                environment_gallery.select(
                    fn=select_environment,
                    inputs=[selected_env_state],
                    outputs=[selected_env_state, selected_env_gallery, selected_env_display]
                )

                clear_env_selection_btn.click(
                    fn=clear_env_selection,
                    inputs=[],
                    outputs=[selected_env_state, selected_env_gallery, selected_env_display]
                )

                # Navigation
                gr.Markdown("---")
                with gr.Row():
                    prev_to_messaging = gr.Button("← Previous: Messaging", variant="secondary", size="lg")
                    next_to_products = gr.Button("Next: Products →", variant="primary", size="lg")

            # Products Tab
            with gr.Tab("📦 Products", id="products"):
                gr.Markdown("## Product Assets Preview & Generation")
                gr.Markdown("Select one or more products to preview assets and generate product views.")

                # State to track selected product images
                selected_product_state = gr.State([])

                with gr.Row():
                    product_dropdown = gr.Dropdown(
                        choices=get_available_products(),
                        label="Select Products (Multi-select enabled)",
                        value=None,
                        interactive=True,
                        multiselect=True
                    )

                gr.Markdown("### Product Photos")
                product_gallery = gr.Gallery(
                    label="Product Photos",
                    show_label=False,
                    columns=4,
                    rows=2,
                    height="auto",
                    object_fit="contain"
                )

                # Event handler for product selection - will be connected after logo tab is created
                # (defined below after logo_product_dropdown and logo_gallery are created)

                gr.Markdown("---")
                gr.Markdown("## Generate Product Views")
                gr.Markdown("Generate all 6 product views (front, back, left, right, top-down, bottom-up) using AI. The model will use the existing product photos as reference to synthesize new views while maintaining consistent appearance, colors, and branding.")

                with gr.Row():
                    generation_mode = gr.Radio(
                        choices=[
                            ("Separate - Generate individual views for each product", "separate"),
                            ("Combined - Generate views with all products together", "combined")
                        ],
                        label="Generation Mode",
                        value="separate",
                        info="Choose whether to generate separate images for each product or combine all products in single images"
                    )

                with gr.Row():
                    generate_btn = gr.Button("🎨 Generate All Product Views", variant="primary", size="lg")

                generation_status = gr.Markdown("")

                gr.Markdown("### Generated Product Views Preview")
                gr.Markdown("*Click on images to select them*")
                generated_gallery = gr.Gallery(
                    label="All Generated Product Views",
                    show_label=True,
                    columns=3,
                    rows=2,
                    height="auto",
                    object_fit="contain"
                )

                gr.Markdown("---")
                gr.Markdown("### Selected Product Views")
                gr.Markdown("Images you've selected for use in campaigns")

                selected_product_gallery = gr.Gallery(
                    label="Selected Images",
                    show_label=False,
                    columns=4,
                    rows=1,
                    height="auto",
                    object_fit="contain"
                )

                with gr.Row():
                    selected_product_display = gr.Markdown("**Selected:** None")
                    clear_product_selection_btn = gr.Button("Clear Selection", size="sm", variant="secondary")

                # Generate button handler
                generate_btn.click(
                    fn=generate_product_views,
                    inputs=[product_dropdown, generation_mode, campaign_id_state],
                    outputs=[generation_status, generated_gallery]
                )

                # Selection handlers
                def select_product_image(evt: gr.SelectData, selected_list):
                    """Handle product image selection."""
                    if evt.value:
                        image_path = evt.value['image']['path'] if isinstance(evt.value, dict) else evt.value

                        # Toggle selection
                        if image_path in selected_list:
                            selected_list.remove(image_path)
                        else:
                            selected_list.append(image_path)

                        if selected_list:
                            display = f"**Selected:** {len(selected_list)} image(s)"
                        else:
                            display = "**Selected:** None"

                        return selected_list, selected_list, display
                    return selected_list, selected_list, "**Selected:** None"

                def clear_product_selection():
                    """Clear product image selection."""
                    return [], [], "**Selected:** None"

                generated_gallery.select(
                    fn=select_product_image,
                    inputs=[selected_product_state],
                    outputs=[selected_product_state, selected_product_gallery, selected_product_display]
                )

                clear_product_selection_btn.click(
                    fn=clear_product_selection,
                    inputs=[],
                    outputs=[selected_product_state, selected_product_gallery, selected_product_display]
                )

                # Navigation
                gr.Markdown("---")
                with gr.Row():
                    prev_to_environments = gr.Button("← Previous: Environments", variant="secondary", size="lg")
                    next_to_logos = gr.Button("Next: Logos →", variant="primary", size="lg")

            # Logos Tab
            with gr.Tab("🏷️ Logos", id="logos"):
                gr.Markdown("## Logo Assets")
                gr.Markdown("View and manage logo assets for your products.")

                # State to track selected logos
                selected_logo_state = gr.State([])

                with gr.Row():
                    logo_product_dropdown = gr.Dropdown(
                        choices=get_available_products(),
                        label="Select Products (Multi-select enabled)",
                        value=None,
                        interactive=True,
                        multiselect=True
                    )

                gr.Markdown("### Logo Assets Preview")
                gr.Markdown("*Click on logos to select them*")
                logo_gallery = gr.Gallery(
                    label="All Logo Assets",
                    show_label=True,
                    columns=4,
                    rows=2,
                    height="auto",
                    object_fit="contain"
                )

                gr.Markdown("---")
                gr.Markdown("### Selected Logos")
                gr.Markdown("Logos you've selected for use in campaigns")

                selected_logo_gallery = gr.Gallery(
                    label="Selected Logos",
                    show_label=False,
                    columns=4,
                    rows=1,
                    height="auto",
                    object_fit="contain"
                )

                with gr.Row():
                    selected_logo_display = gr.Markdown("**Selected:** None")
                    clear_logo_selection_btn = gr.Button("Clear Selection", size="sm", variant="secondary")

                # Event handler for logo product selection
                logo_product_dropdown.change(
                    fn=lambda slugs: load_product(slugs)[1],
                    inputs=[logo_product_dropdown],
                    outputs=[logo_gallery]
                )

                # Logo selection handlers
                def select_logo(evt: gr.SelectData, selected_list):
                    """Handle logo selection."""
                    if evt.value:
                        image_path = evt.value['image']['path'] if isinstance(evt.value, dict) else evt.value

                        # Toggle selection
                        if image_path in selected_list:
                            selected_list.remove(image_path)
                        else:
                            selected_list.append(image_path)

                        if selected_list:
                            display = f"**Selected:** {len(selected_list)} logo(s)"
                        else:
                            display = "**Selected:** None"

                        return selected_list, selected_list, display
                    return selected_list, selected_list, "**Selected:** None"

                def clear_logo_selection():
                    """Clear logo selection."""
                    return [], [], "**Selected:** None"

                logo_gallery.select(
                    fn=select_logo,
                    inputs=[selected_logo_state],
                    outputs=[selected_logo_state, selected_logo_gallery, selected_logo_display]
                )

                clear_logo_selection_btn.click(
                    fn=clear_logo_selection,
                    inputs=[],
                    outputs=[selected_logo_state, selected_logo_gallery, selected_logo_display]
                )

                # Navigation
                gr.Markdown("---")
                with gr.Row():
                    prev_to_products = gr.Button("← Previous: Products", variant="secondary", size="lg")
                    next_to_preview = gr.Button("Next: Preview →", variant="primary", size="lg")

            # Connect event handlers across tabs
            # When products are selected in Products tab, auto-populate logos tab
            def sync_product_selection(slugs):
                """Load product photos and sync logo tab with same selection."""
                photos, logos = load_product(slugs)
                return photos, slugs, logos

            product_dropdown.change(
                fn=sync_product_selection,
                inputs=[product_dropdown],
                outputs=[product_gallery, logo_product_dropdown, logo_gallery]
            )

            # Connect translation button to region selection from Campaign tab
            translate_btn.click(
                fn=translate_message,
                inputs=[campaign_message, region_dropdown],
                outputs=[translations_output]
            )

            # Preview Tab
            with gr.Tab("👁️ Preview", id="preview"):
                gr.Markdown("# Campaign Preview")
                gr.Markdown("Complete overview of your campaign configuration and selected assets.")

                with gr.Row():
                    refresh_preview_btn = gr.Button("🔄 Refresh Preview", variant="primary", size="lg")

                gr.Markdown("---")

                # Campaign Configuration Section
                gr.Markdown("## 📊 Campaign Configuration")
                preview_campaign_summary = gr.Markdown("*Select region and audience in Campaign tab*")

                gr.Markdown("---")

                # Messaging Section
                gr.Markdown("## 💬 Campaign Messaging")
                preview_message = gr.Markdown("*Enter campaign message in Messaging tab*")

                gr.Markdown("### Translations")
                preview_translations = gr.Markdown("*Click Translate in Messaging tab to see translations*")

                gr.Markdown("---")

                # Selected Assets Section
                with gr.Row():
                    with gr.Column():
                        gr.Markdown("## 🌄 Selected Environments")
                        preview_env_gallery = gr.Gallery(
                            label="Environment Backgrounds",
                            show_label=False,
                            columns=2,
                            rows=2,
                            height="auto",
                            object_fit="contain"
                        )
                        preview_env_count = gr.Markdown("*No environments selected*")

                    with gr.Column():
                        gr.Markdown("## 📦 Selected Product Views")
                        preview_product_gallery = gr.Gallery(
                            label="Product Photos",
                            show_label=False,
                            columns=2,
                            rows=2,
                            height="auto",
                            object_fit="contain"
                        )
                        preview_product_count = gr.Markdown("*No product views selected*")

                gr.Markdown("---")

                # Selected Logos Section
                gr.Markdown("## 🏷️ Selected Logos")
                preview_logo_gallery = gr.Gallery(
                    label="Logo Assets",
                    show_label=False,
                    columns=4,
                    rows=1,
                    height="auto",
                    object_fit="contain"
                )
                preview_logo_count = gr.Markdown("*No logos selected*")

                # Refresh preview function
                def refresh_preview(region_key, audience_key, message, translations, selected_envs, selected_products, selected_logos):
                    """Refresh the preview with current selections."""

                    # Build campaign summary
                    campaign_summary = ""
                    if region_key or audience_key:
                        regions = load_regions_config()
                        audiences = load_audiences_config()

                        if region_key:
                            region = regions.get(region_key, {})
                            region_name = region.get('name', 'Not selected')
                            region_desc = region.get('description', '')
                            campaign_summary += f"**Target Region:** {region_name}\n"
                            if region_desc:
                                campaign_summary += f"*{region_desc}*\n\n"

                        if audience_key:
                            audience = audiences.get(audience_key, {})
                            audience_name = audience.get('name', 'Not selected')
                            age_range = audience.get('age_range', '')
                            campaign_summary += f"**Target Audience:** {audience_name}"
                            if age_range:
                                campaign_summary += f" ({age_range})"
                            campaign_summary += "\n"
                    else:
                        campaign_summary = "*Select region and audience in Campaign tab*"

                    # Format message
                    message_display = message if message and message.strip() else "*Enter campaign message in Messaging tab*"
                    message_display = f"**Original Message:**\n\n{message_display}"

                    # Format translations
                    translations_display = translations if translations and "Translations for" in translations else "*Click Translate in Messaging tab to see translations*"

                    # Environment count
                    env_count = f"**{len(selected_envs)} environment(s) selected**" if selected_envs else "*No environments selected*"

                    # Product count
                    product_count = f"**{len(selected_products)} product view(s) selected**" if selected_products else "*No product views selected*"

                    # Logo count
                    logo_count = f"**{len(selected_logos)} logo(s) selected**" if selected_logos else "*No logos selected*"

                    return campaign_summary, message_display, translations_display, selected_envs, env_count, selected_products, product_count, selected_logos, logo_count

                # Connect refresh button
                refresh_preview_btn.click(
                    fn=refresh_preview,
                    inputs=[region_dropdown, audience_dropdown, campaign_message, translations_output, selected_env_state, selected_product_state, selected_logo_state],
                    outputs=[preview_campaign_summary, preview_message, preview_translations, preview_env_gallery, preview_env_count, preview_product_gallery, preview_product_count, preview_logo_gallery, preview_logo_count]
                )

                # Navigation
                gr.Markdown("---")
                with gr.Row():
                    prev_to_logos = gr.Button("← Previous: Logos", variant="secondary", size="lg")
                    next_to_generate = gr.Button("Next: Generate →", variant="primary", size="lg")

            # Generate Tab
            with gr.Tab("🎨 Generate", id="generate"):
                gr.Markdown("# Generate Campaign Ads")

                # Dynamic campaign preview
                generate_campaign_preview = gr.Markdown("Loading campaign details...")

                with gr.Row():
                    generate_ads_btn = gr.Button("🚀 Generate All Ad Formats", variant="primary", size="lg")

                generation_status_ads = gr.Markdown("")

                gr.Markdown("---")

                # Ad Preview Layouts
                with gr.Row():
                    # 1:1 Square Format
                    with gr.Column(scale=1):
                        gr.Markdown("## 1:1 Square Ad")
                        gr.Markdown("*Perfect for Instagram feed, Facebook posts*")
                        gr.Markdown("*Uses campaign message from Messaging tab*")

                        with gr.Row():
                            include_logo_1_1 = gr.Checkbox(
                                label="Include Logo",
                                value=False,
                                interactive=True
                            )
                            generate_localizations_1_1 = gr.Checkbox(
                                label="Generate Localizations",
                                value=False,
                                interactive=True,
                                info="Generate versions in all regional languages"
                            )

                        preview_1_1 = gr.Gallery(
                            label="1:1 Preview (1080x1080)",
                            show_label=True,
                            columns=3,
                            rows=2,
                            height=400,
                            interactive=False
                        )

                    # 9:16 Story/Vertical Format
                    with gr.Column(scale=1):
                        gr.Markdown("## 9:16 Story Ad")
                        gr.Markdown("*Perfect for Instagram Stories, TikTok, Reels*")
                        gr.Markdown("*Uses campaign message from Messaging tab*")

                        with gr.Row():
                            include_logo_9_16 = gr.Checkbox(
                                label="Include Logo",
                                value=False,
                                interactive=True
                            )
                            generate_localizations_9_16 = gr.Checkbox(
                                label="Generate Localizations",
                                value=False,
                                interactive=True,
                                info="Generate versions in all regional languages"
                            )

                        preview_9_16 = gr.Gallery(
                            label="9:16 Preview (1080x1920)",
                            show_label=True,
                            columns=3,
                            rows=2,
                            height=600,
                            interactive=False
                        )

                    # 16:9 Landscape Format
                    with gr.Column(scale=1):
                        gr.Markdown("## 16:9 Landscape Ad")
                        gr.Markdown("*Perfect for YouTube, desktop ads, banners*")
                        gr.Markdown("*Uses campaign message from Messaging tab*")

                        with gr.Row():
                            include_logo_16_9 = gr.Checkbox(
                                label="Include Logo",
                                value=False,
                                interactive=True
                            )
                            generate_localizations_16_9 = gr.Checkbox(
                                label="Generate Localizations",
                                value=False,
                                interactive=True,
                                info="Generate versions in all regional languages"
                            )

                        preview_16_9 = gr.Gallery(
                            label="16:9 Preview (1920x1080)",
                            show_label=True,
                            columns=3,
                            rows=2,
                            height=400,
                            interactive=False
                        )

                gr.Markdown("---")
                gr.Markdown("### 📄 Campaign Configuration JSON")
                gr.Markdown("Complete campaign configuration with all settings and translations:")

                campaign_json_display = gr.Code(
                    label="Campaign Configuration",
                    language="json",
                    value="",
                    interactive=False,
                    lines=20
                )

                # Connect generation button
                generate_ads_btn.click(
                    fn=generate_ad_compositions,
                    inputs=[selected_env_state, selected_product_state, campaign_message, selected_logo_state, include_logo_1_1, include_logo_9_16, include_logo_16_9, region_dropdown, audience_dropdown, generate_localizations_1_1, generate_localizations_9_16, generate_localizations_16_9, campaign_id_state],
                    outputs=[generation_status_ads, preview_1_1, preview_9_16, preview_16_9, campaign_json_display]
                )

                # Navigation
                gr.Markdown("---")
                with gr.Row():
                    prev_to_preview = gr.Button("← Previous: Preview", variant="secondary", size="lg")
                    next_to_settings = gr.Button("Next: Settings →", variant="primary", size="lg")

            # Settings Tab
            with gr.Tab("⚙️ Settings", id="settings"):
                gr.Markdown("## API Configuration")
                gr.Markdown("Configure your Google Gemini API key for image generation.")

                with gr.Row():
                    with gr.Column(scale=3):
                        api_key_input = gr.Textbox(
                            label="Google Gemini API Key",
                            placeholder="Enter your API key from https://ai.google.dev",
                            type="password",
                            value=os.getenv("GOOGLE_API_KEY", ""),
                        )
                    with gr.Column(scale=1):
                        save_key_btn = gr.Button("💾 Save API Key", variant="primary", size="lg")

                api_status = gr.Markdown(value=get_api_key_status())

                gr.Markdown("---")
                gr.Markdown("### How to get your API key:")
                gr.Markdown(
                    """
1. Visit [Google AI Studio](https://ai.google.dev/gemini-api/docs/api-key)
2. Sign in with your Google account
3. Click "Get API key" or "Create API key"
4. Copy the key and paste it above
5. Click "Save API Key" to store it
                    """
                )

                # Save API key handler
                save_key_btn.click(
                    fn=save_api_key,
                    inputs=[api_key_input],
                    outputs=[api_status]
                )

                # Navigation
                gr.Markdown("---")
                with gr.Row():
                    prev_to_generate = gr.Button("← Previous: Generate", variant="secondary", size="lg")
                    gr.Markdown("")  # Spacer

        # Wire up navigation buttons to switch tabs
        next_to_messaging.click(fn=lambda: gr.update(selected="messaging"), inputs=None, outputs=tabs)
        prev_to_campaign.click(fn=lambda: gr.update(selected="campaign"), inputs=None, outputs=tabs)
        next_to_environments.click(fn=lambda: gr.update(selected="environments"), inputs=None, outputs=tabs)
        prev_to_messaging.click(fn=lambda: gr.update(selected="messaging"), inputs=None, outputs=tabs)
        next_to_products.click(fn=lambda: gr.update(selected="products"), inputs=None, outputs=tabs)
        prev_to_environments.click(fn=lambda: gr.update(selected="environments"), inputs=None, outputs=tabs)
        next_to_logos.click(fn=lambda: gr.update(selected="logos"), inputs=None, outputs=tabs)
        prev_to_products.click(fn=lambda: gr.update(selected="products"), inputs=None, outputs=tabs)
        next_to_preview.click(fn=lambda: gr.update(selected="preview"), inputs=None, outputs=tabs)
        prev_to_logos.click(fn=lambda: gr.update(selected="logos"), inputs=None, outputs=tabs)
        next_to_generate.click(fn=lambda: gr.update(selected="generate"), inputs=None, outputs=tabs)
        prev_to_preview.click(fn=lambda: gr.update(selected="preview"), inputs=None, outputs=tabs)
        next_to_settings.click(fn=lambda: gr.update(selected="settings"), inputs=None, outputs=tabs)
        prev_to_generate.click(fn=lambda: gr.update(selected="generate"), inputs=None, outputs=tabs)

        # Wire up Load JSON handler with auto-preview
        def load_and_preview(json_path):
            """Load campaign JSON, populate fields, and switch to preview tab."""
            # Load the JSON
            region_key, audience_key, message, status, environments, products = load_campaign_from_json(json_path)

            # Call refresh_preview to get preview outputs
            preview_outputs = refresh_preview(
                region_key,
                audience_key,
                message,
                "",  # translations (will be empty initially)
                environments,
                products,
                []  # logos
            )

            # Build generate preview
            generate_preview = build_generate_preview(region_key, audience_key, message)

            # Return all outputs including tab switch
            return (
                region_key,           # region_dropdown
                audience_key,         # audience_dropdown
                message,              # campaign_message
                status,               # load_status
                environments,         # selected_env_state
                products,             # selected_product_state
                gr.update(selected="preview"),  # tabs (switch to preview)
                generate_preview,     # generate_campaign_preview
                *preview_outputs      # all preview outputs
            )

        load_json_file.change(
            fn=load_and_preview,
            inputs=[load_json_file],
            outputs=[
                region_dropdown,
                audience_dropdown,
                campaign_message,
                load_status,
                selected_env_state,
                selected_product_state,
                tabs,  # Switch to preview tab
                generate_campaign_preview,  # Update generate tab preview
                preview_campaign_summary,
                preview_message,
                preview_translations,
                preview_env_gallery,
                preview_env_count,
                preview_product_gallery,
                preview_product_count,
                preview_logo_gallery,
                preview_logo_count
            ]
        )

        # Update Generate tab preview when campaign settings change
        def update_generate_preview_wrapper(region_key, audience_key, message):
            """Wrapper to update generate preview."""
            return build_generate_preview(region_key, audience_key, message)

        # Wire up updates to generate preview
        region_dropdown.change(
            fn=update_generate_preview_wrapper,
            inputs=[region_dropdown, audience_dropdown, campaign_message],
            outputs=[generate_campaign_preview]
        )

        audience_dropdown.change(
            fn=update_generate_preview_wrapper,
            inputs=[region_dropdown, audience_dropdown, campaign_message],
            outputs=[generate_campaign_preview]
        )

        campaign_message.change(
            fn=update_generate_preview_wrapper,
            inputs=[region_dropdown, audience_dropdown, campaign_message],
            outputs=[generate_campaign_preview]
        )

    return app


if __name__ == "__main__":
    app = create_interface()
    # Use PORT environment variable if available, otherwise default to 7860
    port = int(os.environ.get("PORT", 7860))
    app.launch(server_name="0.0.0.0", server_port=port)
