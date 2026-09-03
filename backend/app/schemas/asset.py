from pydantic import BaseModel

class AssetSearchResult(BaseModel):
    ticker: str
    name: str
    sector: str | None = None