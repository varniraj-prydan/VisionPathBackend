from fastapi import FastAPI
import os

app = FastAPI(title="Voice Learning Tutor API")

@app.get("/")
async def health_check():
    return {"status": "healthy", "service": "Voice Learning Tutor API", "port": os.getenv("PORT", "8000")}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/test")
async def test_endpoint():
    return {"message": "API is working!"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    print(f"Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)