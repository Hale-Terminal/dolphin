def test_get(session, equity):
    from dolphin.equity.service import get

    t_equity = get(db_session=session, equity_id=equity.id)
    assert t_equity.id == equity.id


def test_get_all(session, equities):
    from dolphin.equity.service import get_all

    t_equities = get_all(db_session=session).all()
    assert t_equities


def test_create(session):
    from dolphin.equity.service import create
    from dolphin.equity.models import EquityCreate

    ticker = "ticker"
    name = "name"

    equity_in = EquityCreate(
        ticker="ticker",
        name="name",
        description="description",
        street1="street1",
        street2="street2",
        city="city",
        state="state",
        zip_code="zipcode",
        country_code="SS",
        exchange="exchange",
        ein="ein",
        phone_number="phone_number",
        shares_outstanding="so",
    )
    equity = create(db_session=session, equity_in=equity_in)
    assert equity
