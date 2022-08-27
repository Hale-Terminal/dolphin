import json

from fastapi import APIRouter


router = APIRouter()

equities = {
    "result": [
        {"id": 1, "ticker": "AAPL", "name": "Apple", "description": "Apple Description"},
        {"id": 2, "ticker": "GOOG", "name": "Google", "description": "Google Description"},
        {"id": 3, "ticker": "TSLA", "name": "Tesla", "description": "Tesla Description"},
    ]
}


@router.get("")
def search():
    msg = {"id": 1, "ticker": "AAPL", "name": "Apple", "description": "Apple Description"}
    return msg
