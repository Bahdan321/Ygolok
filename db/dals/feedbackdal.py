import uuid

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from db.models import Organizations, Users
from views.feedback.schemas import CreateFeedback


class FeedbackDAL:

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_feedback(self, schema: CreateFeedback, current_user, table):
        try:
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
        except TypeError as err:
            raise HTTPException(status_code=404, detail='inn not found')

    async def show_feedback_by_id(self, feedback_id: uuid.UUID, inn, table):
        """table - таблица [Reviews/Offers/Complaints]"""
        user_query = select(Users.name).where(Users.id == table.user_id)
        user_res = await self.db_session.execute(user_query)
        user_row = user_res.fetchone()

        org_query = select(Organizations.inn).where(Organizations.inn == inn)
        org_res = await self.db_session.execute(org_query)
        org_row = org_res.fetchone()
        if not org_row:
            raise HTTPException(status_code=404, detail='not found')

        feedback_query = select(table).where(table.id == feedback_id, inn == org_row[0])
        feedback_res = await self.db_session.execute(feedback_query)
        feedback_row = feedback_res.fetchone()

        if not feedback_row or not user_row:
            raise HTTPException(status_code=404, detail='not found')

        return feedback_row[0], user_row[0]

    async def show_feedback_list(self, limit: int, offset: int, org_id: uuid):
        pass
