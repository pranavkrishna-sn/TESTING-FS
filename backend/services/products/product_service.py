from backend.repositories.products.product_repository import ProductRepository
from backend.models.product import Product
from typing import Optional

class ProductService:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def add_product(self, name: str, price: float, description: str, category: Optional[str] = None) -> Product:
        product = Product(name=name, price=price, description=description, category=category)
        return self.product_repository.add_product(product)

    def update_product(self, product_id: int, name: Optional[str], price: Optional[float], description: Optional[str], category: Optional[str]) -> bool:
        product = self.product_repository.get_product_by_id(product_id)
        if not product:
            return False

        if name:
            product.name = name
        if price is not None:
            product.price = price
        if description:
            product.description = description
        if category is not None:
            product.category = category

        self.product_repository.update_product(product)
        return True