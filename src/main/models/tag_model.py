from mypy_extensions import TypedDict

TagModel = TypedDict('TagModel', {
    'type': str,
    'value': str,
    'confidence': int,
    'isPrimary': bool
})

NLPEntityModel = TypedDict('NLPEntityModel', {
    'text': str,
    'type': str,
    'start_char': int,
    'end_char': int
})
