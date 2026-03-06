from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import httpx
import time
import asyncio
import os
from typing import Dict, List, Any

app = FastAPI(title="Solana Pro API v2")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Mapeo curado de Binance
SOLANA_BINANCE_MAP = {
    "DeFi": ["SOL", "JUP", "RAY", "JTO", "DRIFT", "TNSR", "PYTH"],
    "DePIN": ["RENDER", "HNT", "IO", "AR"],
    "Memecoins": ["WIF", "BONK", "POPCAT", "MEW", "BOME", "MYRO", "PNUT"]
}

# Stablecoins a excluir
STABLES = ["USDT", "USDC", "DAI", "FDUSD", "TUSD", "PYUSD", "USDS", "USTC"]

BINANCE_API = "https://api.binance.com/api/v3/klines"
COINGECKO_API = "https://api.coingecko.com/api/v3/coins/markets"

async def fetch_binance(client: httpx.AsyncClient, symbol: str, interval: str):
    try:
        pair = f"{symbol}USDT"
        res = await client.get(BINANCE_API, params={"symbol": pair, "interval": interval, "limit": 30}, timeout=5.0)
        if res.status_code == 200:
            return [float(item[4]) for item in res.json()]
    except: pass
    return []

@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/v1/data/full")
async def get_full_data():
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            params = {"vs_currency": "usd", "category": "solana-ecosystem", "order": "market_cap_desc", "per_page": 200, "sparkline": "true"}
            cg_res = await client.get(COINGECKO_API, params=params)
            if cg_res.status_code != 200: return JSONResponse(status_code=429, content={"error": "Rate Limit"})
            
            all_tokens = cg_res.json()
            sectors = {s: [] for s in SOLANA_BINANCE_MAP.keys()}
            sectors["Others"] = []
            final_list = []
            assigned_ids = set()
            seen_symbols = set() # CONTROL DE DUPLICADOS

            for token in all_tokens:
                t_id = token.get("id")
                symbol = (token.get("symbol") or "").upper()
                if symbol == "RNDR": symbol = "RENDER"
                
                # Filtros de seguridad
                if symbol in STABLES or symbol in seen_symbols: continue
                
                target_sector = "Others"
                for sector, sym_list in SOLANA_BINANCE_MAP.items():
                    if symbol in sym_list and len(sectors[sector]) < 10:
                        target_sector = sector
                        break
                
                if (target_sector != "Others" or len(sectors["Others"]) < 20) and t_id not in assigned_ids:
                    t_info = {
                        "name": token["name"],
                        "symbol": symbol,
                        "coingecko": {
                            "price": token.get("current_price", 0),
                            "mcap": token.get("market_cap", 0),
                            "vol": token.get("total_volume", 0),
                            "sparkline": token.get("sparkline_in_7d", {}).get("price", [])
                        }
                    }
                    sectors[target_sector].append(t_info)
                    final_list.append(t_info)
                    assigned_ids.add(t_id)
                    seen_symbols.add(symbol)
                    if len(final_list) >= 50: break

            tasks = []
            for t in final_list:
                for intv in ["1h", "4h", "1d"]:
                    tasks.append(fetch_binance(client, t["symbol"], intv))
            
            h_results = await asyncio.gather(*tasks)
            idx = 0
            for t in final_list:
                t["binance"] = {"1h": h_results[idx], "4h": h_results[idx+1], "1d": h_results[idx+2]}
                idx += 3

            return {"status": "success", "total": len(final_list), "sectors": sectors}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
