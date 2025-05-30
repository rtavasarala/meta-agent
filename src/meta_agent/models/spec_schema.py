import json
import yaml
from pathlib import Path
from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import Optional, Dict, List, Any, Union

class SpecSchema(BaseModel):
    """Data model for agent specifications."""
    task_description: str = Field(..., description="Detailed description of the agent's task and requirements.")
    inputs: Optional[Dict[str, str]] = Field(default=None, description="Specification of expected inputs, e.g., {'input_name': 'type'}.")
    outputs: Optional[Dict[str, str]] = Field(default=None, description="Specification of expected outputs, e.g., {'output_name': 'type'}.")
    constraints: Optional[List[str]] = Field(default=None, description="List of constraints or assumptions.")
    technical_requirements: Optional[List[str]] = Field(default=None, description="Specific technical requirements, e.g., libraries, frameworks.")
    metadata: Optional[Dict[str, str]] = Field(default=None, description="Optional metadata fields.")

    @field_validator('task_description')
    @classmethod
    def task_description_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Task description must not be empty')
        return v

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SpecSchema':
        """Creates a SpecSchema instance from a dictionary."""
        try:
            return cls(**data)
        except ValidationError as e:
            # Re-raise or handle specific validation errors
            print(f"Error validating spec data from dict: {e}")
            raise

    @classmethod
    def from_json(cls, json_input: Union[str, Path]) -> 'SpecSchema':
        """Creates a SpecSchema instance from a JSON string or file path."""
        data: Dict[str, Any]
        try:
            if isinstance(json_input, Path) or Path(json_input).is_file():
                file_path = Path(json_input)
                if not file_path.exists():
                    raise FileNotFoundError(f"JSON file not found: {file_path}")
                with file_path.open('r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                # Assume it's a JSON string
                data = json.loads(str(json_input))
            return cls.from_dict(data)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            raise
        except (FileNotFoundError, ValidationError) as e:
            print(f"Error processing JSON input: {e}")
            raise

    @classmethod
    def from_yaml(cls, yaml_input: Union[str, Path]) -> 'SpecSchema':
        """Creates a SpecSchema instance from a YAML string or file path."""
        data: Dict[str, Any]
        try:
            if isinstance(yaml_input, Path) or Path(yaml_input).is_file():
                file_path = Path(yaml_input)
                if not file_path.exists():
                    raise FileNotFoundError(f"YAML file not found: {file_path}")
                with file_path.open('r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
            else:
                # Assume it's a YAML string
                data = yaml.safe_load(str(yaml_input))
            
            if not isinstance(data, dict):
                raise TypeError("YAML content did not parse into a dictionary.")
                
            return cls.from_dict(data)
        except yaml.YAMLError as e:
            print(f"Error decoding YAML: {e}")
            raise
        except (FileNotFoundError, ValidationError, TypeError) as e:
            print(f"Error processing YAML input: {e}")
            raise

    @classmethod
    def from_text(cls, text_input: str) -> 'SpecSchema':
        """(Placeholder) Creates a SpecSchema instance from free-form text."""
        # TODO: Implement actual NLP parsing for free-form text (Task 1.3)
        print("Warning: from_text is a placeholder. Using basic task description.")
        return cls(task_description=text_input.strip())

    # TODO: Add more specific validation methods as needed
    # TODO: Add helper methods (e.g., for merging specs)
    # TODO: Add serialization/deserialization methods (if needed beyond Pydantic defaults)
