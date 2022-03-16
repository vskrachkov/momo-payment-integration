import hashlib
import hmac
import requests
import uuid
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI()

API_URL = "https://test-payment.momo.vn/v2/gateway/api/create"
SECRET_KEY = "at67qH6mk8w5Y1nAyMoYKMWACiEi2bsa"
ACCESS_KEY = "klm05TvNBzhg7h7j"
PARTNER_CODE = "MOMOBKUN20180529"


@app.get("/", response_class=HTMLResponse, name="index-page")
def index() -> str:
    checkout_page_url = app.url_path_for("checkout-page")
    return f"""
    <html>
        <head>
            <title>Momo Demo</title>
        </head>
        <body>
            <h1>Momo Demo</h1>
            <a target="_blank" href="{checkout_page_url}">Pay with Momo App</a></br></br>
        </body>
    </html>
    """


@app.get(
    "/checkout-page",
    name="checkout-page",
    response_class=RedirectResponse,
    status_code=303,
)
def checkout_page() -> str:
    result = create_order("87345")
    return result["payUrl"]


def create_order(
    amount: str,
    notify_url: str = "https://sangle.free.beeceptor.com",
    return_url: str = "https://sangle.free.beeceptor.com",
) -> dict:
    requestId = str(uuid.uuid4())
    orderId = str(uuid.uuid4())
    autoCapture = True
    requestType = "captureWallet"
    notifyUrl = notify_url
    returnUrl = return_url
    amount = amount
    orderInfo = "Some order Info"
    extraData = ""

    rawSignature = (
        f"accessKey={ACCESS_KEY}"
        f"&amount={amount}"
        f"&extraData={extraData}"
        f"&ipnUrl={notifyUrl}"
        f"&orderId={orderId}"
        f"&orderInfo={orderInfo}"
        f"&partnerCode={PARTNER_CODE}"
        f"&redirectUrl={returnUrl}"
        f"&requestId={requestId}"
        f"&requestType={requestType}"
    )

    h = hmac.new(SECRET_KEY.encode(), rawSignature.encode(), hashlib.sha256)
    signature = h.hexdigest()

    payload = {
        "partnerCode": PARTNER_CODE,
        "partnerName": "Test",
        "storeId": PARTNER_CODE,
        "requestType": requestType,
        "ipnUrl": notifyUrl,
        "redirectUrl": returnUrl,
        "orderId": orderId,
        "amount": amount,
        "autoCapture": autoCapture,
        "orderInfo": orderInfo,
        "requestId": requestId,
        "extraData": extraData,
        "signature": signature,
    }
    resp = requests.post(API_URL, json=payload)

    if not resp.ok:
        response = resp.content.decode("utf8")
        print("error: ", resp.status_code, response)
        raise Exception(response)

    return resp.json()
