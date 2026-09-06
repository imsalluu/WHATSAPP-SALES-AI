from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, func
from app.core.database import get_db
from app.core.deps import get_current_organization, require_roles
from app.models.organization import Organization, RoleType
from app.models.product import Product, ProductVariant
from app.schemas.product import ProductCreate, ProductUpdate, ProductOut, VariantCreate, VariantOut

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=List[ProductOut])
async def list_products(
    query: Optional[str] = None,
    category: Optional[str] = None,
    current_org: Organization = Depends(get_current_organization),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Product).where(Product.organization_id == current_org.id)
    if query:
        kw = f"%{query.lower()}%"
        stmt = stmt.where(
            or_(
                func.lower(Product.name).like(kw),
                func.lower(Product.sku).like(kw),
                func.lower(Product.description).like(kw),
            )
        )
    if category:
        stmt = stmt.where(func.lower(Product.category) == category.lower())

    stmt = stmt.order_by(Product.created_at.desc())
    result = await db.execute(stmt)
    products = result.scalars().all()

    # Load variants
    products_out = []
    for p in products:
        var_stmt = select(ProductVariant).where(ProductVariant.product_id == p.id)
        var_res = await db.execute(var_stmt)
        p.variants = var_res.scalars().all()
        products_out.append(p)

    return products_out


@router.post("/", response_model=ProductOut)
async def create_product(
    data: ProductCreate,
    current_org: Organization = Depends(get_current_organization),
    db: AsyncSession = Depends(get_db),
    _role=Depends(require_roles([RoleType.OWNER.value, RoleType.ADMIN.value, RoleType.AGENT.value])),
):
    # Check SKU unique
    sku_check = await db.execute(
        select(Product).where(Product.organization_id == current_org.id, Product.sku == data.sku)
    )
    if sku_check.scalar_one_or_none():
        raise HTTPException(status_code=400, detail=f"Product with SKU '{data.sku}' already exists.")

    product = Product(
        organization_id=current_org.id,
        name=data.name,
        sku=data.sku,
        description=data.description,
        category=data.category,
        price=data.price,
        discount_price=data.discount_price,
        is_available=data.is_available,
        tags=data.tags,
        images=data.images,
        attributes=data.attributes,
    )
    db.add(product)
    await db.flush()

    # Create variants
    variants_list = []
    if data.variants:
        for v in data.variants:
            variant = ProductVariant(
                organization_id=current_org.id,
                product_id=product.id,
                sku=v.sku,
                title=v.title,
                size=v.size,
                color=v.color,
                material=v.material,
                price_override=v.price_override,
                stock_quantity=v.stock_quantity,
                is_available=v.is_available,
            )
            db.add(variant)
            variants_list.append(variant)
    else:
        # Default single standard variant
        variant = ProductVariant(
            organization_id=current_org.id,
            product_id=product.id,
            sku=f"{product.sku}-STD",
            title="Standard / All Size",
            stock_quantity=50,
            is_available=True,
        )
        db.add(variant)
        variants_list.append(variant)

    await db.commit()
    await db.refresh(product)
    product.variants = variants_list
    return product


@router.get("/{product_id}", response_model=ProductOut)
async def get_product_detail(
    product_id: str,
    current_org: Organization = Depends(get_current_organization),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Product).where(Product.id == product_id, Product.organization_id == current_org.id)
    res = await db.execute(stmt)
    product = res.scalars().first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    var_stmt = select(ProductVariant).where(ProductVariant.product_id == product.id)
    var_res = await db.execute(var_stmt)
    product.variants = var_res.scalars().all()
    return product


@router.delete("/{product_id}")
async def delete_product(
    product_id: str,
    current_org: Organization = Depends(get_current_organization),
    db: AsyncSession = Depends(get_db),
    _role=Depends(require_roles([RoleType.OWNER.value, RoleType.ADMIN.value])),
):
    stmt = select(Product).where(Product.id == product_id, Product.organization_id == current_org.id)
    res = await db.execute(stmt)
    product = res.scalars().first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    await db.delete(product)
    await db.commit()
    return {"message": "Product deleted successfully"}


