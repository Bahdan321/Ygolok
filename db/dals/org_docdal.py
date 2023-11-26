import uuid

from fastapi import HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional


class OrgDocDAL:

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
    
    async def create_org_doc(self, org_id: uuid.UUID, doc_title: str, address: str, documet: str, table):
        new_org_doc = table( org_id=org_id,
                             doc_title=doc_title,
                             address=address,
                             documet=documet)
        self.db_session.add(new_org_doc)
        await self.db_session.flush()
        return new_org_doc
    
    async def show_all_org_docs(self, org_id: uuid.UUID,table):
        query = select(table).where(table.id == org_id)
        res = await self.db_session.execute(query)
        org_doc_row = res.fetchall()

        if not org_doc_row:
            raise HTTPException(status_code=404, detail='not found')
        print(org_doc_row[0])
        return org_doc_row[0]