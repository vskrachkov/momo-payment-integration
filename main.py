import hashlib
import hmac
import requests
import uuid

secretKey = "at67qH6mk8w5Y1nAyMoYKMWACiEi2bsa"
accessKey = "klm05TvNBzhg7h7j"
partnerCode = "MOMOBKUN20180529"
lang = "en"
requestId = str(uuid.uuid4())
orderId = str(uuid.uuid4())
autoCapture = True
requestType = "captureWallet"
notifyUrl = "https://sangle.free.beeceptor.com"
returnUrl = "https://sangle.free.beeceptor.com"
amount = "700000"
orderInfo = "Some order Info"
extraData = "ew0KImVtYWlsIjogImh1b25neGRAZ21haWwuY29tIg0KfQ=="

rawSignature = (
    "accessKey="
    + accessKey
    + "&amount="
    + amount
    + "&extraData="
    + extraData
    + "&ipnUrl="
    + notifyUrl
    + "&orderId="
    + orderId
    + "&orderInfo="
    + orderInfo
    + "&partnerCode="
    + partnerCode
    + "&redirectUrl="
    + returnUrl
    + "&requestId="
    + requestId
    + "&requestType="
    + requestType
)

h = hmac.new(secretKey.encode(), rawSignature.encode(), hashlib.sha256)
signature = h.hexdigest()

payload = {
    "partnerCode": partnerCode,
    "partnerName": "Test",
    "storeId": partnerCode,
    "requestType": requestType,
    "ipnUrl": notifyUrl,
    "redirectUrl": returnUrl,
    "orderId": orderId,
    "amount": amount,
    "lang": lang,
    "autoCapture": autoCapture,
    "orderInfo": orderInfo,
    "requestId": requestId,
    "extraData": extraData,
    "signature": signature
}
resp = requests.post("https://test-payment.momo.vn/v2/gateway/api/create", json=payload)
print(resp)

if resp.ok:
    response = resp.json()
    print("response: ", response)
else:
    print("error: ", resp.status_code, resp.content.decode("utf8"))
