import uuid

from fastapi import APIRouter

from db.base import async_session
from db.dals.org_docdal import OrgDocDAL
from views.org_docs.schemas import OrgDoc

from db.models.organizationdocuments import OrganizationDocument
from db.models.organizations import Organizations
from db.models.owners import Owners

org_doc_router = APIRouter()

async def _show_all_org_docs(org_id: uuid.UUID) -> OrgDoc:
    async with async_session() as session:
        async with session.begin():
            org_doc_dal = OrgDocDAL(session)
            org_docs = await org_doc_dal.show_all_org_docs(org_id=org_id, table=OrganizationDocument)

            return OrgDoc(
                id=org_id,
                doc_title=org_docs.doc_title,
                address=org_docs.address,
                documet=org_docs.document
            )

@org_doc_router.get('/org_docs/{org_id}')
async def get_all_org_docs(org_id: uuid.UUID) -> OrgDoc:
    return await _show_all_org_docs(org_id)
