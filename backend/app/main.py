from fastapi import FastAPI

from app.routers import auth
from app.routers import games
from app.routers import levels
from app.routers import students
from app.routers import challenges
from app.routers import questions
from app.routers import student_progress
from app.routers import achievement_router
from app.routers.student_achievement_router import router as student_achievement_router
from app.routers.game_session_router import router as game_session_router
from app.routers.leaderboard_router import router as leaderboard_router

app = FastAPI(
    title="PyKids Academy API",
    version="0.1.0",
)

app.include_router(auth.router)
app.include_router(students.router)
app.include_router(games.router)
app.include_router(levels.router)
app.include_router(challenges.router)
app.include_router(questions.router)
app.include_router(student_progress.router)
app.include_router(achievement_router.router)
app.include_router(student_achievement_router)
app.include_router(game_session_router)
app.include_router(leaderboard_router)

@app.get("/")
def root():
    return {
        "mensaje": "PyKids Academy funcionando",
        "version": "0.1.0",
    }
