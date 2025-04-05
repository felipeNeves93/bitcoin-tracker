from datetime import date
from typing import Optional

import pytest
from sqlalchemy.orm import Session

from app.database.bitcoin_repository import BitcoinRepository
from app.database.database_manager import DatabaseManager, Base
from app.database.model.bitcoin_price import BitcoinPrice


@pytest.fixture(scope="function")
def db_session():
    db_manager = DatabaseManager(database_url="sqlite:///:memory:")
    db_manager.create_tables()

    session = db_manager.get_session()
    yield session

    session.close()
    Base.metadata.drop_all(bind=db_manager.engine)


def test_insert_and_get_latest_price(db_session: Session):
    repository = BitcoinRepository(db_session)
    repository.insert_price(100)

    latest_price: Optional[BitcoinPrice] = repository.get_latest_price()

    assert latest_price is not None
    assert latest_price.price == 100


def test_insert_new_summary_and_get_by_day(db_session: Session):
    repository = BitcoinRepository(db_session)

    max_price = 500
    day = date(2025, 1, 1)

    repository.update_summary(max_price, day)

    # Get a summary first from another date
    summary = repository.get_summary_by_day(date(2021, 1, 1))

    assert summary is None

    summary = repository.get_summary_by_day(day)

    assert summary is not None
    assert summary.max_price == max_price
    assert summary.day == day


def test_update_existing_summary_with_values_that_wont_change_it(db_session: Session):
    repository = BitcoinRepository(db_session)

    min_price = 100

    new_min_price = 150

    day = date(2025, 1, 1)

    repository.update_summary(min_price, day)

    summary = repository.get_summary_by_day(day)

    assert summary.min_price == min_price

    repository.update_summary(new_min_price, day)

    summary = repository.get_summary_by_day(day)

    assert summary.min_price == min_price


def test_update_existing_summary_with_new_values(db_session: Session):
    repository = BitcoinRepository(db_session)

    max_price = 500

    new_max_price = 600

    day = date(2025, 1, 1)

    repository.update_summary(max_price, day)

    summary = repository.get_summary_by_day(day)

    assert summary.max_price == max_price

    repository.update_summary(new_max_price, day)

    summary = repository.get_summary_by_day(day)

    assert summary.max_price == new_max_price
