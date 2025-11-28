from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.models import CityModel, TemperatureModel
from app.schemas import CityBase, CityBaseCreate, CityUpdate, TemperatureBase, TemperatureCreate

router = APIRouter()


@router.get("/city/", response_model=list[CityBase])
async def get_cities(
        db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(CityModel))
    return result.scalars().all()


@router.get("/city/{city_id}", response_model=CityBase)
async def get_city(
        city_id: int,
        db: AsyncSession = Depends(get_db),
):
    stmt = select(CityModel).where(CityModel.id == city_id)
    result = await db.execute(stmt)
    city = result.scalars().one_or_none()

    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    return city


@router.post("/city/", response_model=CityBase)
async def create_city(
        city_data: CityBaseCreate,
        db: AsyncSession = Depends(get_db),
):
    city = CityModel(
        name=city_data.name,
        additional_info=city_data.additional_info,
    )
    db.add(city)
    await db.commit()
    await db.refresh(city)
    return city


@router.patch("/city/{city_id}")
async def update_city(
        city_data: CityUpdate,
        city_id: int,
        db: AsyncSession = Depends(get_db),
):
    stmt = select(CityModel).where(CityModel.id == city_id)
    result = await db.execute(stmt)
    city = result.scalars().one_or_none()

    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    for field, value in city_data.model_dump(exclude_unset=True).items():
        setattr(city, field, value)

    await db.commit()
    await db.refresh(city)

    return {"detail": "City updated"}


@router.delete("/city/{city_id}")
async def delete_city(
        city_id: int,
        db: AsyncSession = Depends(get_db),
):
    stmt = select(CityModel).where(CityModel.id == city_id)
    result = await db.execute(stmt)
    city = result.scalars().one_or_none()

    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    await db.delete(city)
    await db.commit()
    return {"detail": "City deleted"}


@router.get("/temperature/", response_model=list[TemperatureBase])
async def get_temperature(
        db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(TemperatureModel))
    return result.scalars().all()


@router.get("/temperature/{temperature_id}", response_model=TemperatureBase)
async def get_temperature_by_id(
        temperature_id: int,
        db: AsyncSession = Depends(get_db),
):
    stmt = select(TemperatureModel).where(TemperatureModel.id == temperature_id)
    result = await db.execute(stmt)
    temperature = result.scalars().one_or_none()
    if not temperature:
        raise HTTPException(status_code=404, detail="Temperature not found")
    return temperature


@router.post("/temperature/", response_model=TemperatureBase)
async def create_temperature(
        temperature_data: TemperatureCreate,
        db: AsyncSession = Depends(get_db),
):
    temperature = TemperatureModel(
        city_id=temperature_data.city_id,
        date_time=temperature_data.date_time,
        temperature=temperature_data.temperature,
    )
    db.add(temperature)
    await db.commit()
    await db.refresh(temperature)
    return temperature
