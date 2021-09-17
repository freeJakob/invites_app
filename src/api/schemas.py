import pydantic


class BPInfo(pydantic.BaseModel):
    destination: str
    address: str
    boarding_datetime: str


class User(pydantic.BaseModel):
    id: int
    name: str
    distance: str
    hours: str


class CheckInCode(pydantic.BaseModel):
    value: str
