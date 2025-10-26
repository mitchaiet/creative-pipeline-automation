"""Test image detection"""
from app import get_available_products, get_product_images
from pathlib import Path

# Test all products
products = get_available_products()
print(f"Testing image detection for {len(products)} products:\n")

for product in products:
    product_photos = get_product_images(product, "product")
    logo_photos = get_product_images(product, "logo")

    print(f"📦 {product}")
    print(f"   Product photos: {len(product_photos)}")
    print(f"   Logo photos: {len(logo_photos)}")

    # Show file types
    if product_photos:
        extensions = set(Path(p).suffix.lower() for p in product_photos)
        print(f"   Product formats: {', '.join(sorted(extensions))}")

    if logo_photos:
        extensions = set(Path(p).suffix.lower() for p in logo_photos)
        print(f"   Logo formats: {', '.join(sorted(extensions))}")

    print()
