import requests
import validators

def main():
    PHONE_NUMBER = "0xx xxx xxxx"
    GIFT_URL = input("> ")
    redeem(PHONE_NUMBER,GIFT_URL)
    input()

def redeem(PHONE_NUMBER,GIFT_URL):
    if validators.url(GIFT_URL) is True:
        if "https://gift.truemoney.com/campaign/?v=" in GIFT_URL:
            if requests.get(GIFT_URL).status_code == 200:
                VOUCHER_CODE = str(GIFT_URL.split("https://gift.truemoney.com/campaign/?v=")[1]) 
                response = requests.get(f"https://gift.truemoney.com/campaign/vouchers/{VOUCHER_CODE}/verify?mobile={PHONE_NUMBER}").json()
                gift_code = response["status"]["code"]
                gift_status = response["data"]["voucher"]["status"]
                if gift_status == "active":                           
                    if gift_code != "CANNOT_GET_OWN_VOUCHER":
                        response = requests.post(f"https://gift.truemoney.com/campaign/vouchers/{VOUCHER_CODE}/redeem",
                            json={
                                "mobile":f"{PHONE_NUMBER}","voucher_hash":f"{VOUCHER_CODE}"
                                },
                                headers={
                                "Accept": "application/json",
                                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
                                "Content-Type": "application/json",
                                "Origin": "https://gift.truemoney.com",
                                "Accept-Language": "en-US,en;q=0.9",
                                "Connection": "keep-alive"
                            })
                        if response.status_code == 200:
                            gift_owner = response.json()["data"]["owner_profile"]["full_name"]
                            amount_redeem = float(response.json()["data"]["amount_baht"])
                            print(f"รับเงินสําเร็จจาก {gift_owner} จํานวน {amount_redeem}")
                        
                        else:
                            print("รับเงินไม่สําเร็จ")
                else:
                    print("ไม่สามารถรับ gift ของตัวเองได้")     
            else:
                print("ไม่พบอั่งเปา")
        else:
            print("ลิงค์อั่งเปาไม่ถูกต้อง")
    else:
        print("ลิงค์ไม่ถูกต้อง")

main()