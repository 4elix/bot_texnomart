from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, Mapped, mapped_column


# Базовый класс для всех моделей SQLAlchemy. Все ORM-классы будут наследоваться от
Base = declarative_base()


class Category(Base):
    #  Определяет таблицу с названием categories.
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)

    # Это связь один-ко-многим: у категории может быть много продуктов
    # back_populates="category" -> указывает на связанное поле в Product;
    # lazy="selectin" — SQLAlchemy сделает «умный» подзапрос

    # select -> Отдельный SQL-запрос при доступе к атрибуту
    # joined -> Джойнит данные сразу
    # selectin -> сначала ID, потом IN (...) запросом
    products = relationship('Product', back_populates='category', lazy='selectin')


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String)
    price: Mapped[str] = mapped_column(String)
    info: Mapped[str] = mapped_column(String)
    image_url: Mapped[str] = mapped_column(String)

    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    category = relationship('Category', back_populates='products', lazy='selectin')
