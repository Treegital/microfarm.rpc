import typing as t
from pydantic import BaseModel, computed_field
from datetime import datetime
from cryptography import x509
from typing_extensions import TypedDict


I = t.TypeVar('I')
Error = str
Token = str


class Pagination(TypedDict):
    total: int
    offset: int | None = None
    page_size: int | None = None


class PaginatedSet(BaseModel, t.Generic[I]):
    metadata: Pagination
    items: t.List[I]


class CertificateRequest(BaseModel):
    id: str
    requester: str
    identity: str
    submission_date: datetime
    serial_number: str | None = None
    generation_date: datetime | None = None

    @computed_field
    def status(self) -> str:
        if self.serial_number:
            return 'generated'
        return "pending"


class CertificateInfo(BaseModel):
    account: str
    identity: str
    serial_number: str
    fingerprint: str
    valid_from: datetime
    valid_until: datetime
    generation_date: datetime | None = None
    revocation_date: datetime | None = None
    revocation_reason: x509.ReasonFlags | None = None

    @computed_field
    def status(self) -> str:
        if self.revocation_date:
            return 'revoked'

        now = datetime.now()
        if self.valid_from <= now:
            if self.valid_until <= now:
                return 'expired'
            else:
                return 'active'
        return 'not yet active'
