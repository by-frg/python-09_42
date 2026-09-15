#!/usr/bin/env python3
from pydantic import BaseModel, Field, ValidationError, model_validator
from datetime import datetime
from enum import Enum


class Rank (Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode='after')
    def validate_mission(self) -> "SpaceMission":
        if self.mission_id[0] != "M":
            raise ValueError("Mission ID must start with 'M'")

        has_ranked_official = False
        for member in self.crew:
            if (member.rank.value == "commander"
                    or member.rank.value == "captain"):
                has_ranked_official = True
                break
        if not has_ranked_official:
            raise ValueError("Must have at least one Commander or Captain")

        half_crew = 0.5 * len(self.crew)
        exp_crew = 0
        if self.duration_days > 365:
            for member in self.crew:
                if member.years_experience >= 5:
                    exp_crew += 1
            if exp_crew < half_crew:
                raise ValueError(
                    "Long missions (> 365 days) need"
                    " 50% experienced crew (5+ years)"
                    )

        for member in self.crew:
            if not member.is_active:
                raise ValueError("All crew members must be active")
            break

        return self


def main() -> None:
    try:
        crew_member1 = CrewMember(
            member_id="SACON",
            name="Sarah Connor",
            rank="commander",  # type: ignore[arg-type]
            age=50,
            specialization="Mission Command",
            years_experience=30,
            is_active=True,
        )
        crew_member2 = CrewMember(
            member_id="JOSMI",
            name="John Smith",
            rank="lieutenant",  # type: ignore[arg-type]
            age=41,
            specialization="Navigation",
            years_experience=20,
            is_active=True,
        )
        crew_member3 = CrewMember(
            member_id="ALJON",
            name="Alice Jonhson",
            rank="officer",  # type: ignore[arg-type]
            age=35,
            specialization="Engineering",
            years_experience=4,
            is_active=True,
        )
        valid_mission = SpaceMission(
                mission_id="M2024_MARS",
                mission_name="Mars Colony Establishment",
                destination="Mars",
                launch_date="2024-04-24T09:00:00",  # type: ignore[arg-type]
                duration_days=900,
                crew=[crew_member1, crew_member2, crew_member3],
                budget_millions=2500,
        )

        print("=============================")
        print("Valid mission created")
        print(
            f"Mission: {valid_mission.mission_name}\n"
            f"ID: {valid_mission.mission_id}\n"
            f"Destination: {valid_mission.destination}\n"
            f"Duration: {valid_mission.duration_days} days\n"
            f"Budget: ${valid_mission.duration_days}M\n"
            f"Crew size: {len(valid_mission.crew)}\n"
            f"Mission Status: {valid_mission.mission_status}\n"
            f"Crew members:"
        )
        for member in valid_mission.crew:
            print(
                f"-{member.name} ({member.rank.value})-{member.specialization}"
                )

        print("\n=============================")

        # invalid data input
        print("Expected validation error")

        crew_member4 = CrewMember(
            member_id="PETSTE",
            name="Peter Stein",
            rank="cadet",  # type: ignore[arg-type]
            age=21,
            specialization="Trainee",
            years_experience=15,
        )

        SpaceMission(
            mission_id="M2024_VENUS",
            mission_name="Venus Attempt Landing",
            destination="Venus",
            launch_date="2024-12-24T09:00:00",  # type: ignore[arg-type]
            duration_days=366,
            crew=[crew_member4, crew_member2, crew_member3],
            budget_millions=2200,
        )
    except ValidationError as err:
        for e in err.errors():
            print(e["msg"])


if __name__ == "__main__":
    print("Space Mission Crew Validation")
    main()
