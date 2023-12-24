from typing import List
from dataclasses import dataclass
import json


@dataclass
class NetPosition:
    symbol: str
    id: str
    buy_avg: float
    buy_qty: int
    buy_val: float
    sell_avg: float
    sell_qty: int
    sell_val: float
    net_avg: int
    net_qty: int
    side: int
    qty: int
    product_type: str
    realized_profit: float
    cross_currency: str
    rbi_ref_rate: int
    fy_token: str
    exchange: int
    segment: int
    day_buy_qty: int
    day_sell_qty: int
    cf_buy_qty: int
    cf_sell_qty: int
    qty_multi_com: int
    pl: float
    unrealized_profit: int
    ltp: float
    sl_no: int

    @staticmethod
    def from_dict(obj) -> "NetPosition":
        return NetPosition(
            symbol=str(obj.get("symbol")),
            id=str(obj.get("id")),
            buy_avg=float(obj.get("buyAvg", 0)),
            buy_qty=int(obj.get("buyQty", 0)),
            buy_val=float(obj.get("buyVal", 0)),
            sell_avg=float(obj.get("sellAvg", 0)),
            sell_qty=int(obj.get("sellQty", 0)),
            sell_val=float(obj.get("sellVal", 0)),
            net_avg=int(obj.get("netAvg", 0)),
            net_qty=int(obj.get("netQty", 0)),
            side=int(obj.get("side", 0)),
            qty=int(obj.get("qty", 0)),
            product_type=str(obj.get("productType")),
            realized_profit=float(obj.get("realized_profit", 0)),
            cross_currency=str(obj.get("crossCurrency", "")),
            rbi_ref_rate=int(obj.get("rbiRefRate", 0)),
            fy_token=str(obj.get("fyToken")),
            exchange=int(obj.get("exchange", 0)),
            segment=int(obj.get("segment", 0)),
            day_buy_qty=int(obj.get("dayBuyQty", 0)),
            day_sell_qty=int(obj.get("daySellQty", 0)),
            cf_buy_qty=int(obj.get("cfBuyQty", 0)),
            cf_sell_qty=int(obj.get("cfSellQty", 0)),
            qty_multi_com=int(obj.get("qtyMulti_com", 0)),
            pl=float(obj.get("pl", 0)),
            unrealized_profit=int(obj.get("unrealized_profit", 0)),
            ltp=float(obj.get("ltp", 0)),
            sl_no=int(obj.get("slNo", 0)),
        )


@dataclass
class Overall:
    count_open: int
    count_total: int
    pl_realized: float
    pl_total: float
    pl_unrealized: int

    @staticmethod
    def from_dict(obj) -> "Overall":
        return Overall(
            count_open=int(obj.get("count_open", 0)),
            count_total=int(obj.get("count_total", 0)),
            pl_realized=float(obj.get("pl_realized", 0)),
            pl_total=float(obj.get("pl_total", 0)),
            pl_unrealized=int(obj.get("pl_unrealized", 0)),
        )


@dataclass
class NetPositionResponse:
    code: int
    message: str
    s: str
    net_positions: List[NetPosition]
    overall: Overall

    @staticmethod
    def from_dict(obj) -> "NetPositionResponse":
        return NetPositionResponse(
            code=int(obj.get("code")),
            message=str(obj.get("message", "")),
            s=str(obj.get("s")),
            net_positions=[NetPosition.from_dict(y) for y in obj.get("netPositions")],
            overall=Overall.from_dict(obj.get("overall")),
        )

    @staticmethod
    def from_json(json_string: str) -> "NetPositionResponse":
        obj = json.loads(json_string)

        return NetPositionResponse(
            code=int(obj.get("code")),
            message=str(obj.get("message", "")),
            s=str(obj.get("s")),
            net_positions=[NetPosition.from_dict(y) for y in obj.get("netPositions")],
            overall=Overall.from_dict(obj.get("overall")),
        )

    def get_positions_of_type(self, product_type: str) -> List[NetPosition]:
        """Filter positions by a certain product type."""
        return [
            position
            for position in self.net_positions
            if position.product_type == product_type
        ]


# Example Usage
# json_string = '{"code":200, ...}'  # Replace with actual JSON string
# json_data = json.loads(json_string)
# root = Root.from_dict(json_data)
