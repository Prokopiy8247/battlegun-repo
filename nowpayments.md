API Documentation
Instant Payments Notifications
IPN (Instant payment notifications, or callbacks) are used to notify you when transaction status is changed.
To use them, you should complete the following steps:

Generate and save the IPN Secret key in Payment Settings tab at the Dashboard;

Insert your URL address where you want to get callbacks in create_payment request. The parameter name is ipn_callback_url. You will receive payment updates (statuses) to this URL address.**
Please, take note that we cannot send callbacks to your localhost unless it has dedicated IP address.**

important Please make sure that firewall software on your server (i.e. Cloudflare) does allow our requests to come through. It may be required to whitelist our IP addresses on your side to get it. The list of these IP addresses can be requested at partners@nowpayments.io;

You will receive all the parameters at the URL address you specified in (2) by POST request;
The POST request will contain the x-nowpayments-sig parameter in the header.
The body of the request is similiar to a get payment status response body.
You can see examples in "Webhook examples" section.

Sort the POST request by keys and convert it to string using
JSON.stringify (params, Object.keys(params).sort()) or the same function;

Sign a string with an IPN-secret key with HMAC and sha-512 key;

Compare the signed string from the previous step with the x-nowpayments-sig , which is stored in the header of the callback request;
If these strings are similar, it is a success.
Otherwise, contact us on support@nowpayments.io to solve the problem.

Example of creating a signed string at Node.JS

View More
Plain Text
function sortObject(obj) {
  return Object.keys(obj).sort().reduce(
    (result, key) => {
      result[key] = (obj[key] && typeof obj[key] === 'object') ? sortObject(obj[key]) : obj[key]
      return result
    },
    {}
  )
}
const hmac = crypto.createHmac('sha512', notificationsKey);
hmac.update(JSON.stringify(sortObject(params)));
const signature = hmac.digest('hex');
Example of comparing signed strings in PHP

View More
Plain Text
function tksort(&$array)
  {
  ksort($array);
  foreach(array_keys($array) as $k)
    {
    if(gettype($array[$k])=="array")
      {
      tksort($array[$k]);
      }
    }
  }
function check_ipn_request_is_valid()
    {
        $error_msg = "Unknown error";
        $auth_ok = false;
        $request_data = null;
        if (isset($_SERVER['HTTP_X_NOWPAYMENTS_SIG']) && !empty($_SERVER['HTTP_X_NOWPAYMENTS_SIG'])) {
            $recived_hmac = $_SERVER['HTTP_X_NOWPAYMENTS_SIG'];
            $request_json = file_get_contents('php://input');
            $request_data = json_decode($request_json, true);
            tksort($request_data);
            $sorted_request_json = json_encode($request_data, JSON_UNESCAPED_SLASHES);
            if ($request_json !== false && !empty($request_json)) {
                $hmac = hash_hmac("sha512", $sorted_request_json, trim($this->ipn_secret));
                if ($hmac == $recived_hmac) {
                    $auth_ok = true;
                } else {
                    $error_msg = 'HMAC signature does not match';
                }
            } else {
                $error_msg = 'Error reading POST data';
            }
        } else {
            $error_msg = 'No HMAC signature sent.';
        }
    }
Example comparing signed signatures in Python

View More
python
import json 
import hmac 
import hashlib
def np_signature_check(np_secret_key, np_x_signature, message):
    sorted_msg = json.dumps(message, separators=(',', ':'), sort_keys=True)
    digest = hmac.new(
    str(np_secret_key).encode(), 
    f'{sorted_msg}'.encode(),
    hashlib.sha512)
    signature = digest.hexdigest()
    if signature == np_x_signature:
        return
    else:
        print("HMAC signature does not match")
Usually you will get a notification per each step of processing payments, withdrawals, or transfers, related to custodial recurring payments.

The webhook is being sent automatically once the transaction status is changed.

You also can request an additional IPN notification using your NOWPayments dashboard.

Please note that you should set up an endpoint which can receive POST requests from our server.

Before going production we strongly recommend to make a test request to this endpoint to ensure it works properly.



