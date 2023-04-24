from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from munch import Munch
from schema import ReportSchema
from mailmerge import MailMerge
import numpy as np
from fastapi.responses import FileResponse
from lib import convert_file

# from munch import Munch
from pathlib import Path
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MALE_TEMPLATE = Path("./templates/male.docx")
FEMALE_TEMPLATE = Path("./templates/fem.docx")


# @app.post("/upload")
# async def convert_file():
#     return Munch(message="file has been converted")


@app.post("/report")
async def get_report(report: ReportSchema):
    # print(report)
    try:
        payload = {}
        data = report.dict()

        payload.update(data["client"])
        payload.update(data["parameters"])
        bmi = float(payload["bmi"])
        payload["area"] = payload["area"].strip()
        payload["ref"] = payload["ref"].strip()
        payload["dt"] = payload["dt"].strip()
        print(payload["ref"])
        final_bmi = 0
        # print(bmi)

        if bmi < 18.5:
            final_bmi = f"{bmi}kg/m2(UnderWeight)"
        if bmi >= 18.5 and bmi < 25:
            final_bmi = f"{bmi}kg/m2(Normal)"
        if bmi >= 25 and bmi < 30:
            final_bmi = f"{bmi}kg/m2(Normal)"
        if bmi >= 30.0:
            final_bmi = f"{bmi}kg/m2(Obese)"
        payload["bmi"] = final_bmi
        print(payload["gender"])
        if payload["gender"] in ["MALE", "male", "Male", "M", "m"]:
            template = MALE_TEMPLATE
            print("Printing male")
        else:
            template = FEMALE_TEMPLATE
            print("printing")
        document = MailMerge(template.resolve())
        document.merge(**payload)
        document.write("./reports/TEMPLATE_PRINT.docx")
        fpath = Path("./reports/TEMPLATE_PRINT.docx")
        # if os.path.exists(Path("./pdf/TEMPLATE_PRINT.pdf").resolve()):
        #     os.remove(Path("./pdf/TEMPLATE_PRINT.pdf").resolve())
        # convert_file("./pdf", fpath.resolve())
        # pdfReport = Path("./pdf/TEMPLATE_PRINT.pdf")
        # return FileResponse(pdfReport.resolve())
        return FileResponse(fpath.resolve())

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=400,
            detail="Error downloading report,check report vital parameters",
        )
