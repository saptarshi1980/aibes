from enum import Enum


class TenderStatus(str, Enum):

    DRAFT = "DRAFT"

    OPEN = "OPEN"

    CLOSED = "CLOSED"

    EVALUATION = "EVALUATION"

    COMPLETED = "COMPLETED"

    ARCHIVED = "ARCHIVED"

    CANCELLED = "CANCELLED"