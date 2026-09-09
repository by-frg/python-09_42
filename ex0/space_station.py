#!/usr/bin/env python3
from pydantic import BaseModel, Field, ValidationError
from datetime import datetime
from typing import Optional


# gt - greater than
# ge - greater or equal
# le - lower or equal
class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: Optional[str] = Field(None, max_length=200)


def main() -> None:
    try:
        valid_station = SpaceStation(  # type: ignore[call-arg]
            station_id="ISS001",
            name="International Space Station",
            crew_size=6,
            last_maintenance="2026-06-13",  # type: ignore[arg-type]
            power_level=85.5,
            oxygen_level=92.3,
            is_operational=True,
        )
        print("===================================")
        print(
            "Valid station created:\n"
            f"ID: {valid_station.station_id}\n"
            f"Name: {valid_station.name}\n"
            f"Crew: {valid_station.crew_size} people\n"
            f"Power: {valid_station.power_level}%\n"
            f"Oxygen: {valid_station.oxygen_level}%\n"
            )
        if valid_station.is_operational:
            print("Status: Operational")
        else:
            print("Status: Not operational")
        print("\n===================================")

        print("Expected Validation Error:")

        # testing invalid data input
        SpaceStation(  # type: ignore[call-arg]
            station_id="ISS001",
            name="International Space Station",
            crew_size=21,
            last_maintenance="2026-07-03",  # type: ignore[arg-type]
            power_level=101,
            oxygen_level=92.3,
            is_operational=True,
        )
    # errors is a list of dictionaries. I want the msg of every dictionary 'e'
    except ValidationError as err:
        for e in err.errors():
            print(e["msg"])


if __name__ == "__main__":
    print("Space Station Data Validation")
    main()
