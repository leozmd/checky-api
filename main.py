# Librerías
from fastapi import FastAPI, Response, status
from dotenv import load_dotenv

# Routes
from routes.RoutesAnswer import answer
from routes.RoutesCareer import career
from routes.RoutesChoice import choice
from routes.RoutesClassroom import classroom
from routes.RoutesCourse import course
from routes.RoutesGrade import grade
from routes.RoutesGroup import group
from routes.RoutesList import list
from routes.RoutesLogin import login
from routes.RoutesMember import member
from routes.RoutesQuestion import question
from routes.RoutesRecord import record
from routes.RoutesRole import role
from routes.RoutesSchedule import schedule
from routes.RoutesScheduleClassroom import schedule_classroom
from routes.RoutesShift import shift
from routes.RoutesStatus import status
from routes.RoutesUser import user

app = FastAPI(
    title="Checky API",
    description="API for Checky web and mobile apps",
    version="1.0"
)

load_dotenv()


app.include_router(answer)
app.include_router(career)
app.include_router(choice)
app.include_router(classroom)
app.include_router(course)
app.include_router(grade)
app.include_router(group)
app.include_router(list)
app.include_router(login)
app.include_router(member)
app.include_router(question)
app.include_router(record)
app.include_router(role)
app.include_router(schedule)
app.include_router(schedule_classroom)
app.include_router(shift)
app.include_router(status)
app.include_router(user)


@app.get('/')
async def index():
    return {
        "msg": "Bienvenido a la API para Checky, visite /docs para ver la documentacion de esta API"
    }


@app.get('/hack/{inst}', status_code=418)
async def hack(inst: str):
    return {
        "msg": f"¿En serio crees que puedo hackear {inst}? Soy una simple API, válgame Bill Gates."
    }
