import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.base import async_session, get_db
from db.dals.feedbackdal import FeedbackDAL
from db.models import Users
from views.auth.login import get_current_user_from_token
from views.feedback.schemas import ShowFeedback, CreateFeedback

from db.models.reviews import Reviews
from db.models.complaints import Complaints
from db.models.offers import Offers

feedback_router = APIRouter()


async def _create_feedback(schema, current_user, db, table):
    async with db as session:
        async with session.begin():
            feedback_dal = FeedbackDAL(session)
            feedback = await feedback_dal.create_feedback(
                schema=schema,
                current_user=current_user,
                table=table
            )

            return {'response: ': 'successful'}


async def _show_feedback_by_id(feedback_id: uuid.UUID, inn: str, table, db: AsyncSession) -> ShowFeedback:
    async with db as session:
        async with session.begin():
            feedback_dal = FeedbackDAL(session)
            review = await feedback_dal.show_feedback_by_id(feedback_id=feedback_id, inn=inn, table=table)

            return ShowFeedback(
                id=review[0].id, user_name=review[1], body=review[0].body, created_at=review[0].created_at
            )


@feedback_router.get('/organization={inn}/review={id}')
async def get_review(feedback_id: uuid.UUID, inn: str, db: AsyncSession = Depends(get_db)) -> ShowFeedback:
    return await _show_feedback_by_id(feedback_id=feedback_id, inn=inn, table=Reviews, db=db)


@feedback_router.get('/organization={inn}/offer={id}')
async def get_offer(feedback_id: uuid.UUID, inn: str, db: AsyncSession = Depends(get_db)) -> ShowFeedback:
    return await _show_feedback_by_id(feedback_id=feedback_id, inn=inn, table=Offers, db=db)


@feedback_router.get('/organization={inn}/complaint={id}')
async def get_complaint(feedback_id: uuid.UUID, inn: str, db: AsyncSession = Depends(get_db)) -> ShowFeedback:
    return await _show_feedback_by_id(feedback_id=feedback_id, inn=inn, table=Complaints, db=db)


@feedback_router.post('/organization={inn}/offers')
async def create_offer(schema: CreateFeedback,
                       db: AsyncSession = Depends(get_db),
                       current_user: Users = Depends(get_current_user_from_token)):
    return await _create_feedback(schema=schema, table=Offers, db=db, current_user=current_user)


@feedback_router.post('/organization={inn}/complaints')
async def create_complaint(schema: CreateFeedback,
                           db: AsyncSession = Depends(get_db),
                           current_user: Users = Depends(get_current_user_from_token)):
    return await _create_feedback(schema=schema, table=Complaints, db=db, current_user=current_user)


@feedback_router.post('/organization={inn}/reviews')
async def create_review(schema: CreateFeedback,
                        db: AsyncSession = Depends(get_db),
                        current_user: Users = Depends(get_current_user_from_token)):
    return await _create_feedback(schema=schema, table=Reviews, db=db, current_user=current_user)
