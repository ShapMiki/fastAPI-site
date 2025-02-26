from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from cars.router import router as cars_router
from users.router import router as users_router
from pages.router import router as pages_router
from images.router import router as images_router
from chat.router import router as chats_router #В разработкe

from config import settings
from scheduler import Scheduler

#uvicorn app.main:app --reload
#uvicorn app.main:app --host  87.252.252.226 --port 3333 --reload



app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

#Подключение роутеров
app.include_router(users_router)
app.include_router(cars_router)
app.include_router(pages_router)
app.include_router(images_router)

app.include_router(chats_router) #В разработке



scheduler = Scheduler()


@app.get("/")
def read_root():
    return RedirectResponse(url="/pages/")

origins = [
    "http://localhost",
    "http://localhost:8080"
    "http://shap.software",
    "http://87.252.252.226:3333",
    "http://192.168.1.100"
    ]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

scheduler.start()





"""
class SBooking(BaseModel):
    id: int
    name: str
    password: str
    number: str

@app.post("/send_date")
def pipl(book: SBooking):
    return book"""

"""
@app.get('/popas/{popas_id}')
def get_popka(popas_id: int, kaktus: int,  stars: Optional[int] = Query(None, ge=0, le=5)):
    return f"Popas {popas_id} - {kaktus} \n {stars}"
@app.get('/pop')
def get_poka():
    return f"Popas"
"""


