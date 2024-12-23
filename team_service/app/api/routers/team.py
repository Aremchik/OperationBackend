from fastapi import FastAPI, APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List
from app.api.database.database import get_db 
from app.api.model.model import UserModel, TeamModel, TeamMemberModel
from app.api.schemas import UserSchema, TeamSchema, CreateTeamSchema  

app = FastAPI()
router = APIRouter()


@router.get("/teams/", response_model=List[TeamSchema])
async def get_all_teams(db: AsyncSession = Depends(get_db)):
    # Запрос к базе данных для получения всех команд с участниками
    result = await db.execute(
        select(TeamModel).options(selectinload(TeamModel.members))  # Предварительно загружаем участников
    )
    teams = result.scalars().all()

    # Если нет команд, возвращаем ошибку
    if not teams:
        raise HTTPException(status_code=404, detail="No teams found")

    # Формируем список команд с пользователями
    return teams  # Возвращаем все команды с участниками
# Эндпоинт для создания команды
@router.post("/teams/", response_model=TeamSchema)
async def create_team(team: CreateTeamSchema, db: AsyncSession = Depends(get_db)):
    # Создаем команду
    new_team = TeamModel(name=team.name)
    db.add(new_team)
    await db.commit()
    await db.refresh(new_team)

    # Добавляем участников в команду
    existing_user_ids = set()
    for username in team.members:
        user_query = await db.execute(select(UserModel).where(UserModel.username == username))
        user = user_query.scalar_one_or_none()

        if user:
            existing_user_ids.add(user.id)  # Сохраняем уже существующих пользователей

            # Проверяем, существует ли эта запись в team_members
            member_query = await db.execute(
                select(TeamMemberModel).where(TeamMemberModel.team_id == new_team.id, TeamMemberModel.user_id == user.id)
            )
            existing_member = member_query.scalar_one_or_none()

            if not existing_member:
                # Добавляем только если участник еще не добавлен
                new_team_member = TeamMemberModel(team_id=new_team.id, user_id=user.id)
                db.add(new_team_member)

    await db.commit()

    # Возвращаем команду с участниками
    return await get_team_with_members(db, new_team.id)

async def get_team_with_members(db: AsyncSession, team_id: UUIDType):
    # Получаем команду с участниками
    result = await db.execute(
        select(TeamModel).options(selectinload(TeamModel.members)).where(TeamModel.id == team_id)
    )
    team_with_members = result.scalar_one_or_none()
    return team_with_members

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