from datetime import datetime
from typing import Any, List, Optional
from uuid import UUID

from pydantic import parse_obj_as, root_validator, validator

from .documents import AccountDocument
from ..enums import (
    AccountStatus,
    AgreementType,
    ClearingBroker,
    DTBPCheck,
    EmploymentStatus,
    FundingSource,
    PDTCheck,
    TaxIdType,
    TradeConfirmationEmail,
    VisaType,
)
from ...common.models import ValidateBaseModel as BaseModel


class Contact(BaseModel):
    """User contact details within Account Model

    see https://alpaca.markets/docs/broker/api-references/accounts/accounts/#the-account-model

    Attributes:
        email_address (str): The user's email address
        phone_number (str): The user's phone number. It should include the country code.
        street_address (List[str]): The user's street address lines.
        unit (Optional[str]): The user's apartment unit, if any.
        city (str): The city the user resides in.
        state (Optional[str]): The state the user resides in. This is required if country is 'USA'.
        postal_code (str): The user's postal
        country (str): The country the user resides in. 3 letter country code is permissible.
    """

    email_address: str
    phone_number: str
    street_address: List[str]
    unit: Optional[str] = None
    city: str
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None

    @validator("state")
    def usa_state_has_value(cls, v: str, values: dict, **kwargs) -> str:
        """Validates that the state has a value if the country is USA

        Args:
            v (str): The state field's value
            values (dict): The values of each field

        Raises:
            ValueError: State is required for country USA

        Returns:
            str: The value of the state field
        """
        if "country" in values and values["country"] == "USA" and v is None:
            raise ValueError("State is required for country USA.")
        return v


class Identity(BaseModel):
    """User identity details within Account Model

    see https://alpaca.markets/docs/broker/api-references/accounts/accounts/#the-account-model

    Attributes:
        given_name (str): The user's first name
        middle_name (Optional[str]): The user's middle name, if any
        family_name (str): The user's last name
        date_of_birth (str): The user's date of birth
        tax_id (Optional[str]): The user's country specific tax id, required if tax_id_type is provided
        tax_id_type (Optional[TaxIdType]): The tax_id_type for the tax_id provided, required if tax_id provided
        country_of_citizenship (Optional[str]): The country the user is a citizen
        country_of_birth (Optional[str]): The country the user was born
        country_of_tax_residence (str): The country the user files taxes
        visa_type (Optional[VisaType]): Only used to collect visa types for users residing in the USA.
        visa_expiration_date (Optional[str]): The date of expiration for visa, Required if visa_type is set.
        date_of_departure_from_usa (Optional[str]): Required if visa_type = B1 or B2
        permanent_resident (Optional[bool]): Only used to collect permanent residence status in the USA.
        funding_source (Optional[List[FundingSource]]): How the user will fund their account
        annual_income_min (Optional[float]): The minimum of the user's income range
        annual_income_max (Optional[float]): The maximum of the user's income range
        liquid_net_worth_min (Optional[float]): The minimum of the user's liquid net worth range
        liquid_net_worth_max (Optional[float]): The maximum of the user's liquid net worth range
        total_net_worth_min (Optional[float]): The minimum of the user's total net worth range
        total_net_worth_max (Optional[float]): The maximum of the user's total net worth range
    """

    given_name: str
    middle_name: Optional[str] = None
    family_name: str
    date_of_birth: str
    tax_id: Optional[str] = None
    tax_id_type: Optional[TaxIdType] = None
    country_of_citizenship: Optional[str] = None
    country_of_birth: Optional[str] = None
    country_of_tax_residence: str
    visa_type: Optional[VisaType] = None
    visa_expiration_date: Optional[str] = None
    date_of_departure_from_usa: Optional[str] = None
    permanent_resident: Optional[bool] = None
    funding_source: Optional[List[FundingSource]] = None
    annual_income_min: Optional[float] = None
    annual_income_max: Optional[float] = None
    liquid_net_worth_min: Optional[float] = None
    liquid_net_worth_max: Optional[float] = None
    total_net_worth_min: Optional[float] = None
    total_net_worth_max: Optional[float] = None