@router.post("/seed-samples")
async def seed_sample_catalog(
    current_org: Organization = Depends(get_current_organization),
    db: AsyncSession = Depends(get_db),
):
    """Populates realistic demo products with variants and stock for instant testing."""
    sample_products = [
        {
            "name": "Heavyweight Oversized Black Hoodie",
            "sku": "HD-BLK-01",
            "description": "Premium 380 GSM fleece oversized black hoodie with kangaroo pockets and double-lined hood. Ideal winter streetwear.",
            "category": "Clothing",
            "price": 2200.0,
            "discount_price": 1850.0,
            "tags": ["hoodie", "black", "winter", "oversized", "streetwear", "gift"],
            "images": ["https://images.unsplash.com/photo-1556905055-8f358a7a47b2?w=800"],
            "variants": [
                {"sku": "HD-BLK-01-M", "title": "Black / M", "size": "M", "color": "Black", "stock_quantity": 25},
                {"sku": "HD-BLK-01-L", "title": "Black / L", "size": "L", "color": "Black", "stock_quantity": 40},
                {"sku": "HD-BLK-01-XL", "title": "Black / XL", "size": "XL", "color": "Black", "stock_quantity": 30},
                {"sku": "HD-BLK-01-XXL", "title": "Black / XXL", "size": "XXL", "color": "Black", "stock_quantity": 10},
            ]
        },
        {
            "name": "Minimalist Classic White Polo",
            "sku": "POLO-WHT-02",
            "description": "Breathable 100% Pique cotton polo t-shirt with ribbed collar and tailored sleeve cuffs. Smart casual aesthetic.",
            "category": "Clothing",
            "price": 1200.0,
            "discount_price": 990.0,
            "tags": ["polo", "white", "shirt", "summer", "formal", "casual"],
            "images": ["https://images.unsplash.com/photo-1581655353564-df123a1eb820?w=800"],
            "variants": [
                {"sku": "POLO-WHT-02-M", "title": "White / M", "size": "M", "color": "White", "stock_quantity": 15},
                {"sku": "POLO-WHT-02-L", "title": "White / L", "size": "L", "color": "White", "stock_quantity": 20},
                {"sku": "POLO-WHT-02-XL", "title": "White / XL", "size": "XL", "color": "White", "stock_quantity": 18},
            ]
        },
        {
            "name": "Genuine Leather Bifold Wallet & Keychain Gift Set",
            "sku": "GIFT-WAL-03",
            "description": "Handcrafted full-grain vintage brown leather wallet with RFID blocking and matching keychain in a luxury gift box.",
            "category": "Accessories",
            "price": 2800.0,
            "discount_price": 2450.0,
            "tags": ["gift", "wallet", "leather", "accessories", "gift for husband", "gift for wife", "birthday"],
            "images": ["https://images.unsplash.com/photo-1627123424574-724758594e93?w=800"],
            "variants": [
                {"sku": "GIFT-WAL-03-BRN", "title": "Vintage Tan Brown", "color": "Brown", "stock_quantity": 35},
                {"sku": "GIFT-WAL-03-BLK", "title": "Matte Jet Black", "color": "Black", "stock_quantity": 28},
            ]
        },
        {
            "name": "Luxury Silk Floral Scarf for Women",
            "sku": "SCARF-SLK-04",
            "description": "100% pure Mulberry silk square scarf with hand-rolled edges. Vibrant pastel floral pattern.",
            "category": "Accessories",
            "price": 1950.0,
            "discount_price": 1650.0,
            "tags": ["scarf", "silk", "gift for wife", "gift for women", "accessories", "luxury"],
            "images": ["https://images.unsplash.com/photo-1601924994987-69e26d50dc26?w=800"],
            "variants": [
                {"sku": "SCARF-SLK-04-PST", "title": "Pastel Blossom", "color": "Pastel Pink", "stock_quantity": 42},
                {"sku": "SCARF-SLK-04-BLU", "title": "Royal Azure", "color": "Blue", "stock_quantity": 30},
            ]
        },
        {
            "name": "Wireless Noise Cancelling Earbuds Pro",
            "sku": "TECH-EAR-05",
            "description": "Active Noise Cancellation, 36-hour battery life, IPX5 water resistance with high-fidelity deep bass.",
            "category": "Electronics",
            "price": 3500.0,
            "discount_price": 2990.0,
            "tags": ["earbuds", "audio", "bluetooth", "wireless", "electronics", "under 3000 taka"],
            "images": ["https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=800"],
            "variants": [
                {"sku": "TECH-EAR-05-BLK", "title": "Carbon Black", "color": "Black", "stock_quantity": 18},
                {"sku": "TECH-EAR-05-WHT", "title": "Glacier White", "color": "White", "stock_quantity": 22},
            ]
        }
    ]

    count = 0
    for p_data in sample_products:
        exists = await db.execute(
            select(Product).where(Product.organization_id == current_org.id, Product.sku == p_data["sku"])
        )
        if exists.scalar_one_or_none():
            continue

        prod = Product(
            organization_id=current_org.id,
            name=p_data["name"],
            sku=p_data["sku"],
            description=p_data["description"],
            category=p_data["category"],
            price=p_data["price"],
            discount_price=p_data.get("discount_price"),
            tags=p_data["tags"],
            images=p_data["images"],
            is_available=True,
        )
        db.add(prod)
        await db.flush()

        for v_data in p_data["variants"]:
            v = ProductVariant(
                organization_id=current_org.id,
                product_id=prod.id,
                sku=v_data["sku"],
                title=v_data["title"],
                size=v_data.get("size"),
                color=v_data.get("color"),
                stock_quantity=v_data["stock_quantity"],
                is_available=True,
            )
            db.add(v)
        count += 1

    await db.commit()
    return {"message": f"Successfully seeded {count} sample products with variants."}
