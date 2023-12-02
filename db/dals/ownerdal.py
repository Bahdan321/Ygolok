from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from db.models.owners import Owners


class OwnerDAL:

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    @staticmethod
    def __validate_owner_inn(inn: str):
        if len(inn) != 12 or not inn.isdigit():
            raise HTTPException(status_code=400, detail="invalid inn")

        coefficients1 = [7, 2, 4, 10, 3, 5, 9, 4, 6, 8]
        coefficients2 = [3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8]

        control_sum1 = sum(int(inn[i]) * coefficients1[i] for i in range(10)) % 11 % 10
        control_sum2 = sum(int(inn[i]) * coefficients2[i] for i in range(11)) % 11 % 10

        if not(str(control_sum1) == inn[10] and str(control_sum2) == inn[11]):
            raise HTTPException(status_code=400, detail="invalid inn")

        return inn

    async def create_owner(
        self,
        name: str, last_name: str, patronymic: Optional[str],
        phone: str, inn: str, ogrn: str,
        password_id: str,
    ) -> Owners:
        self.__validate_owner_inn(inn)
        new_owner = Owners(
            name=name,
            last_name=last_name,
            patronymic=patronymic,
            phone=phone,
            inn=inn,
            ogrn=ogrn,
            is_verified=False,
            password_id=password_id,
        )
        self.db_session.add(new_owner)
        await self.db_session.flush()
        return new_owner

    async def get_owner_by_phone(self, phone: str) -> Optional[Owners]:
        query = select(Owners).where(Owners.phone == phone)
        res = await self.db_session.execute(query)
        owner_row = res.fetchone()
        print(owner_row)
        if owner_row:
            return owner_row[0]

    async def get_owner_by_inn(self, inn: str) -> Optional[Owners]:
        query = select(Owners).where(Owners.inn == inn)
        res = await self.db_session.execute(query)
        owner_row = res.fetchone()
        print(owner_row)
        if owner_row:
            return owner_row[0]
