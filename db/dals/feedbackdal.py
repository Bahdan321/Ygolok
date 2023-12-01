import uuid

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional


class FeedbackDAL:

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_feedback(self, user_id: uuid.UUID, org_id: uuid.UUID, body: str, table):
        new_feedback = table(user_id=user_id,
                             org_id=org_id,
                             body=body)
        self.db_session.add(new_feedback)
        await self.db_session.flush()
        return new_feedback

    async def show_feedback_by_id(self, feedback_id: uuid.UUID, table):
        """table - таблица [Reviews/Offers/Complaints]"""

        query = select(table).where(table.id == feedback_id)
        res = await self.db_session.execute(query)
        feedback_row = res.fetchone()

        if not feedback_row:
            raise HTTPException(status_code=404, detail='not found')
        print(feedback_row[0])
        return feedback_row[0]

    async def show_feedback_list(self, limit: int, offset: int, org_id: uuid):
        pass
