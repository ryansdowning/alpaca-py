from .models import ValidateBaseModel as BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional, List
from ..enums import OrderStatus


class Position(BaseModel):
    """ """

    asset_id: UUID
    symbol: str
    exchange: str
    asset_class: str
    avg_entry_price: str
    qty: str
    side: str
    market_value: str
    cost_basis: str
    unrealized_pl: str
    unrealized_plpc: str
    unrealized_intraday_pl: str
    unrealized_intraday_plpc: str
    current_price: str
    lastday_price: str
    change_today: str


class ClosePositionResponse(BaseModel):
    """ """

    order_id: UUID
    status_code: int


class Order(BaseModel):
    """ """

    id: UUID
    client_order_id: UUID
    created_at: datetime
    updated_at: datetime
    submitted_at: datetime
    filled_at: Optional[datetime]
    expired_at: Optional[datetime]
    canceled_at: Optional[datetime]
    failed_at: Optional[datetime]
    replaced_at: Optional[datetime]
    replaced_by: Optional[UUID]
    replaces: Optional[UUID]
    asset_id: UUID
    symbol: str
    asset_class: str
    notional: Optional[str]
    qty: Optional[str]
    filled_qty: Optional[str]
    filled_avg_price: Optional[str]
    order_class: str
    order_type: str
    type: str
    side: str
    time_in_force: str
    limit_price: Optional[str]
    stop_price: Optional[str]
    status: OrderStatus
    extended_hours: bool
    legs: Optional[List["Order"]]
    trail_percent: Optional[str]
    trail_price: Optional[str]
    hwm: Optional[str]
    commission: float


class PortfolioHistory(BaseModel):
    """ """

    timestamp: List[int]
    equity: List[float]
    profit_loss: List[float]
    profit_loss_pct: List[float]
    base_value: float
    timeframe: str