POST
Create invoice
https://api.nowpayments.io/v1/invoice
Creates a payment link. With this method, the customer is required to follow the generated url to complete the payment. Data must be sent as a JSON-object payload.

Request fields:

price_amount (required) - the amount that users have to pay for the order stated in fiat currency. In case you do not indicate the price in crypto, our system will automatically convert this fiat amount into its crypto equivalent. NOTE: Some of the assets (KISHU, NWC, FTT, CHR, XYM, SRK, KLV, SUPER, OM, XCUR, NOW, SHIB, SAND, MATIC, CTSI, MANA, FRONT, FTM, DAO, LGCY), have a maximum price limit of ~$2000;
price_currency (required) - the fiat currency in which the price_amount is specified (usd, eur, etc);
pay_currency (optional) - the specified crypto currency (btc, eth, etc), or one of available fiat currencies if it's enabled for your account (USD, EUR, ILS, GBP, AUD, RON);
If not specified, can be chosen on the invoice_url
ipn_callback_url (optional) - url to receive callbacks, should contain "http" or "https", eg. "https://nowpayments.io";
order_id (optional) - internal store order ID, e.g. "RGDBP-21314";
order_description (optional) - internal store order description, e.g. "Apple Macbook Pro 2019 x 1";
success_url(optional) - url where the customer will be redirected after successful payment;
cancel_url(optional) - url where the customer will be redirected after failed payment;
is_fixed_rate(optional) - boolean, can be true or false. Required for fixed-rate exchanges;
NOTE: the rate of exchange will be frozen for 20 minutes. If there are no incoming payments during this period, the payment status changes to "expired";
is_fee_paid_by_user(optional) - boolean, can be true or false. Required for fixed-rate exchanges with all fees paid by users;
NOTE: the rate of exchange will be frozen for 20 minutes. If there are no incoming payments during this period, the payment status changes to "expired";
SUCCESSFUL RESPONSE FIELDS
View More
Name	Type	Description
id	String	Invoice ID
token_id	String	Internal identifier
order_id	String	Order ID specified in request
order_description	String	Order description specified in request
price_amount	String	Base price in fiat
price_currency	String	Ticker of base fiat currency
pay_currency	String	Currency your customer will pay with. If it's 'null' your customer can choose currency in web interface.
ipn_callback_url	String	Link to your endpoint for IPN notifications catching
invoice_url	String	Link to the payment page that you can share with your customer
success_url	String	Customer will be redirected to this link once the payment is finished
cancel_url	String	Customer will be redirected to this link if the payment fails
partially_paid_url	String	Customer will be redirected to this link if the payment gets partially paid status
payout_currency	String	Ticker of payout currency
created_at	String	Time of invoice creation
updated_at	String	Time of latest invoice information update
is_fixed_rate	Boolean	This parameter is 'True' if Fixed Rate option is enabled and 'false' if it's disabled
is_fee_paid_by_user	Boolean	This parameter is 'True' if Fee Paid By User option is enabled and 'false' if it's disabled
HEADERS
x-api-key
{{api-key}}

(Required) Your NOWPayments API key

Content-Type
application/json

(Required) Your payload has to be JSON object

Body
raw (json)
View More
json
{
  "price_amount": 1000,
  "price_currency": "usd",
  "order_id": "RGDBP-21314",
  "order_description": "Apple Macbook Pro 2019 x 1",
  "ipn_callback_url": "https://nowpayments.io",
  "success_url": "https://nowpayments.io",
  "cancel_url": "https://nowpayments.io",
  "partially_paid_url": "https://nowpayments.io",
  "is_fixed_rate": true,
  "is_fee_paid_by_user": false
}

Example Request
201
View More
curl
curl --location 'https://api.nowpayments.io/v1/invoice' \
--header 'x-api-key: {{api-key}}' \
--header 'Content-Type: application/json' \
--data '{
  "price_amount": 1000,
  "price_currency": "usd",
  "order_id": "RGDBP-21314",
  "order_description": "Apple Macbook Pro 2019 x 1",
  "ipn_callback_url": "https://nowpayments.io",
  "success_url": "https://nowpayments.io",
  "cancel_url": "https://nowpayments.io"
}

