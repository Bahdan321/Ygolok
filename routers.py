from fastapi import APIRouter

from views.auth.register import user_register_router
from views.auth.login import user_login_router
from views.auth_owner.register import owner_register_router
from views.auth_owner.login import owner_login_router
from views.feedback.feedbackRouter import feedback_router
from views.organization.organizationRouter import organization_router
from views.org_docs.org_doc_ownerRouter import org_doc_router

main_api_router = APIRouter(prefix='/v1')


main_api_router.include_router(user_register_router, prefix='/user/register',)
main_api_router.include_router(user_login_router, prefix='/user/auth')
main_api_router.include_router(owner_register_router, prefix='/owner/register')
main_api_router.include_router(owner_login_router, prefix='/owner/auth')
main_api_router.include_router(feedback_router, prefix='/feedback', tags=['feedback'])
main_api_router.include_router(organization_router, prefix='/organizations', tags=['organizations'])
main_api_router.include_router(org_doc_router, prefix='/org_docs', tags=['org_docs'])


