from django.shortcuts import render

# Create your views here.
import jsons
import base64
import requests
import shortuuid
from django.http import HttpResponse
from django.shortcuts import redirect
from cryptography.hazmat.primitives import hashes
from django.views.decorators.csrf import csrf_exempt
from cryptography.hazmat.backends import default_backend
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
########################## HELPER FUNCTION ################################
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def calculate_sha256_string(input_string):
    # Create a hash object using the SHA-256 algorithm
    sha256 = hashes.Hash(hashes.SHA256(), backend=default_backend())
    # Update hash with the encoded string
    sha256.update(input_string.encode('utf-8'))
    # Return the hexadecimal representation of the hash
    return sha256.finalize().hex()
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def base64_encode(input_dict):
    # Convert the dictionary to a JSON string
    json_data = jsons.dumps(input_dict)
    # Encode the JSON string to bytes
    data_bytes = json_data.encode('utf-8')
    # Perform Base64 encoding and return the result as a string
    return base64.b64encode(data_bytes).decode('utf-8')
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
########################## Create your views here. ########################
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def index(request):
    return render(request, "phonepay/index.html", { 'output': "Please Pay & Repond From The Payment Gateway Will Come In This Section", 'main_request': "" })

def pay(request):
    MAINPAYLOAD = {
        "merchantId": "PGTESTPAYUAT86",
        "merchantTransactionId": shortuuid.uuid(),
        "merchantUserId": "MUID123",
        "amount": 10000,
        "redirectUrl": "http://0.0.0.0:8000/phonepay/return-to-me/",
        "redirectMode": "POST",
        "callbackUrl": "http://0.0.0.0:8000/phonepay/return-to-me/",
        "mobileNumber": "9999999999",
        "paymentInstrument": {
            "type": "PAY_PAGE"
        }
    }
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # SETTING
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    INDEX = "1"
    ENDPOINT = "/pg/v1/pay"
    SALTKEY = "099eb0cd-02cf-4e2a-8aca-3e6c6aff0399"
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    base64String = base64_encode(MAINPAYLOAD)
    mainString = base64String + ENDPOINT + SALTKEY;
    sha256Val = calculate_sha256_string(mainString)
    checkSum = sha256Val + '###' + INDEX;
    # # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # # Payload Send
    # # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    headers = {
        'Content-Type': 'application/json',
        'X-VERIFY': checkSum,
        'accept': 'application/json',
    }
    json_data = {
        'request': base64String,
    }
    response = requests.post('https://api-preprod.phonepe.com/apis/pg-sandbox/pg/v1/pay', headers=headers, json=json_data)
    responseData = response.json();
    return redirect(responseData['data']['instrumentResponse']['redirectInfo']['url'])

@csrf_exempt
def payment_return(request):
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # SETTING
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    INDEX = "1"
    SALTKEY = "96434309-7796-489d-8924-ab56988a6076"
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Access form data in a POST request
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    form_data = request.POST
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Convert form data to a dictionary
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    form_data_dict = dict(form_data)
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    transaction_id = form_data.get('transactionId', None)
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # 1.In the live please match the amount you get byamount you send also so that hacker can't pass static value.
    # 2.Don't take Marchent ID directly validate it with yoir Marchent ID
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++
    if transaction_id:
        request_url = 'https://api-preprod.phonepe.com/apis/pg-sandbox/pg/v1/status/PGTESTPAYUAT/' + transaction_id;
        sha256_Pay_load_String = '/pg/v1/status/PGTESTPAYUAT/' + transaction_id + SALTKEY;
        sha256_val = calculate_sha256_string(sha256_Pay_load_String);
        checksum = sha256_val + '###' + INDEX;
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # Payload Send
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        headers = {
            'Content-Type': 'application/json',
            'X-VERIFY': checksum,
            'X-MERCHANT-ID': transaction_id,
            'accept': 'application/json',
        }
        response = requests.get(request_url, headers=headers)
        #page_respond_data=form_data_dict, page_respond_data_varify=response.text
    return render(request, 'phonepay/index.html', { 'output': response.text, 'main_request': form_data_dict  })
