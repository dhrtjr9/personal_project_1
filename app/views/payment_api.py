import requests

# 아이엠포트 API 키 설정
IMPORT_API_KEY = 'your_import_api_key_here'
IMPORT_API_SECRET = 'your_import_api_secret_here'

# 결제 정보 전송을 위한 URL
IMPORT_PAYMENT_URL = 'https://api.iamport.kr/payments/prepare'

# 결제 완료 후 상태 확인을 위한 URL
IMPORT_PAYMENT_STATUS_URL = 'https://api.iamport.kr/payments/'

def request_payment(order_id, amount, card_number, expiry, cvc):
    headers = {
        'Authorization': f'{IMPORT_API_KEY}:{IMPORT_API_SECRET}'
    }

    data = {
        'merchant_uid': order_id,
        'amount': amount,
        'card_number': card_number,
        'expiry': expiry,
        'cvc': cvc
    }

    response = requests.post(IMPORT_PAYMENT_URL, headers=headers, data=data)
    return response.json()

def check_payment_status(order_id):
    headers = {
        'Authorization': f'{IMPORT_API_KEY}:{IMPORT_API_SECRET}'
    }

    url = f'{IMPORT_PAYMENT_STATUS_URL}{order_id}'
    response = requests.get(url, headers=headers)
    return response.json()

# 테스트를 위한 예제
if __name__ == '__main__':
    order_id = 'your_unique_order_id_here'  # 고유 주문번호
    amount = 1000  # 결제 금액 (KRW)
    card_number = 'your_card_number_here'  # 카드번호
    expiry = 'your_card_expiry_here'  # 카드 유효기간 (MMYY)
    cvc = 'your_card_cvc_here'  # 카드 CVC 번호

    # 결제 요청
    payment_result = request_payment(order_id, amount, card_number, expiry, cvc)
    print(payment_result)

    # 결제 상태 확인
    if payment_result['code'] == 0:
        payment_id = payment_result['response']['imp_uid']
        payment_status = check_payment_status(payment_id)
        print(payment_status)
