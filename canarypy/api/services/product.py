from uuid import UUID

from sqlalchemy.orm import Session

from canarypy.api.models.product import Product
from canarypy.api.schemas import product as product_schema


class ProductService:
    """ProductService provides methods to interact with Product objects stored in a
    database."""

    def __init__(self, db_session: Session):
        """Initialize ProductService with the database session.

        Parameters:
        db_session (Session): SQLAlchemy session object.
        """
        self.db_session = db_session

    def get_product_by_id(self, product_id: UUID):
        """Retrieve a Product by its ID.

        Parameters:
        product_id (UUID): The ID of the Product to retrieve.

        Returns:
        Product: The Product object or None if not found.
        """
        return self.db_session.query(Product).filter(Product.id == product_id).first()

    def get_products(self):
        """Retrieve all Products.

        Returns:
        List[Product]: List of Product objects.
        """
        return self.db_session.query(Product).all()

    def save(self, product: product_schema.Product):
        """Save a new Product to the database.

        Parameters:
        product (Product): The Product to save.

        Returns:
        Product: The newly saved Product object.
        """
        new_product = Product(
            name=product.name,
            repository_url=product.repository_url,
            artifact_url=product.artifact_url,
        )
        self.db_session.add(new_product)
        self.db_session.commit()
        return new_product
