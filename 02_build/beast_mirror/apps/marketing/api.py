from fastapi import FastAPI
app = FastAPI(title="Amplified Marketing Engine")

@app.get("/health")
async def health():
    return {"status": "ok", "service": "marketing-engine"}
