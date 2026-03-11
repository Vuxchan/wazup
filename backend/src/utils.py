from pydantic import ConfigDict

def to_camel(s: str):
    parts = s.split("_")
    return parts[0] + "".join(p.capitalize() for p in parts[1:])

config = ConfigDict(
    alias_generator=to_camel,
    populate_by_name=True
)