# Product View Generation Guide

## Camera Angles

The system generates 6 distinct product views with precise camera positioning:

### 1. **Front View**
- **Angle**: Straight-on front view, camera directly facing the front of the product at eye level
- **Shows**: Primary face/label of the product
- **Purpose**: Main product presentation

### 2. **Back View**
- **Angle**: Straight-on back/rear view, camera directly facing the back at eye level
- **Shows**: 180 degrees opposite from the front
- **Purpose**: Show ingredients, nutritional info, or rear features

### 3. **Left Side View**
- **Angle**: Left side profile, camera positioned 90 degrees to the left of the front view
- **Shows**: Left edge/side panel
- **Purpose**: Display product depth and left side details

### 4. **Right Side View**
- **Angle**: Right side profile, camera positioned 90 degrees to the right of the front view
- **Shows**: Right edge/side panel
- **Purpose**: Display product depth and right side details

### 5. **Top-Down View**
- **Angle**: Looking straight down from directly above the product
- **Shows**: Top surface as if camera is mounted on ceiling
- **Purpose**: Display product from overhead perspective

### 6. **Bottom-Up View**
- **Angle**: Looking straight up from directly below the product
- **Shows**: Bottom/base surface
- **Purpose**: Display product base and bottom features

## Prompt Strategy

Each view uses a structured prompt with:

1. **Reference Study**: "Study the provided reference images of this {product_name} product."
2. **Exact Angle Description**: Detailed camera positioning for the specific view
3. **Product Context**: Name and description from product config
4. **Critical Requirements**:
   - Identical appearance to reference images
   - Pure white background (#FFFFFF)
   - Professional studio lighting
   - Specific camera angle enforcement
   - High resolution, sharp focus
   - Photorealistic rendering
   - Square aspect ratio (1:1)

## Image-to-Image Generation

The system uses **multi-modal input**:
- Text prompt describing the exact angle needed
- All existing product photos as visual reference

This ensures:
- Consistent product appearance across all views
- Accurate colors, branding, and labels
- Realistic 3D representation from multiple angles
