from uuid import UUID

from sqlalchemy.orm import Session

from canarypy.api.models.product import Product


class ProductService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_product_by_id(self, product_id: UUID):
        return self.db_session.query(Product).filter(Product.id == product_id).first()

    def get_products(self):
        return self.db_session.query(Product).all()

    def save(self, product: Product):
        new_product = Product(
            name=product.name,
            repository_url=product.repository_url,
            artifact_url=product.artifact_url,
        )
        self.db_session.add(new_product)
        self.db_session.commit()
        return new_product
