#!/usr/bin/env python3
from pydantic import BaseModel, Field, ValidationError, model_validator
from datetime import datetime
from typing import Optional
from enum import Enum

# ao herdar str, cada valor do enum comporta-se também como uma string normal
# sem str, o comportamento ao imprimir/comparar é ligeiramente diferente.
class ContactType(str, Enum):
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
    def validate_contact(self):
        if self.contact_id[:2] != "AC":
            raise ValueError("Contact ID must start with 'AC'")
        if self.is_verified is False:
            raise ValueError("Physical contact reports must be verified")
        if self.witness_count < 3:
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses"
                )
        if self.signal_strength > 7.0 and self.message_received is NotImplemented:
            raise ValueError("Strong signals (> 7.0) should include received messages")