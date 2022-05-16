import datetime

from .models import ValidateBaseModel as BaseModel
from typing import Optional
from datetime import date
from pydantic import validator


class NonEmptyRequest(BaseModel):
    """
    Mixin for models that represent requests where we don't want to send nulls for optional fields.
    """

    def to_request_fields(self) -> dict:
        """
        the equivalent of self::dict but removes empty values.

        Ie say we only set trusted_contact.given_name instead of generating a dict like:
          {contact: {city: None, country: None...}, etc}
        we generate just:
          {trusted_contact:{given_name: "new value"}}

        Returns:
            dict: a dict containing any set fields
        """

        # pydantic almost has what we need by passing exclude_none to dict() but it returns:
        #  {trusted_contact: {}, contact: {}, identity: None, etc}
        # so we do a simple list comprehension to filter out None and {}

        return {
            key: val
            for key, val in self.dict(exclude_none=True).items()
            if val and len(str(val)) > 0
        }


class ClosePositionRequest(NonEmptyRequest):
    """ """

    qty: str
    percentage: str


class GetPortfolioHistoryRequest(NonEmptyRequest):
    """ """

    period: Optional[str]
    timeframe: Optional[str]
    date_end: Optional[date]
    extended_hours: Optional[bool]

    @validator("date_end", pre=True)
    def parse_date_end(cls, value):
        return datetime.strptime(value, "%Y-%m-%d").date()
