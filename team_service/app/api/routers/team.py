from fastapi import FastAPI, APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List
from app.api.database.database import get_db 
from uuid import UUID as UUIDType
from app.api.model.model import UserModel, TeamModel, TeamMemberModel
from app.api.schemas import UserSchema, TeamSchema, CreateTeamSchema  

app = FastAPI()
router = APIRouter()


@router.get("/teams/", response_model=List[TeamSchema])
async def get_all_teams(db: AsyncSession = Depends(get_db)):
    # Запрос к базе данных для получения всех команд с участниками
    result = await db.execute(
        select(TeamModel).options(selectinload(TeamModel.members))  # Предварительная загрузка участников
    )
    teams = result.scalars().all()

    # Если нет команд, возвращаем ошибку
    if not teams:
        raise HTTPException(status_code=404, detail="No teams found")

    # Формируем и возвращаем результат
    return teams  # Возвращаем все команды с участниками
# Эндпоинт для создания команды
@router.post("/teams/", response_model=TeamSchema)
async def create_team(team: CreateTeamSchema, db: AsyncSession = Depends(get_db)):
    new_team = TeamModel(name=team.name)
    db.add(new_team)
    await db.commit()
    await db.refresh(new_team)

    unique_members = set()

    for username in team.members:
        user_query = await db.execute(select(UserModel).where(UserModel.username == username))
        user = user_query.scalar_one_or_none()

        if user:
            if user.id not in unique_members:
                unique_members.add(user.id)

                member_query = await db.execute(
                    select(TeamMemberModel).where(TeamMemberModel.team_id == new_team.id, TeamMemberModel.user_id == user.id)
                )
                if member_query.scalar_one_or_none() is None:
                    new_team_member = TeamMemberModel(team_id=new_team.id, user_id=user.id)
                    db.add(new_team_member)

                # Обновление team_id у пользователя
                user.team_id = new_team.id
                db.add(user)  # Добавляем пользователя в сессию для фиксации изменений

    await db.commit()
    return await get_team_with_members(db, new_team.id)


async def get_team_with_members(db: AsyncSession, team_id: UUIDType):
    # Получаем команду с участниками
    result = await db.execute(
        select(TeamModel).options(selectinload(TeamModel.members)).where(TeamModel.id == team_id)
    )
    team_with_members = result.scalar_one_or_none()
    return team_with_members

# Добавление пользователя в команду
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

    member_query = await db.execute(select(TeamMemberModel).where(TeamMemberModel.user_id == user.id))
    current_team_member = member_query.scalar_one_or_none()

    if current_team_member:
        current_team_member.team_id = team.id  # Обновляем team_id
    else:
        new_team_member = TeamMemberModel(team_id=team.id, user_id=user.id)
        db.add(new_team_member)

    # Обновляем team_id у пользователя
    user.team_id = team.id
    db.add(user)

    await db.commit()
    await db.refresh(user)  # Обновляем объект в памяти
    return user




# Удаление пользователя из команды
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

    # Удаляем запись из TeamMemberModel
    await db.delete(team_member)

    # Очищаем team_id у пользователя
    user.team_id = None
    db.add(user)

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

    # Запрашиваем команду с предзагрузкой участников
    team_query = await db.execute(
        select(TeamModel).options(selectinload(TeamModel.members)).where(TeamModel.id == user.team_id)
    )
    team = team_query.scalar_one_or_none()

    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    return team