'
201 Created
Example Response
Body
Headers (19)
View More
json
{
  "id": "4522625843",
  "order_id": "RGDBP-21314",
  "order_description": "Apple Macbook Pro 2019 x 1",
  "price_amount": "1000",
  "price_currency": "usd",
  "pay_currency": null,
  "ipn_callback_url": "https://nowpayments.io",
  "invoice_url": "https://nowpayments.io/payment/?iid=4522625843",
  "success_url": "https://nowpayments.io",
  "cancel_url": "https://nowpayments.io",
  "created_at": "2020-12-22T15:05:58.290Z",
  "updated_at": "2020-12-22T15:05:58.290Z"
}
POST
Create payment
https://api.nowpayments.io/v1/payment
Creates payment. With this method, your customer will be able to complete the payment without leaving your website.

Be sure to consider the details of repeated and wrong-asset deposits from 'Repeated Deposits and Wrong-Asset Deposits' section when processing payments.

Data must be sent as a JSON-object payload.
Required request fields:

price_amount (required) - the fiat equivalent of the price to be paid in crypto. If the pay_amount parameter is left empty, our system will automatically convert this fiat price into its crypto equivalent. Please note that this does not enable fiat payments, only provides a fiat price for yours and the customer’s convenience and information. NOTE: Some of the assets (KISHU, NWC, FTT, CHR, XYM, SRK, KLV, SUPER, OM, XCUR, NOW, SHIB, SAND, MATIC, CTSI, MANA, FRONT, FTM, DAO, LGCY), have a maximum price amount of ~$2000;

price_currency (required) - the fiat currency in which the price_amount is specified (usd, eur, etc);

pay_amount (optional) - the amount that users have to pay for the order stated in crypto. You can either specify it yourself, or we will automatically convert the amount you indicated in price_amount;

pay_currency (required) - the crypto currency in which the pay_amount is specified (btc, eth, etc), or one of available fiat currencies if it's enabled for your account (USD, EUR, ILS, GBP, AUD, RON);
NOTE: some of the currencies require a Memo, Destination Tag, etc., to complete a payment (AVA, EOS, BNBMAINNET, XLM, XRP). This is unique for each payment. This ID is received in “payin_extra_id” parameter of the response. Payments made without "payin_extra_id" cannot be detected automatically;

ipn_callback_url (optional) - url to receive callbacks, should contain "http" or "https", eg. "https://nowpayments.io";

order_id (optional) - inner store order ID, e.g. "RGDBP-21314";

order_description (optional) - inner store order description, e.g. "Apple Macbook Pro 2019 x 1";

payout_address (optional) - usually the funds will go to the address you specify in your Personal account. In case you want to receive funds on another address, you can specify it in this parameter;

payout_currency (optional) - currency of your external payout_address, required when payout_adress is specified;

payout_extra_id(optional) - extra id or memo or tag for external payout_address;

is_fixed_rate(optional) - boolean, can be true or false. Required for fixed-rate exchanges;
NOTE: the rate of exchange will be frozen for 20 minutes. If there are no incoming payments during this period, the payment status changes to "expired".

is_fee_paid_by_user(optional) - boolean, can be true or false. Required for fixed-rate exchanges with all fees paid by users;
NOTE: the rate of exchange will be frozen for 20 minutes. If there are no incoming payments during this period, the payment status changes to "expired". The fee paid by user payment can be only fixed rate. If you disable fixed rate during payment creation process, this flag would enforce fixed_rate to be true;

Here the list of available statuses of payment:

waiting - waiting for the customer to send the payment. The initial status of each payment;

confirming - the transaction is being processed on the blockchain. Appears when NOWPayments detect the funds from the user on the blockchain;
Please note: each currency has its own amount of confirmations required to start the processing.

confirmed - the process is confirmed by the blockchain. Customer’s funds have accumulated enough confirmations;

sending - the funds are being sent to your personal wallet. We are in the process of sending the funds to you;

