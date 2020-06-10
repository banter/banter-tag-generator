from enum import Enum


class TagKeys(Enum):
    TYPE = "type"
    VALUE = "value"
    CONFIDENCE = "confidence"
    ISPRIMARY = 'isPrimary'


class BaseTagTypes(Enum):
    PERSON = "person"
