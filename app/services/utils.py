from sqlalchemy.ext.declarative import DeclarativeMeta
import json

def to_dict(model):
    """
    Convert a SQLAlchemy model instance to a dictionary.
    """
    if not isinstance(model.__class__, DeclarativeMeta):
        raise ValueError("Expected SQLAlchemy model instance.")
    
    model_dict = {}
    for column in model.__table__.columns:
        value = getattr(model, column.name)
        # Exclude the 'mat_khau' field
        if column.name == "mat_khau":
            continue
        # Check if the column name is 'JsonData' and handle it accordingly
        if column.name == "JsonData":
            if isinstance(value, dict):
                model_dict[column.name] = value
            else:
                try:
                    model_dict[column.name] = json.loads(value)
                except (TypeError, ValueError):
                    model_dict[column.name] = value  # If not a JSON string, keep original
        else:
            model_dict[column.name] = value
    return model_dict
