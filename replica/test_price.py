import datetime
import pandas as pd
import pytest

from price import _ensure_same_prices_within_hour

INDEX = pd.MultiIndex.from_tuples(
    [
        (1, 32, (2022, 4, 1), datetime.datetime.strptime("2022-04-01 00:15:00+02:00", "%Y-%m-%d %H:%M:%S%z")),
        (1, 32, (2022, 4, 1), datetime.datetime.strptime("2022-04-01 00:45:00+02:00", "%Y-%m-%d %H:%M:%S%z")),
        (1, 32, (2022, 4, 1), datetime.datetime.strptime("2022-04-01 01:00:00+02:00", "%Y-%m-%d %H:%M:%S%z")),
        (1, 32, (2022, 4, 1), datetime.datetime.strptime("2022-04-01 01:15:00+02:00", "%Y-%m-%d %H:%M:%S%z")),
        (1, 32, (2022, 4, 1), datetime.datetime.strptime("2022-04-01 01:30:00+02:00", "%Y-%m-%d %H:%M:%S%z")),
        (1, 32, (2022, 4, 1), datetime.datetime.strptime("2022-04-01 01:45:00+02:00", "%Y-%m-%d %H:%M:%S%z")),
    ],
    names=["ablock", "service", "contract", "interval"],
)

@pytest.mark.parametrize(
    "price_data, data_expected",
    [
        pytest.param(
            [1.0, 4.0, 2.0, 5.0, 2.0, 2.0],
            [1.0, 1.0, 2.0, 2.0, 2.0, 2.0],
        ),
        pytest.param(
            [1.0, 1.0, 5.0, 5.0, 2.0, 2.0],
            [1.0, 1.0, 5.0, 5.0, 5.0, 5.0],
        ),
    ],
)
def test__ensure_same_prices_within_hour(price_data, data_expected):
    expected_activation_price = pd.Series(data=data_expected, index=INDEX)
    activation_prices = pd.Series(data=price_data, index=INDEX)

    activation_prices_checked = _ensure_same_prices_within_hour(activation_prices=activation_prices)

    pd.testing.assert_series_equal(activation_prices_checked, expected_activation_price)

