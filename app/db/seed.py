from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Category, Product, User, Profile, Order, OrderItem


async def seed_if_empty(db: AsyncSession) -> None:
    # Users
    res = await db.execute(select(User).limit(1))
    if res.scalar_one_or_none() is None:
        u1 = User(username="user1", email="user1@example.com", is_active=True)
        u2 = User(username="user2", email="user2@example.com", is_active=True)
        db.add_all([u1, u2])
        await db.commit()
        await db.refresh(u1)
        await db.refresh(u2)

        db.add_all([
            Profile(user_id=u1.id, full_name="User One", phone="111-111"),
            Profile(user_id=u2.id, full_name="User Two", phone="222-222"),
        ])
        await db.commit()

    # Categories
    res = await db.execute(select(Category).limit(1))
    if res.scalar_one_or_none() is None:
        c1 = Category(name="Electronics")
        c2 = Category(name="Books")
        db.add_all([c1, c2])
        await db.commit()
        await db.refresh(c1)
        await db.refresh(c2)

        p1 = Product(name="Keyboard", price=49.99, category_id=c1.id)
        p2 = Product(name="Python Book", price=19.99, category_id=c2.id)
        db.add_all([p1, p2])
        await db.commit()
        await db.refresh(p1)
        await db.refresh(p2)

    # Orders + OrderItems
    res = await db.execute(select(Order).limit(1))
    if res.scalar_one_or_none() is None:
        user = (await db.execute(select(User).order_by(User.id))).scalars().first()
        product = (await db.execute(select(Product).order_by(Product.id))).scalars().first()
        if user and product:
            o1 = Order(user_id=user.id, status="new")
            o2 = Order(user_id=user.id, status="paid")
            db.add_all([o1, o2])
            await db.commit()
            await db.refresh(o1)
            await db.refresh(o2)

            db.add_all([
                OrderItem(order_id=o1.id, product_id=product.id, qty=1, unit_price=float(product.price)),
                OrderItem(order_id=o2.id, product_id=product.id, qty=2, unit_price=float(product.price)),
            ])
            await db.commit()