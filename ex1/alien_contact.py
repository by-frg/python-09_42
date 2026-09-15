#!/usr/bin/env python3
from pydantic import BaseModel, Field, ValidationError, model_validator
from datetime import datetime
from typing import Optional
from enum import Enum


class ContactType(Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: Optional[str] = Field(None, max_length=500)
    is_verified: bool = False

    @model_validator(mode='after')
    def validate_contact(self) -> "AlienContact":
        if self.contact_id[:2] != "AC":
            raise ValueError("Contact ID must start with 'AC'")
        if (self.contact_type == ContactType.PHYSICAL
                and not self.is_verified):
            raise ValueError("Physical contact reports must be verified")
        if (self.contact_type is ContactType.TELEPATHIC
                and self.witness_count < 3):
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses"
                )
        if self.signal_strength > 7.0 and self.message_received is None:
            raise ValueError(
                "Strong signals (> 7.0) should include received messages"
                )
        return self


def main() -> None:
    print("==================================")
    print("Valid Contact Report")

    try:
        contact_1 = AlienContact(
            contact_id="AC_2024_01",
            timestamp="2024-04-20T09:42:42",  # type: ignore[arg-type]
            location="Area 51, Nevada",
            contact_type=ContactType.RADIO,
            signal_strength="8.5",  # type: ignore[arg-type]
            duration_minutes="45",  # type: ignore[arg-type]
            witness_count="5",  # type: ignore[arg-type]
            message_received="Greetings from Zeta Reticuli",
            is_verified="True",  # type: ignore[arg-type]
        )
        print(
            f"ID: {contact_1.contact_id}\n"
            f"Type: {contact_1.contact_type.value}\n"
            f"Location: {contact_1.location}\n"
            f"Signal: {contact_1.signal_strength}/10\n"
            f"Duration: {contact_1.duration_minutes} minutes\n"
            f"Witnesses: {contact_1.witness_count}\n"
            f"Message: {contact_1.message_received}\n"
        )

        print("==================================\n")

        # testing invalid data input
        print("Expected validation error")
        AlienContact(
            contact_id="AC_2024_02",
            timestamp="2024-09-20T09:42:42",  # type: ignore[arg-type]
            location="Area 51, Nevada",
            contact_type="telepathic",  # type: ignore[arg-type]
            signal_strength="7.5",  # type: ignore[arg-type]
            duration_minutes="100",  # type: ignore[arg-type]
            witness_count="2",  # type: ignore[arg-type]
            message_received="Greetings from Beta Yuli",
            is_verified="True",  # type: ignore[arg-type]
        )
    except ValidationError as err:
        for e in err.errors():
            print(e['msg'])


if __name__ == "__main__":
    print("Alien Contact Validation Log")
    main()
