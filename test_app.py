"""Quick test of the app functionality"""
from app import get_available_products, load_product

# Test getting products
products = get_available_products()
print(f"Found {len(products)} products:")
for p in products:
    print(f"  - {p}")

# Test loading a product
if products:
    test_product = products[0]
    print(f"\nTesting with product: {test_product}")
    product_photos, logo_photos = load_product(test_product)
    print(f"  Product photos: {len(product_photos)}")
    print(f"  Logo photos: {len(logo_photos)}")

    if product_photos:
        print(f"  First product photo: {product_photos[0]}")
    if logo_photos:
        print(f"  First logo: {logo_photos[0]}")
