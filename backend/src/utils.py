from pydantic import ConfigDict
from sqlalchemy import inspect

def to_camel(s: str):
    parts = s.split("_")
    return parts[0] + "".join(p.capitalize() for p in parts[1:])

config = ConfigDict(
    alias_generator=to_camel,
    populate_by_name=True
)

def check_loaded_relationships(obj):
    """Kiểm tra relationship nào đã được load"""
    inspector = inspect(obj)
    for attr in inspector.mapper.relationships.keys():
        is_loaded = inspector.attrs[attr].loaded_value
        print(f"{attr}: {'Đã load' if is_loaded else 'Chưa load (sẽ lazy)'}")