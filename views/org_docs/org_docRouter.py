from fastapi import APIRouter
from typing import Optional, Dict, Any
from uuid import UUID

from db.base import async_session
from db.dals.org_docdal import OrgDocDAL
from views.org_docs.schemas import OrgDoc

org_doc_router = APIRouter()


async def _create_new_org_doc(org_id: UUID, doc_title: str, address: str, document: str) -> Dict[str, Any]:
    async with async_session() as session:
        async with session.begin():
            org_doc_dal = OrgDocDAL(session)
            new_org_doc = await org_doc_dal.create_org_doc(org_id=org_id, doc_title=doc_title, address=address, document=document)

            return {
                "id": new_org_doc.id,
                "doc_title": new_org_doc.doc_title,
                "address": new_org_doc.address,
                "document": new_org_doc.document
            }


async def _delete_org_doc(org_id: UUID, doc_id: int) -> None:
    async with async_session() as session:
        async with session.begin():
            org_doc_dal = OrgDocDAL(session)
            await org_doc_dal.delete_org_doc(org_id=org_id, doc_id=doc_id)


async def _show_all_org_docs(org_id: UUID) -> Optional[list[Dict[str, Any]]]:
    async with async_session() as session:
        async with session.begin():
            org_doc_dal = OrgDocDAL(session)
            org_docs = await org_doc_dal.show_all_org_docs(org_id=org_id)

            if org_docs:
                return [
                    {
                        "id": org_doc.id,
                        "doc_title": org_doc.doc_title,
                        "address": org_doc.address,
                        "document": org_doc.document
                    }
                    for org_doc in org_docs
                ]
            else:
                return None


@org_doc_router.post('//organizations/org_docs/{org_id}')
async def create_new_org_doc(org_id: UUID, org_doc: OrgDoc) -> Dict[str, Any]:
    doc_title = org_doc.doc_title
    address = org_doc.address
    document = org_doc.document
    return await _create_new_org_doc(org_id=org_id, doc_title=doc_title, address=address, document=document)


@org_doc_router.delete('//organizations/org_docs/{org_id}/{doc_id}')
async def delete_org_doc(org_id: UUID, doc_id: int) -> None:
    return await _delete_org_doc(org_id=org_id, doc_id=doc_id)


@org_doc_router.get('/organizations/org_docs/{org_id}')
async def get_all_org_docs(org_id: UUID) -> Optional[list[Dict[str, Any]]]:
    return await _show_all_org_docs(org_id=org_id)