class Disclosures(BaseModel):
    """User disclosures within Account Model

    see https://alpaca.markets/docs/broker/api-references/accounts/accounts/#the-account-model

    Attributes:
        is_control_person (bool): Whether user holds a controlling position in a publicly traded company
        is_affiliated_exchange_or_finra (bool): If user is affiliated with any exchanges or FINRA
        is_politically_exposed (bool): If user is politically exposed
        immediate_family_exposed (bool): If user’s immediate family member is either politically exposed or holds a control position.
        employment_status (EmploymentStatus): The employment status of the user
        employer_name (str): The user's employer's name, if any
        employer_address (str): The user's employer's address, if any
        employment_position (str): The user's employment position, if any
    """

    is_control_person: bool
    is_affiliated_exchange_or_finra: bool
    is_politically_exposed: bool
    immediate_family_exposed: bool
    employment_status: Optional[EmploymentStatus] = None
    employer_name: Optional[str] = None
    employer_address: Optional[str] = None
    employment_position: Optional[str] = None


class Agreement(BaseModel):
    """User agreements signed within Account Model

    see https://alpaca.markets/docs/broker/api-references/accounts/accounts/#the-account-model

    Attributes:
        agreement (Agreement): The type of agreement signed by the user
        signed_at (str): The timestamp the agreement was signed
        ip_address (str): The ip_address the signed agreements were sent from by the user
        revision (str): The revision date
    """

    agreement: AgreementType
    signed_at: str
    ip_address: str
    revision: Optional[str]


class TrustedContact(BaseModel):
    """User's trusted contact details within Account Model

    see https://alpaca.markets/docs/broker/api-references/accounts/accounts/#the-account-model

    Attributes:given_name
        given_name (str): The first name of the user's trusted contact
        family_name (str): The last name of the user's trusted contact
        email_address (Optional[str]): The email address of the user's trusted contact
        phone_number (Optional[str]): The email address of the user's trusted contact
        city (Optional[str]): The email address of the user's trusted contact
        state (Optional[str]): The email address of the user's trusted contact
        postal_code (Optional[str]): The email address of the user's trusted contact
        country (Optional[str]): The email address of the user's trusted contact
    """

    given_name: str
    family_name: str
    email_address: Optional[str] = None
    phone_number: Optional[str] = None
    street_address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None

    @root_validator()
    def root_validator(cls, values: dict) -> dict:
        has_phone_number = (
            "phone_number" in values and values["phone_number"] is not None
        )
        has_street_address = (
            "street_address" in values and values["street_address"] is not None
        )
        has_email_address = (
            "email_address" in values and values["email_address"] is not None
        )

        if has_phone_number or has_street_address or has_email_address:
            return values

        raise ValueError("At least one method of contact required for trusted contact")


