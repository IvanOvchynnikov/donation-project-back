from pydantic import BaseModel

class DonationResponseModel(BaseModel):
    id: int
    title: str
    tag: str
    description: str
    image: str

    bank_account_number: str
    bank_beneficiary_name: str
    bank_ifsc_code: str

    upi_mobile_number: str
    upi_id: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Save the Oceans",
                "tag": "environment",
                "description": "Help us save marine life and protect ocean ecosystems.",
                "image": "https://example.com/image1.jpg",
                "bank_account_number": "1234567890",
                "bank_beneficiary_name": "Ocean Fund",
                "bank_ifsc_code": "IFSC1234",
                "upi_mobile_number": "9876543210",
                "upi_id": "oceanfund@upi",
            }
        }
