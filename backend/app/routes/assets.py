from fastapi import APIRouter, HTTPException
from app.services.market_data import get_asset_info
from app.schemas.asset import AssetSearchResult

router = APIRouter(prefix='/assets', tags=['assets'])

@router.get("/search", response_model=list[AssetSearchResult])
def search_assets(q: str):
    try:
        info = get_asset_info(q)
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Asset info not found for ticker {q}")

    return [{
        "ticker": info.get("symbol", q.upper()),
        "name": info.get("instrument_name", "Unknown"),
        "sector": info.get("sector")
    }]