partially_paid - it shows that the customer sent less than the actual price. Appears when the funds have arrived in your wallet;

finished - the funds have reached your personal address and the payment is finished;

failed - the payment wasn't completed due to the error of some kind;

expired - the user didn't send the funds to the specified address in the 7 days time window;

Please note: when you're creating a fiat2crypto payment you also should include additional header to your request - "origin-ip : xxx", where xxx is your customer IP address.

SUCCESSFUL RESPONSE FIELDS
View More
Name	Type	Description
payment_id	String	Payment ID you can refer to
payment_status	String	Current status of the payment. On creation it supposed to be 'waiting'
pay_address	String	Address which is meant for customer to make a deposit to.
price_amount	Float	The amount you set as a price,
price_currency	String	Ticker of base currency
pay_amount	Float	Amount customer is meant to pay.
pay_currency	String	Deposit currency.
order_id	String	Order ID is a string for your internal identifier you can enter upon payment creation.
order_description	String	Order description is a string for your convenience to describe anything about the payment for your own reference.
ipn_callback_url	String	Link to your endpoint for IPN notifications catching
created_at	String	Time of payment creation
updated_at	String	Time of latest payment information update
purchase_id	String	Special identifier for handling partially_paid payments
amount_received	Float	Estimate for amount you're intended to receive if customer would deposit full amount.
payin_extra_id	String	(Optional) Deposit address' memo, if applied
smart_contract	String	
network	String	Network of deposit
network_precision	String	
time_limit	String	
expiration_estimate_date	String	
is_fixed_rate	String	This parameter is 'True' if Fixed Rate option is enabled and 'false' if it's disabled
is_fee_paid_by_user	String	This parameter is 'True' if Fee Paid By User option is enabled and 'false' if it's disabled
valid_until	String	This parameter indicated when payment go expired.
type	String	Type of payment. It can be either crypto2crypto or fiat2crypto
redirectData: redirect_url	String	(Optional) If you're using fiat2crypto flow, this parameter will appear with link to our fiat2crypto processing provider web interface.
HEADERS
x-api-key
{{api-key}}

(Required) Your NOWPayments API key

Content-Type
application/json

(Required) Your payload has to be JSON object

example:

{
  "price_amount": 3999.5,
  "price_currency": "usd",
  "pay_currency": "btc",
  "ipn_callback_url": "https://nowpayments.io",
  "order_id": "RGDBP-21314",
  "order_description": "Apple Macbook Pro 2019 x 1",
  "is_fixed_rate": true,
  "is_fee_paid_by_user": false
}

Example Request:

curl --location 'https://api.nowpayments.io/v1/invoice-payment' \
--header 'x-api-key: {{api-key}}' \
--header 'Content-Type: application/json' \
--data-raw '{
  "iid": {{invoice_id}},
  "pay_currency": "btc",
  "purchase_id": {{purchase_id}},
  "order_description": "Apple Macbook Pro 2019 x 1",
  "customer_email": "test@gmail.com",
  "payout_address": "0x...",
  "payout_extra_id": null,
  "payout_currency": "usdttrc20"
}'

Example Response:

{
  "payment_id": "5745459419",
  "payment_status": "waiting",
  "pay_address": "3EZ2uTdVDAMFXTfc6uLDDKR6o8qKBZXVkj",
  "price_amount": 3999.5,
  "price_currency": "usd",
  "pay_amount": 0.17070286,
  "pay_currency": "btc",
  "order_id": "RGDBP-21314",
  "order_description": "Apple Macbook Pro 2019 x 1",
  "ipn_callback_url": "https://nowpayments.io",
  "created_at": "2020-12-22T15:00:22.742Z",
  "updated_at": "2020-12-22T15:00:22.742Z",
  "purchase_id": "5837122679",
  "amount_received": null,
  "payin_extra_id": null,
  "smart_contract": "",
  "network": "btc",
  "network_precision": 8,
  "time_limit": null,
  "burning_percent": null,
  "expiration_estimate_date": "2020-12-23T15:00:22.742Z"
}