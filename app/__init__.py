from app.main import get_app
import uvicorn

app = get_app()

uvicorn.run(app)