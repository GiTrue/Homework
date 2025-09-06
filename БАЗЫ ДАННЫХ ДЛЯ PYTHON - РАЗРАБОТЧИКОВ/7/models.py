import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Publisher(Base):
    __tablename__ = "publisher"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True, nullable=False)

    books = relationship("Book", back_populates="publisher")

    def __repr__(self):
        return f"<Publisher(id={self.id}, name='{self.name}')>"

class Book(Base):
    __tablename__ = "book"

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String, nullable=False)
    id_publisher = sa.Column(sa.Integer, sa.ForeignKey("publisher.id"), nullable=False)

    publisher = relationship("Publisher", back_populates="books")
    stocks = relationship("Stock", back_populates="book")

    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}')>"

class Shop(Base):
    __tablename__ = "shop"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True, nullable=False)

    stocks = relationship("Stock", back_populates="shop")

    def __repr__(self):
        return f"<Shop(id={self.id}, name='{self.name}')>"

class Stock(Base):
    __tablename__ = "stock"

    id = sa.Column(sa.Integer, primary_key=True)
    id_book = sa.Column(sa.Integer, sa.ForeignKey("book.id"), nullable=False)
    id_shop = sa.Column(sa.Integer, sa.ForeignKey("shop.id"), nullable=False)
    count = sa.Column(sa.Integer, nullable=False)

    book = relationship("Book", back_populates="stocks")
    shop = relationship("Shop", back_populates="stocks")
    sales = relationship("Sale", back_populates="stock")

    def __repr__(self):
        return f"<Stock(id={self.id}, book={self.id_book}, shop={self.id_shop}, count={self.count})>"

class Sale(Base):
    __tablename__ = "sale"

    id = sa.Column(sa.Integer, primary_key=True)
    price = sa.Column(sa.Numeric(10, 2), nullable=False)
    date_sale = sa.Column(sa.DateTime, nullable=False)
    id_stock = sa.Column(sa.Integer, sa.ForeignKey("stock.id"), nullable=False)
    count = sa.Column(sa.Integer, nullable=False)

    stock = relationship("Stock", back_populates="sales")

    def __repr__(self):
        return f"<Sale(id={self.id}, price={self.price}, date={self.date_sale})>"
