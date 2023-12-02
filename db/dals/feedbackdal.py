import uuid

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from db.models import Organizations
from views.feedback.schemas import CreateFeedback


class FeedbackDAL:

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_feedback(self, schema: CreateFeedback, current_user, table):
        query = select(Organizations.id).where(Organizations.inn == schema.inn)
        res = await self.db_session.execute(query)
        org_id = res.fetchone()[0]
        print(org_id)
        new_feedback = table(user_id=current_user.id,
                             org_id=org_id,
                             body=schema.body)
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
