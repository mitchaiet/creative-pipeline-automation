# Development Guide

Guide for developers who want to contribute to, extend, or customize the Creative Automation Pipeline.

---

## Table of Contents

1. [Development Setup](#development-setup)
2. [Project Architecture](#project-architecture)
3. [Adding New Features](#adding-new-features)
4. [Testing](#testing)
5. [Code Style](#code-style)
6. [Contributing](#contributing)
7. [Deployment](#deployment)
8. [Roadmap](#roadmap)

---

## Development Setup

### Prerequisites

- **Python 3.12+** installed
- **Git** for version control
- **uv** package manager (recommended) or pip
- **Google Gemini API key** (required for testing)
- **Code editor** (VS Code, PyCharm, etc.)

### Clone Repository

```bash
git clone https://github.com/mitchaiet/creative-pipeline-automation.git
cd creative-pipeline-automation
```

### Install Dependencies

**Option A: Using uv (recommended)**
```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install project dependencies
uv sync
```

**Option B: Using pip**
```bash
pip install -r requirements.txt
```

### Configure Environment

1. **Copy environment template**:
```bash
cp .env.example .env
```

2. **Add your API key**:
```bash
# Edit .env
GOOGLE_API_KEY=your_gemini_api_key_here
```

3. **Verify configuration**:
```bash
cat .env
```

### Run Application

```bash
# Using uv
uv run python src/app.py

# Using standard python
python src/app.py
```

Application starts at `http://localhost:7860`

---

## Project Architecture

### Single-File Design

The application uses a **single-file architecture** (`app.py`) for simplicity:

**Benefits**:
- Easy to understand and navigate
- No complex module imports
- Straightforward deployment
- Fast iteration

**Structure** (5000+ lines):
1. Imports & setup
2. Helper functions
3. Configuration loaders
4. Generation functions
5. UI components
6. Event handlers
7. App launch

### Key Design Patterns

#### State Management
```python
# Gradio State objects persist data across tabs
campaign_id_state = gr.State()
selected_env_state = gr.State([])
selected_product_state = gr.State([])
```

#### Event-Driven UI
```python
# Button clicks trigger functions
generate_btn.click(
    fn=generate_environments,
    inputs=[environment_prompt, campaign_id_state],
    outputs=[environment_status, environment_gallery]
)
```

#### Progressive Disclosure
```python
# 7-tab workflow guides users step-by-step
with gr.Tabs() as tabs:
    with gr.Tab("Campaign"):
        # Campaign config
    with gr.Tab("Messaging"):
        # Message creation
    # ... etc
```

---

## Adding New Features

### Adding a New Product

**Steps**:

1. **Create product folder**:
```bash
mkdir -p products/new-product-name/photos/{product,logo,generated}
```

2. **Create config.yaml**:
```yaml
# products/new-product-name/config.yaml
product:
  name: "Product Display Name"
  description: "Detailed product description for AI prompts"
  category: "Product Category"

company:
  name: "Company Name"
  tagline: "Optional company tagline"
```

3. **Add reference photos**:
```bash
# Copy product photos (at least 1 required)
cp your-photos/* products/new-product-name/photos/product/
```

4. **Add logo** (optional):
```bash
cp your-logo.png products/new-product-name/photos/logo/
```

5. **Restart app** - Product automatically appears in dropdown

**Naming convention**:
- Use lowercase with hyphens: `new-product-name`
- Avoid spaces or special characters

### Adding a New Region

**Steps**:

1. **Edit config/regions.yaml**:
```yaml
new_region_key:
  name: "Region Display Name"
  description: "Brief description"
  countries: ["Country1", "Country2", "Country3"]
  cultural_context:
    - "Cultural insight 1"
    - "Cultural insight 2"
  visual_preferences:
    colors: ["Color palette 1", "Color palette 2"]
    imagery: ["Image style 1", "Image style 2"]
  messaging:
    tone: ["Tone 1", "Tone 2"]
    themes: ["Theme 1", "Theme 2"]
  top_languages:
    - code: "en"
      name: "English"
    - code: "es"
      name: "Spanish"
    - code: "fr"
      name: "French"
    - code: "de"
      name: "German"
```

2. **Update world map** (in app.py):

Find the `create_world_map()` function and update country mappings:

```python
# Map countries to regions
region_map = {
    'USA': 'north_america',
    'Canada': 'north_america',
    # Add your new countries here
    'NewCountry1': 'new_region_key',
    'NewCountry2': 'new_region_key',
}
```

3. **Restart app** - Region appears in dropdown and map

### Adding a New Audience

**Steps**:

1. **Edit config/audiences.yaml**:
```yaml
new_audience_key:
  name: "Audience Display Name"
  demographics:
    age_range: "25-40"
    characteristics:
      - "Characteristic 1"
      - "Characteristic 2"
      - "Characteristic 3"
  messaging_preferences:
    tone: ["Tone 1", "Tone 2"]
    themes: ["Theme 1", "Theme 2"]
    key_values: ["Value 1", "Value 2"]
  visual_preferences:
    colors: ["Color 1", "Color 2"]
    imagery: ["Style 1", "Style 2"]
```

2. **Restart app** - Audience appears in dropdown

### Adding Environment Presets

**Edit the preset list in app.py**:

Find `ENVIRONMENT_PRESETS` around line 100:

```python
ENVIRONMENT_PRESETS = [
    "Modern minimalist kitchen with natural light",
    "Cozy living room with fireplace",
    # Add your new presets here
    "Your new environment description",
    "Another preset environment",
]
```

### Adding Sample Messages

**Edit the sample list in app.py**:

Find `SAMPLE_MESSAGES` around line 150:

```python
SAMPLE_MESSAGES = [
    "Transform your wellness routine with natural ingredients",
    "Experience the difference quality makes",
    # Add your new messages here
    "Your new campaign message",
    "Another sample message",
]
```

---

## Testing

### Manual Testing

**Test generation pipeline**:

1. **Environment generation**:
```bash
# Run app
uv run python src/app.py

# In UI:
# 1. Go to Environments tab
# 2. Enter prompt or use randomize
# 3. Click Generate
# 4. Verify 4 images appear
# 5. Check outputs/{CAMPAIGN_ID}/environments/
```

2. **Product generation**:
```bash
# In UI:
# 1. Go to Products tab
# 2. Select 1-2 products
# 3. Choose Separate or Combined mode
# 4. Click Generate
# 5. Verify images appear
# 6. Check outputs/{CAMPAIGN_ID}/products/
```

3. **Ad generation**:
```bash
# In UI:
# 1. Complete all tabs (Campaign → Messaging → Environments → Products)
# 2. Go to Generate tab
# 3. Configure options
# 4. Click Generate
# 5. Verify ads appear in 3 aspect ratios
# 6. Check outputs/{CAMPAIGN_ID}/ads/
```

### API Testing

**Test Gemini API connection**:

```python
# Quick test script
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=api_key)

response = client.models.generate_images(
    model='gemini-2.5-flash-image',
    prompt="A modern minimalist kitchen",
    config={'numberOfImages': 1, 'aspectRatio': '1:1'}
)

print("API test successful!" if response.images else "API test failed")
```

### Configuration Testing

**Test YAML parsing**:

```python
import yaml
from pathlib import Path

# Test regions
with open('config/regions.yaml') as f:
    regions = yaml.safe_load(f)
    print(f"Loaded {len(regions)} regions")

# Test audiences
with open('config/audiences.yaml') as f:
    audiences = yaml.safe_load(f)
    print(f"Loaded {len(audiences)} audiences")

# Test product configs
for product_dir in Path('products').iterdir():
    if product_dir.is_dir():
        config_file = product_dir / 'config.yaml'
        if config_file.exists():
            with open(config_file) as f:
                config = yaml.safe_load(f)
                print(f"✓ {product_dir.name}: {config['product']['name']}")
```

### Automated Testing

Currently no automated test suite. Future additions:
- Unit tests for helper functions
- Integration tests for generation pipeline
- UI tests with Gradio testing framework

---

## Code Style

### Python Style Guide

Follow **PEP 8** with these specifics:

**Indentation**: 4 spaces (no tabs)
```python
def example_function():
    if condition:
        do_something()
```

**Line length**: 100 characters (soft limit)
```python
# Good
message = "Short line"

# Acceptable
long_message = (
    "This is a longer message that exceeds "
    "the line limit so we break it up"
)
```

**Naming conventions**:
- Functions: `snake_case`
- Variables: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Classes: `PascalCase` (if added)

**Imports**: Grouped and sorted
```python
# Standard library
import os
from pathlib import Path
from datetime import datetime

# Third-party
import gradio as gr
import yaml
from google import genai

# Local (if applicable)
from helpers import utility_function
```

### Documentation

**Function docstrings**:
```python
def generate_environments(prompt: str, campaign_id: str, progress=gr.Progress()) -> Tuple[str, List[str]]:
    """Generate 4 background environment images using Gemini.

    Args:
        prompt: Text description of desired environment
        campaign_id: 6-character campaign identifier
        progress: Gradio progress tracker

    Returns:
        Tuple of (status_message, list_of_image_paths)
    """
    # Function implementation
```

**Inline comments**: Explain "why", not "what"
```python
# Good
# Use timestamp to avoid overwriting previous generations
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Bad
# Create timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
```

---

## Contributing

### Contribution Workflow

1. **Fork the repository**
2. **Create a feature branch**:
```bash
git checkout -b feature/amazing-feature
```

3. **Make your changes**:
- Follow code style guide
- Add comments for complex logic
- Test your changes manually

4. **Commit your changes**:
```bash
git add .
git commit -m "Add amazing feature: description of what it does"
```

5. **Push to your fork**:
```bash
git push origin feature/amazing-feature
```

6. **Open a Pull Request**:
- Describe what the PR does
- Include screenshots for UI changes
- Reference any related issues

### Commit Message Format

Use clear, descriptive commit messages:

**Format**: `<type>: <description>`

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style/formatting
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples**:
```bash
git commit -m "feat: Add support for custom aspect ratios"
git commit -m "fix: Resolve issue with campaign JSON loading"
git commit -m "docs: Update README with new deployment instructions"
```

### Pull Request Guidelines

**Good PR**:
- Clear title and description
- One feature/fix per PR
- Tested manually
- Screenshots for UI changes
- No unrelated changes

**PR template**:
```markdown
## Description
Brief description of changes

## Changes Made
- Change 1
- Change 2

## Testing
How to test these changes

## Screenshots (if applicable)
[Add screenshots]
```

---

## Deployment

### Local Development

```bash
# Run with hot reload (if using --reload flag)
uv run python src/app.py

# Access at
http://localhost:7860
```

### Docker Deployment (Future)

Not currently implemented. Would require:
- `Dockerfile`
- `docker-compose.yml`
- Environment variable configuration

---

## Roadmap

### Completed Features 

- [x] Campaign configuration (regions/audiences)
- [x] Interactive world map
- [x] Multi-product selection
- [x] Environment generation
- [x] Product view generation (6 angles)
- [x] Multi-aspect ratio ads (1:1, 9:16, 16:9)
- [x] Logo integration
- [x] Localization support
- [x] Campaign preview & JSON export
- [x] Self-contained campaign folders
- [x] Outputs browser
- [x] Campaign JSON loading with auto-preview

### Planned Features 

#### Short Term
- [ ] Batch generation across product/environment matrices
- [ ] Advanced text overlay controls (font, size, position)
- [ ] Logo positioning controls (corner selection, size)
- [ ] Custom aspect ratios
- [ ] Image quality settings

#### Medium Term
- [ ] A/B testing variant generation
- [ ] Campaign performance tracking integration
- [ ] Video/animation support
- [ ] Custom brand style guides
- [ ] Automated testing suite
- [ ] API rate limiting UI

#### Long Term
- [ ] Multi-user support with authentication
- [ ] Database integration for campaign storage
- [ ] Real-time collaboration features
- [ ] Integration with social media platforms
- [ ] Analytics dashboard
- [ ] Mobile app

### Feature Requests

To request a feature:
1. Open an issue on GitHub
2. Use "Feature Request" template
3. Describe use case and benefits
4. Community votes with 👍 reactions

---

## Extension Points

### Custom Generation Models

To use a different AI model:

1. **Replace API client**:
```python
# Instead of google-genai
from custom_ai_sdk import CustomClient

client = CustomClient(api_key=api_key)
```

2. **Update generation functions**:
```python
def generate_environments(prompt, campaign_id):
    # Replace Gemini API call
    response = client.generate(
        prompt=prompt,
        # Model-specific parameters
    )
    return response.images
```

### Custom UI Themes

Gradio supports custom CSS:

```python
# In app launch section
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    # UI components
    pass

# Or custom CSS
demo.launch(css="""
    .gradio-container {
        background-color: #f0f0f0;
    }
""")
```

### Database Integration

To persist campaigns in a database:

1. **Choose database** (PostgreSQL, SQLite, MongoDB)
2. **Add dependency**: `psycopg2`, `sqlite3`, `pymongo`
3. **Create schema**:
```sql
CREATE TABLE campaigns (
    id VARCHAR(6) PRIMARY KEY,
    created_at TIMESTAMP,
    config JSONB,
    -- other fields
);
```

4. **Replace file-based storage**:
```python
# Instead of JSON files
def save_campaign_config(campaign_data):
    db.campaigns.insert_one(campaign_data)
```

---

## Debugging

### Enable Debug Mode

```python
# In app.py, at launch
demo.launch(
    debug=True,  # Enable debug mode
    server_port=7860
)
```

**Debug mode provides**:
- Detailed error messages
- Stack traces in UI
- Hot reload on code changes

### Logging

Add logging for troubleshooting:

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def generate_environments(prompt, campaign_id):
    logger.debug(f"Generating environments for campaign {campaign_id}")
    logger.debug(f"Prompt: {prompt}")
    # Function logic
```

### Common Issues

**API key not found**:
```python
# Check .env loading
from dotenv import load_dotenv
load_dotenv()
print(os.getenv("GOOGLE_API_KEY"))  # Should print your key
```

**Import errors**:
```bash
# Reinstall dependencies
uv sync --force
```

**Port conflicts**:
```python
# Change port
demo.launch(server_port=7861)
```

---

## Best Practices

### Code Organization

1. **Keep functions focused**: One function, one responsibility
2. **Use type hints**: Helps with IDE autocomplete and debugging
3. **Handle errors gracefully**: User-friendly error messages
4. **Validate inputs**: Check user input before processing
5. **Document complex logic**: Add comments for non-obvious code

### Performance

1. **Lazy loading**: Load large data only when needed
2. **Caching**: Cache API responses when appropriate
3. **Async operations**: Consider async for I/O operations (future)
4. **Image optimization**: Compress images if file size is concern

### Security

1. **Never commit secrets**: Use `.gitignore` for `.env`
2. **Validate file paths**: Prevent directory traversal
3. **Sanitize inputs**: Clean user input before API calls
4. **Rate limiting**: Consider for production deployments

---

## Resources

### Documentation
- [Gradio Docs](https://gradio.app/docs/)
- [Google Gemini API](https://ai.google.dev/docs)
- [Python dotenv](https://github.com/theskumar/python-dotenv)
- [PyYAML](https://pyyaml.org/wiki/PyYAMLDocumentation)

### Community
- GitHub Issues: Bug reports and feature requests
- GitHub Discussions: Questions and community support

### Related Projects
- [Gradio](https://github.com/gradio-app/gradio)
- [Google Generative AI](https://github.com/google/generative-ai-python)

---

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

---

## Questions?

For development questions:
1. Check existing documentation
2. Search GitHub issues
3. Open a new issue with "Question" label
4. Join discussions on GitHub

Happy coding! 
