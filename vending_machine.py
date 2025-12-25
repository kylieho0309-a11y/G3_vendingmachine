from easycard_service import EasyCardService

ITEMS = {
    'A01': {'name': '生活泡沫綠茶', 'price': 25, 'stock': 10},
    'B02': {'name': '百事可樂鋁罐', 'price': 30, 'stock': 2},
    'C03': {'name': '綜合蔓越莓汁', 'price': 29, 'stock': 5},
}

def print_menu():
    print('=' * 50)
    print('【悠遊卡自動販賣機】')
    print('商品清單：')
    print('-' * 50)
    print(f"{'代碼':<6}{'商品名稱':<14}{'價格':<8}{'庫存':<8}")
    print('-' * 50)
    for code, info in ITEMS.items():
        print(f"{code:<8}{info['name']:<12}{info['price']:<10}{info['stock']:<8}")
    print('-' * 50)
    print('輸入商品代碼購買後按 Enter，或輸入 Q 離開。')
    print('=' * 50)

def ask_item_code() -> str:
    return input('請輸入商品代碼：').strip().upper()

def validate_item(code: str) -> bool:
    if code not in ITEMS:
        print('⚠️ 商品代碼錯誤，請重新輸入。')
        return False
    if ITEMS[code]['stock'] <= 0:
        print('⚠️ 此商品目前缺貨。')
        return False
    return True

def main():
    svc = EasyCardService(initial_balance=100)

    while True:
        print_menu()
        code = ask_item_code()

        if code == 'Q':
            print('系統結束，感謝使用！')
            break

        if not validate_item(code):
            input('按 Enter 回到清單...')
            continue

        item = ITEMS[code]
        name = item['name']
        price = item['price']
        print(f"您選擇：{name}，價格：{price} 元")

        combined_attempts = 0
        max_attempts = 3

        while True:
            card_number = input('請輸入悠遊卡卡號（8 碼）：').strip()
            error_msg = None

            if not (card_number.isdigit() and len(card_number) == 8):
                error_msg = '卡號格式錯誤，需為 8 位數字'
                combined_attempts += 1
            else:
                ok, info = svc.charge(card_number, price)
                if ok:
                    ITEMS[code]['stock'] -= 1
                    remaining_bal = info.get('new_balance', None)
                    print('✅ 交易成功！')
                    if remaining_bal is not None:
                        print(f'悠遊卡剩餘餘額：{remaining_bal} 元')
                    print('交易完成請取卡，謝謝光臨！')
                    input('按 Enter 回到清單...')
                    break
                else:
                    error_msg = info.get('error', '未知錯誤')
                    combined_attempts += 1

            remaining = max_attempts - combined_attempts
            if remaining > 0:
                print(f'❌ 交易失敗：{error_msg}。可再試 {remaining} 次。')
                continue
            else:
                print('❌ 交易失敗（重試達 3 次），返回商品清單。')
                input('按 Enter 回到清單...')
                break

if __name__ == '__main__':
    main()
