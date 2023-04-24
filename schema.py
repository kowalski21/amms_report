from pydantic import BaseModel


class ReportSchema(BaseModel):
    client: dict
    parameters: dict