class Account(BaseModel):
    """Contains information pertaining to a specific brokerage account

    see https://alpaca.markets/docs/broker/api-references/accounts/accounts/#the-account-model

    The fields contact, identity, disclosures, agreements, documents, trusted_contact, and trading_configurations
    are all optional and won't always be provided by the api depending on what endpoint you use and what options you
    pass

    Attributes:
        id (str): The account uuid used to reference this account
        account_number (str): A more human friendly identifier for this account
        status (AccountStatus): The approval status of this account
        crypto_status (Optional[AccountStatus]): The crypto trading status. Only present if crypto trading is enabled.
        currency (str): The currency the account's values are returned in
        last_equity (str): The total equity value stored in the account
        created_at (str): The timestamp when the account was created
        contact (Optional[Contact]): The contact details for the account holder
        identity (Optional[Identity]): The identity details for the account holder
        disclosures (Optional[Disclosures]): The account holder's political disclosures
        agreements (Optional[List[Agreement]]): The agreements the account holder has signed
        documents (Optional[List[AccountDocument]]): The documents the account holder has submitted
        trusted_contact (Optional[TrustedContact]): The account holder's trusted contact details
    """

    id: UUID
    account_number: str
    status: AccountStatus
    crypto_status: Optional[AccountStatus] = None
    currency: str
    last_equity: str
    created_at: str
    contact: Optional[Contact] = None
    identity: Optional[Identity] = None
    disclosures: Optional[Disclosures] = None
    agreements: Optional[List[Agreement]] = None
    documents: Optional[List[AccountDocument]] = None
    trusted_contact: Optional[TrustedContact] = None

    def __init__(self, **response):
        super().__init__(
            id=(UUID(response["id"])),
            account_number=(response["account_number"]),
            status=(response["status"]),
            crypto_status=(
                response["crypto_status"] if "crypto_status" in response else None
            ),
            currency=(response["currency"]),
            last_equity=(response["last_equity"]),
            created_at=(response["created_at"]),
            contact=(
                parse_obj_as(Contact, response["contact"])
                if "contact" in response
                else None
            ),
            identity=(
                parse_obj_as(Identity, response["identity"])
                if "identity" in response
                else None
            ),
            disclosures=(
                parse_obj_as(Disclosures, response["disclosures"])
                if "disclosures" in response
                else None
            ),
            agreements=(
                parse_obj_as(List[Agreement], response["agreements"])
                if "agreements" in response
                else None
            ),
            documents=(
                parse_obj_as(List[AccountDocument], response["documents"])
                if "documents" in response
                else None
            ),
            trusted_contact=(
                parse_obj_as(TrustedContact, response["trusted_contact"])
                if "trusted_contact" in response
                else None
            ),
        )


