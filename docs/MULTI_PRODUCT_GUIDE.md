# Multi-Product Generation Guide

This guide explains how to use the multi-product selection and generation features.

## Overview

The Creative Automation Pipeline supports generating product views for multiple products simultaneously. You can choose between two generation modes:

1. **Separate Mode**: Generate individual views for each product
2. **Combined Mode**: Generate views with all products together

## Multi-Product Selection

### How to Select Multiple Products

1. Navigate to the **Products** tab
2. Click on the **Select Products** dropdown
3. The dropdown supports multi-select - you can:
   - Click multiple products to select them
   - Click a selected product again to deselect it
   - Select as many products as you need

### Product Preview

When you select multiple products:
- The **Product Photos** gallery shows photos from all selected products
- The **Logo Assets** gallery shows logos from all selected products
- Photos and logos are combined from all selections for easy review

## Generation Modes

### Separate Mode (Default)

**What it does:**
- Generates individual product views for each selected product separately
- Each product gets its own set of 6 views (front, back, left, right, top-down, bottom-up)
- Products are photographed independently

**Output:**
- Saved to each product's individual folder: `products/{product-slug}/photos/generated/`
- Each product maintains its own generated images directory
- Total images: 6 views × number of products

**Best for:**
- Individual product catalogs
- E-commerce product pages
- SKU-specific imagery
- When products need to be showcased independently

**Example:**
If you select `eco-cleaner` and `smart-watch`:
- Generates 6 views of eco-cleaner alone → saved to `products/eco-cleaner/photos/generated/`
- Generates 6 views of smart-watch alone → saved to `products/smart-watch/photos/generated/`
- Total: 12 images

### Combined Mode

**What it does:**
- Generates product views showing ALL selected products together in a single composition
- Creates 6 views with all products arranged aesthetically in each shot
- Products appear together as a product bundle or set

**Output:**
- Saved to a timestamped combined folder: `outputs/combined_{timestamp}/`
- All products appear in each of the 6 views
- Total images: 6 views (all products in each view)

**Best for:**
- Product bundles and sets
- Gift packages
- Cross-sell imagery
- Campaign visuals showing multiple products
- Comparison shots

**Example:**
If you select `eco-cleaner` and `smart-watch`:
- Generates 6 views showing both products together
- Each view contains both eco-cleaner and smart-watch in a single image
- Saved to `outputs/combined_20251026_120000/`
- Total: 6 images (each containing both products)

## Step-by-Step Instructions

### Generating Separate Product Views

1. Select one or more products from the dropdown
2. Choose **"Separate - Generate individual views for each product"**
3. Click **"Generate All Product Views"**
4. Wait for generation to complete
5. Images saved to individual product folders

Progress indicator shows: `{product-name}: {view} view...`

### Generating Combined Product Views

1. Select two or more products from the dropdown
2. Choose **"Combined - Generate views with all products together"**
3. Click **"Generate All Product Views"**
4. Wait for generation to complete
5. Images saved to `outputs/combined_{timestamp}/`

Progress indicator shows: `Generating combined {view} view...`

## Technical Details

### Separate Mode Behavior

- Loads each product's config independently
- Uses each product's reference photos separately
- Generates views sequentially for each product
- Each product maintains its brand identity and appearance
- Processing time: ~6 views per product

### Combined Mode Behavior

- Loads all product configs simultaneously
- Combines reference photos from all products
- Instructs AI to arrange products aesthetically
- Creates cohesive compositions with all products
- Processing time: ~6 views total (regardless of product count)

### AI Prompt Differences

**Separate Mode Prompt:**
```
Study the provided reference images of this {product_name} product.
Generate a professional product photography shot...
```

**Combined Mode Prompt:**
```
Study the provided reference images showing multiple products: {product1} and {product2}.
Generate a professional product photography shot showing ALL products together in a single composition...
Arrange products in an aesthetically pleasing composition...
```

## Tips & Best Practices

### For Separate Mode:
- Select 1-3 products at a time for reasonable processing time
- Each product can have very different styling and it won't matter
- Great for batch processing individual product catalogs

### For Combined Mode:
- Select products that make sense together (e.g., same product line, gift sets, bundles)
- 2-4 products works best for composition
- Products should have compatible sizes for good visual balance
- Consider products from the same category or campaign

### General Tips:
- Always ensure selected products have reference photos in their folders
- Preview photos before generating to confirm selections
- Use descriptive timestamps to organize combined outputs
- Combined mode saves to centralized outputs folder for easy campaign management

## Troubleshooting

**Issue**: "No existing product photos found"
- **Solution**: Ensure selected products have photos in `products/{slug}/photos/product/`

**Issue**: Combined mode shows only one product
- **Solution**: Make sure all selected products have reference photos loaded

**Issue**: Generation takes too long
- **Solution**: For separate mode with many products, consider running in smaller batches

## Output Structure

```
# Separate Mode
products/
  eco-cleaner/
    photos/
      generated/
        front_20251026_120000.png
        back_20251026_120000.png
        ...
  smart-watch/
    photos/
      generated/
        front_20251026_120000.png
        back_20251026_120000.png
        ...

# Combined Mode
outputs/
  combined_20251026_120000/
    combined_front_20251026_120000.png
    combined_back_20251026_120000.png
    combined_left_20251026_120000.png
    combined_right_20251026_120000.png
    combined_top-down_20251026_120000.png
    combined_bottom-up_20251026_120000.png
```
