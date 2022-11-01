# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.customer import Customer  # noqa
from app.models.cat import Cat  # noqa