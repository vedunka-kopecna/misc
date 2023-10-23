import pandas as pd
import logging
from dataclasses import dataclass


@dataclass(frozen=True)
class LevelsNames:
    """
    Collection of names of multiindex levels (problem dimensions)
    """

    ablocks: str = "ablock"
    services: str = "service"
    contracts: str = "contract"
    devices: str = "device"
    intervals: str = "interval"

lvls_names = LevelsNames()


def _ensure_same_prices_within_hour(activation_prices: pd.Series) -> pd.Series:
    """
    Ensure that the activation prices are the same in all intervals of each hour for every ablock, service and contract.
    """
    intervals_lvl = activation_prices.index.get_level_values(lvls_names.intervals)
    prices_grouped_hourly = activation_prices.groupby(
        [
            lvls_names.ablocks,
            lvls_names.services,
            lvls_names.contracts,
            intervals_lvl.date,
            intervals_lvl.hour,
        ]
    )
    if prices_grouped_hourly.nunique().ne(1).any():
        logging.warning("Multiple values of activation prices are used within the same hour.")
        return prices_grouped_hourly.transform(lambda s: s.iloc[0])
    return activation_prices