class TradeAccount(BaseModel):
    """
    Represents trading account information for an Account.

    Attributes:
        id (UUID): The account ID
        account_number (str): The account number
        status (AccountStatus): The current status of the account
        crypto_status (Optional[AccountStatus]): The status of the account in regards to trading crypto. Only present if
          crypto trading is enabled for your brokerage account.
        currency (Optional[str]): Currently will always be the value "USD".
        buying_power (str): Current available cash buying power. If multiplier = 2 then
          buying_power = max(equity-initial_margin(0) * 2). If multiplier = 1 then buying_power = cash.
        regt_buying_power (str): User’s buying power under Regulation T
          (excess equity - (equity - margin value) - * margin multiplier)
        daytrading_buying_power (str): The buying power for day trades for the account
        non_marginable_buying_power (str): The non marginable buying power for the account
        cash (str): Cash balance in the account
        cash_withdrawable (Optional[str]): Cash available for withdrawal from the account
        cash_transferable (Optional[str]): Cash available for transfer (JNLC) from the account
        accrued_fees (str): Fees accrued in this account
        pending_transfer_out (Optional[str]): Cash pending transfer out of this account
        pending_transfer_in (Optional[str]): Cash pending transfer into this account
        portfolio_value (str): Total value of cash + holding positions.
          (This field is deprecated. It is equivalent to the equity field.)
        pattern_day_trader (bool): Whether the account is flagged as pattern day trader or not.
        trading_blocked (bool): If true, the account is not allowed to place orders.
        transfers_blocked (bool): If true, the account is not allowed to request money transfers.
        account_blocked (bool): If true, the account activity by user is prohibited.
        created_at (datetime): Timestamp this account was created at
        trade_suspended_by_user (bool): If true, the account is not allowed to place orders.
        multiplier (str): Multiplier value for this account.
        shorting_enabled (bool): Flag to denote whether or not the account is permitted to short
        equity (str): This value is cash + long_market_value + short_market_value. This value isn't calculated in the
          SDK it is computed on the server and we return the raw value here.
        last_equity (str): Equity as of previous trading day at 16:00:00 ET
        long_market_value (str): Real-time MtM value of all long positions held in the account
        short_market_value (str): Real-time MtM value of all short positions held in the account
        initial_margin (str): Reg T initial margin requirement
        maintenance_margin (str): Maintenance margin requirement
        last_maintenance_margin (str): Maintenance margin requirement on the previous trading day
        sma (str): Value of Special Memorandum Account (will be used at a later date to provide additional buying_power)
        daytrade_count (int): The current number of daytrades that have been made in the last 5 trading days
          (inclusive of today)
        previous_close (Optional[datetime]): Previous sessions close time
        last_long_market_value (Optional[str]): Value of all long positions as of previous trading day at 16:00:00 ET
        last_short_market_value (Optional[str]): Value of all short positions as of previous trading day at 16:00:00 ET
        last_cash (Optional[str]): Value of all cash as of previous trading day at 16:00:00 ET
        last_initial_margin (Optional[str]): Value of initial_margin as of previous trading day at 16:00:00 ET
        last_regt_buying_power (Optional[str]): Value of regt_buying_power as of previous trading day at 16:00:00 ET
        last_daytrading_buying_power (Optional[str]): Value of daytrading_buying_power as of previous trading day at 16:00:00 ET
        last_daytrade_count (Optional[int]): Value of daytrade_count as of previous trading day at 16:00:00 ET
        last_buying_power (Optional[str]): Value of buying_power as of previous trading day at 16:00:00 ET
        clearing_broker (Optional[ClearingBroker]): The Clearing broker for this account
    """

    id: UUID
    account_number: str
    status: AccountStatus
    crypto_status: Optional[AccountStatus]
    currency: Optional[str]
    buying_power: str
    regt_buying_power: str
    daytrading_buying_power: str
    non_marginable_buying_power: str
    cash: str
    cash_withdrawable: Optional[str]
    cash_transferable: Optional[str]
    accrued_fees: str
    pending_transfer_out: Optional[str]
    pending_transfer_in: Optional[str]
    portfolio_value: str
    pattern_day_trader: bool
    trading_blocked: bool
    transfers_blocked: bool
    account_blocked: bool
    created_at: datetime
    trade_suspended_by_user: bool
    multiplier: str
    shorting_enabled: bool
    equity: str
    last_equity: str
    long_market_value: str
    short_market_value: str
    initial_margin: str
    maintenance_margin: str
    last_maintenance_margin: str
    sma: str
    daytrade_count: int
    previous_close: Optional[datetime]
    last_long_market_value: Optional[str]
    last_short_market_value: Optional[str]
    last_cash: Optional[str]
    last_initial_margin: Optional[str]
    last_regt_buying_power: Optional[str]
    last_daytrading_buying_power: Optional[str]
    last_daytrade_count: Optional[int]
    last_buying_power: Optional[str]
    clearing_broker: Optional[ClearingBroker]

    def __init__(self, **data: Any) -> None:
        if "id" in data and type(data["id"]) == str:
            data["id"] = UUID(data["id"])

        super().__init__(**data)


class TradeAccountConfiguration(BaseModel):
    """
    Represents configuration options for a TradeAccount.

    Attributes:
        dtbp_check (DTBPCheck): Day Trade Buying Power Check. Controls Day Trading Margin Call (DTMC) checks.
        fractional_trading (bool): If true, account is able to participate in fractional trading
        max_margin_multiplier (str): A number between 1-4 that represents your max margin multiplier
        no_shorting (bool): If true then Account becomes long-only mode.
        pdt_check (PDTCheck): Controls Pattern Day Trader (PDT) checks.
        suspend_trade (bool): If true Account becomes unable to submit new orders
        trade_confirm_email (TradeConfirmationEmail): Controls whether Trade confirmation emails are sent.
    """

    dtbp_check: DTBPCheck
    fractional_trading: bool
    max_margin_multiplier: str
    no_shorting: bool
    pdt_check: PDTCheck
    suspend_trade: bool
    trade_confirm_email: TradeConfirmationEmail
