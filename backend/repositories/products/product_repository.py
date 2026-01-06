from typing import Optional
from backend.models.product import Product

class ProductRepository:

    def __init__(self, db):
        self.db = db

    def add_product(self, product: Product) -> Product:
        query = """
        INSERT INTO products (name, price, description, category, created_at, updated_at)
        VALUES (:name, :price, :description, :category, :created_at, :updated_at)
        RETURNING id;
        """
        cursor = self.db.cursor()
        cursor.execute(query, product.dict())
        product.id = cursor.fetchone()[0]
        self.db.commit()
        return product

    def get_product_by_name(self, name: str) -> Optional<Product]:
        query = "SELECT * FROM products WHERE name = :name;"
        cursor = self.db.cursor()
        cursor.execute(query, {"name": name})
        row = cursor.fetchone()
        if row:
            return Product(id=row[0], name=row[1], price=row[2], description=row[3], category=row[4], created_at=row[5], updated_at=row[6])
        return None