from fastapi import FastAPI

app = FastAPI(
    title="DataParity",
    description="Local-first structured data quality and change analysis platform",
    version="0.1.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
