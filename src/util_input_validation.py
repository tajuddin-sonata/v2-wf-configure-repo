# JSONSchema for Request Body validation
schema = {
    "type": "object",
    "properties": {
        "context": {
            "type": "object",
            "properties": {
                "azure_subscription": {"type": "string"},
                "azure_location": {"type": "string"},
                "client_id": {"type": "string"},
                "execution_id": {"type": "string"},
                "execution_start": {"type": "string"},
            },
            "required": ["client_id"],
        },
        "input_files": {
            "type": "object",
            "properties": {
                "source_file": {"$ref": "#/$defs/file"},
            },
            "required":["source_file"]
        },
        "function_config": {
            "type": "object",
            "properties": {
                "label_tags": {
                    "type": "object",
                    "properties": {
                        "client": {"type": "string"},
                        "step": {"type": "string"},
                        "type": {"type": "string"},
                    },
                    "required": ["client", "step", "type"],
                },
                "functions": {
                    "type": "object",
                    "patternProperties": {
                        ".*": {
                            "type": "array",
                            "items": {"type": "string"},
                            "minItems": 1,
                        }
                    },
                },
                "config_bucket_name": {"type": "string"},
            },
            "required": ["functions", "config_bucket_name"],
        },
    },
    "required": ["context", "function_config"],
    "$defs": {
        "file": {
            "type": "object",
            "properties": {
                "bucket_name": {"type": "string"},
                "full_path": {"type": "string"},
                "version": {"type": "string"},
                "size": {"type": "string"},
                "content_type": {"type": "string"},
                "uploaded": {"type": "string"},
            },
            "required": ["bucket_name", "full_path", "version"],
        }
    },
}


from datetime import datetime
from typing import Any
from ciso8601 import parse_datetime
from json import dumps, loads
# from jsonschema import validate, ValidationError


def jsonify(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    else:
        return obj.__dict__

class Jsonable(object):
    def __repr__(self):
        return dumps(self, default=jsonify, indent=4)

    def toJson(self):
        return loads(repr(self))

    def __contains__(self, attr):
        return attr in self.__dict__
        
    def __getitem__(self, attr):
        return self.__dict__[attr]
    
    def keys(self):
        return self.__dict__.keys()

    def items(self):
        return self.__dict__.items()
    
# class Config(Jsonable):
#     def __init__(self, req):
#         try:
#             validate(req, schema)  # Validate against the defined schema
#             self.context = self.Context(req["context"])
#             self.input_files = self.InputFiles(req["input_files"]) if "input_files" in req else None
#             self.function_config = self.FunctionConfig(req["function_config"])
#         except ValidationError as e:
#             raise ValueError(f"Invalid request format: {e}")

class Config(Jsonable):
    def __init__(self, req):
        self.context = self.Context(req["context"])
        self.input_files = self.InputFiles(req["input_files"]) if "input_files" in req else None
        self.function_config = self.FunctionConfig(req["function_config"])

    class Context(Jsonable):
        def __init__(self, c):
            self.azure_subscription = str(c["azure_subscription"]) if "azure_subscription" in c else None
            self.azure_location = str(c["azure_location"]) if "azure_location" in c else None
            self.client_id = str(c["client_id"])
            self.execution_id = str(c["execution_id"]) if "execution_id" in c else None
            self.execution_start=parse_datetime(str(c["execution_start"])) if "execution_start" in c else None

    class InputFiles(Jsonable):
        def __init__(self, c):
            # for f in c:
            #     setattr(self, str(f["tag"]), self.InputFile(f))
            self.source_file=self.InputFile(c["source_file"])

        class InputFile(Jsonable):
            def __init__(self, c):
                self.bucket_name = str(c["bucket_name"])
                self.full_path = str(c["full_path"])
                # self.version = int(c["version"])
                self.version = c["version"]  ########## removed int
                self.size = int(c["size"]) if "size" in c else None
                self.content_type = str(c["content_type"]) if "content_type" in c else None
                self.uploaded=parse_datetime(str(c["uploaded"])) if "uploaded" in c else None

    class FunctionConfig(Jsonable):
        def __init__(self, c):
            self.config_bucket_name = str(c["config_bucket_name"])
            self.functions = self.Functions(c["functions"])
            self.label_tags = (
                self.LabelTags(c["label_tags"]) if "label_tags" in c else None
            )

        class Functions(Jsonable):
            def __init__(self, c):
                for f, v in c.items():
                    setattr(self, f, list(v))

        class LabelTags(Jsonable):
            def __init__(self, c):
                self.client = str(c["client"])
                self.step = str(c["step"])
                self.type = str(c["type"])
