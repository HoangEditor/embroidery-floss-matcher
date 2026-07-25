"""
Embroidery Floss Matcher API
"""
import json
from pathlib import Path
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
DATA_FILE = Path(__file__).resolve().parent / "colors.json"

with open(DATA_FILE) as f:
    COLORS = json.load(f)
COLOR_MAP = {c["code"]: c for c in COLORS}

BRANDS = [
    {"id":"dmc","name":"DMC","color":"#e4002b"},
    {"id":"anchor","name":"Anchor","color":"#0072ce"},
    {"id":"cosmo","name":"Cosmo","color":"#ec6608"},
    {"id":"jp_coats","name":"J&P Coats","color":"#009639"},
]

app = FastAPI(title="Embroidery Floss Matcher", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/api/health")
def health():
    return {"status":"ok","colors":len(COLORS),"brands":len(BRANDS)}

@app.get("/api/brands")
def brands():
    return {"brands":BRANDS}

@app.get("/api/search")
def search(q: str = Query(...)):
    q = q.strip().upper()
    if q in COLOR_MAP:
        return {"found":True,"color":COLOR_MAP[q]}
    matches = [c for c in COLORS if c["code"].upper().startswith(q)][:12]
    return {"found":False,"suggestions":matches}

@app.get("/api/color/{code}")
def get_color(code: str):
    code = code.strip().upper()
    if code in COLOR_MAP:
        return {"found":True,"color":COLOR_MAP[code]}
    return {"found":False}

@app.get("/api/all")
def all_colors(q: str = Query(None), limit: int = Query(100, le=500)):
    if q:
        q = q.lower()
        results = [c for c in COLORS if q in c["code"].lower() or q in c["name"].lower()][:limit]
    else:
        results = COLORS[:limit]
    return {"colors":results,"count":len(results)}

@app.get("/", response_class=HTMLResponse)
def frontend():
    path = STATIC_DIR / "index.html"
    if path.exists():
        return path.read_text(encoding="utf-8")
    return "<h1>Embroidery Floss Matcher</h1>"


@app.get("/blog/{slug}", response_class=HTMLResponse)
def blog_post(slug: str):
    path = STATIC_DIR / "blog" / f"{slug}.html"
    if path.exists():
        return path.read_text(encoding="utf-8")
    raise HTTPException(404, "Blog post not found")


@app.get("/blog", response_class=HTMLResponse)
def blog_index():
    path = STATIC_DIR / "blog" / "index.html"
    if path.exists():
        return path.read_text(encoding="utf-8")
    return "<h1>Blog</h1><p>No posts yet.</p>"


if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
