import uuid
from fastapi import APIRouter

from db.base import async_session
from db.dals.feedbackdal import FeedbackDAL
from views.feedback.schemas import ShowFeedback

from db.models.reviews import Reviews
from db.models.complaints import Complaints
from db.models.offers import Offers

feedback_router = APIRouter()


async def _show_review_by_id(review_id: uuid.UUID) -> ShowFeedback:
    async with async_session() as session:
        async with session.begin():
            feedback_dal = FeedbackDAL(session)
            review = await feedback_dal.show_feedback_by_id(feedback_id=review_id, table=Reviews)

            return ShowFeedback(
                id=review.id, user_name=review.user_name, body=review.body, created_at=review.created_at
            )


async def _show_offer_by_id(offer_id: uuid.UUID) -> ShowFeedback:
    async with async_session() as session:
        async with session.begin():
            feedback_dal = FeedbackDAL(session)
            offer = await feedback_dal.show_feedback_by_id(feedback_id=offer_id, table=Offers)

            return ShowFeedback(
                id=offer.id, user_name=offer.user_name, body=offer.body, created_at=offer.created_at
            )


async def _show_complaint_by_id(complaint_id: uuid.UUID) -> ShowFeedback:
    async with async_session() as session:
        async with session.begin():
            feedback_dal = FeedbackDAL(session)
            complaint = await feedback_dal.show_feedback_by_id(feedback_id=complaint_id, table=Complaints)

            return ShowFeedback(
                id=complaint.id, user_name=complaint.user_name, body=complaint.body, created_at=complaint.created_at
            )


@feedback_router.get('/review/{id}')
async def get_review(review_id: uuid.UUID) -> ShowFeedback:
    return await _show_review_by_id(review_id)


@feedback_router.get('/offer/{id}')
async def get_review(offer_id: uuid.UUID) -> ShowFeedback:
    return await _show_offer_by_id(offer_id)


@feedback_router.get('/complaint/{id}')
async def get_review(complaint_id: uuid.UUID) -> ShowFeedback:
    return await _show_complaint_by_id(complaint_id)