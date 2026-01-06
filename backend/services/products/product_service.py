from backend.repositories.products.product_repository import ProductRepository
from backend.models.product import Product

class ProductService:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def add_product(self, name: str, price: float, description: str, category: Optional[str] = None) -> Product:
        product = Product(name=name, price=price, description=description, category=category)
        return self.product_repository.add_product(product)