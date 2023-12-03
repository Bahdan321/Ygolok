from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.organizationdocuments import OrganizationDocument


class OrgDocDAL:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_org_doc(self, org_id: str, doc_title: str, address: str, document: str) -> OrganizationDocument:
        new_org_doc = OrganizationDocument(org_id=org_id, doc_title=doc_title, address=address, document=document)
        self.session.add(new_org_doc)
        await self.session.flush()

        return new_org_doc

    async def delete_org_doc(self, org_id: str, doc_id: int) -> None:
        stmt = delete(OrganizationDocument).where(OrganizationDocument.org_id == org_id and OrganizationDocument.id == doc_id)
        await self.session.execute(stmt)

    async def show_all_org_docs(self, org_id: str) -> list[OrganizationDocument]:
        stmt = select(OrganizationDocument).where(OrganizationDocument.org_id == org_id)
        result = await self.session.execute(stmt)
        org_docs = result.scalars().all()

        return org_docs