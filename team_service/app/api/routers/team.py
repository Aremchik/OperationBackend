from fastapi import FastAPI, APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.api.database.database import get_db  # Импорт вашей базы данных
from app.api.model.model import UserModel, TeamModel, TeamMemberModel
from app.api.schemas import UserSchema, TeamSchema, CreateTeamSchema  # Ваши схемы


app = FastAPI()
router = APIRouter()

# Эндпоинт для получения всех команд
@router.get("/teams/", response_model=List[TeamSchema])
async def get_all_teams(db: AsyncSession = Depends(get_db)):
    # Запрос к базе данных для получения всех команд
    result = await db.execute(select(TeamModel))
    teams = result.scalars().all()

    # Если нет команд, возвращаем ошибку
    if not teams:
        raise HTTPException(status_code=404, detail="No teams found")

    # Запрашиваем участников для каждой команды через связь с TeamMemberModel
    for team in teams:
        team_members_query = await db.execute(
            select(UserModel.username).join(TeamMemberModel).where(TeamMemberModel.team == team.id)
        )
        team.members = team_members_query.scalars().all()  # Заполняем поле members

    # Возвращаем все команды с участниками
    return teams


# Эндпоинт для создания команды
@router.post("/teams/", response_model=TeamSchema)
async def create_team(team: CreateTeamSchema, db: AsyncSession = Depends(get_db)):
    # Проверяем существование команды с таким именем
    existing_team_query = await db.execute(select(TeamModel).where(TeamModel.name == team.name))
    existing_team = existing_team_query.scalar_one_or_none()
    if existing_team:
        raise HTTPException(status_code=400, detail="Team with this name already exists")

    # Проверяем существование участников
    user_query = await db.execute(select(UserModel).where(UserModel.username.in_(team.members)))
    users = user_query.scalars().all()

    if len(users) != len(team.members):
        missing_users = set(team.members) - {user.username for user in users}
        raise HTTPException(status_code=404, detail=f"Some users not found: {', '.join(missing_users)}")

    # Создаём команду
    new_team = TeamModel(name=team.name)
    db.add(new_team)
    await db.commit()
    await db.refresh(new_team)

    # Добавляем участников в команду
    for user in users:
        new_team_member = TeamMemberModel(team_id=new_team.id, user_id=user.id)
        db.add(new_team_member)

    await db.commit()

    # Получаем всех участников команды через связь с таблицей TeamMemberModel
    team_members_query = await db.execute(
        select(UserModel.username).join(TeamMemberModel).where(TeamMemberModel.team_id == new_team.id)
    )
    team_members = team_members_query.scalars().all()

    # Обновляем команду с участниками, добавляем их в поле 'members'
    new_team.members = team_members

    # Возвращаем команду с участниками
    return new_team


# Добавление пользователя в команду
@router.patch("/users/{username}/team/{team_id}", response_model=UserSchema)
async def add_user_to_team(username: str, team_id: str, db: AsyncSession = Depends(get_db)):
    user_query = await db.execute(select(UserModel).where(UserModel.username == username))
    user = user_query.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    team_query = await db.execute(select(TeamModel).where(TeamModel.id == team_id))
    team = team_query.scalar_one_or_none()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    # Добавляем пользователя в таблицу TeamMemberModel
    new_team_member = TeamMemberModel(team_id=team.id, user_id=user.id)
    db.add(new_team_member)
    await db.commit()
    await db.refresh(user)

    return user


# Удаление пользователя из команды
@router.delete("/users/{username}/team/{team_id}", response_model=UserSchema)
async def remove_user_from_team(username: str, team_id: str, db: AsyncSession = Depends(get_db)):
    user_query = await db.execute(select(UserModel).where(UserModel.username == username))
    user = user_query.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    team_member_query = await db.execute(
        select(TeamMemberModel).where(TeamMemberModel.user_id == user.id, TeamMemberModel.team_id == team_id)
    )
    team_member = team_member_query.scalar_one_or_none()
    if not team_member:
        raise HTTPException(status_code=404, detail="User is not part of this team")

    await db.delete(team_member)
    await db.commit()
    await db.refresh(user)
    return user


# Получение команды конкретного пользователя
@router.get("/users/{username}/team", response_model=TeamSchema)
async def get_user_team(username: str, db: AsyncSession = Depends(get_db)):
    user_query = await db.execute(select(UserModel).where(UserModel.username == username))
    user = user_query.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.team_id:
        raise HTTPException(status_code=404, detail="User does not belong to any team")

    team_query = await db.execute(select(TeamModel).where(TeamModel.id == user.team_id))
    team = team_query.scalar_one_or_none()

    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    return team
