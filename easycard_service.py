from typing import Tuple, Dict, Any

class EasyCardService:
    def __init__(self, initial_balance: int = 300) -> None:
        self._accounts: Dict[str, int] = {}
        self._initial_balance = int(initial_balance)

    def is_valid_card(self, card_number: str) -> bool:
        return isinstance(card_number, str) and card_number.isdigit() and len(card_number) == 8

    def digit_sum(self, card_number: str) -> int:
        return sum(int(d) for d in card_number)

    def is_insufficient_by_rule(self, card_number: str) -> bool:
        return self.digit_sum(card_number) % 3 == 0

    def card_exists(self, card_number: str) -> bool:
        return self.is_valid_card(card_number)

    def ensure_account_initialized(self, card_number: str) -> None:
        if card_number not in self._accounts:
            self._accounts[card_number] = 0 if self.is_insufficient_by_rule(card_number) else self._initial_balance

    def get_balance(self, card_number: str) -> int:
        if not self.is_valid_card(card_number):
            return -1
        self.ensure_account_initialized(card_number)
        return self._accounts[card_number]

    def has_sufficient_balance(self, card_number: str, amount: int) -> bool:
        bal = self.get_balance(card_number)
        return bal >= 0 and bal >= amount

    def charge(self, card_number: str, amount: int) -> Tuple[bool, Dict[str, Any]]:
        if not self.is_valid_card(card_number):
            return False, {'error': '卡號格式錯誤，需為 8 位數字'}
        if amount <= 0:
            return False, {'error': '扣款金額需為正整數'}

        if self.is_insufficient_by_rule(card_number):
            self.ensure_account_initialized(card_number)
            return False, {'error': '餘額不足'}

        self.ensure_account_initialized(card_number)
        if not self.has_sufficient_balance(card_number, amount):
            return False, {'error': '餘額不足'}

        self._accounts[card_number] -= amount
        return True, {'new_balance': self._accounts[card_number]}

    def top_up(self, card_number: str, amount: int) -> Tuple[bool, Dict[str, Any]]:
        if not self.is_valid_card(card_number):
            return False, {'error': '卡號格式錯誤，需為 8 位數字'}
        if amount <= 0:
            return False, {'error': '加值金額需為正整數'}
        self.ensure_account_initialized(card_number)
        self._accounts[card_number] += amount
        return True, {'new_balance': self._accounts[card_number]}


if __name__ == '__main__':
    svc = EasyCardService(initial_balance=300)
    samples = ['12345678', '87654321', '11112222', '22223333', '33334444', '13572468', '00000000', '99999999']
    print('示範檢查：')
    for c in samples:
        bal = svc.get_balance(c)
        rule = '3 的倍數 → 餘額不足' if svc.is_insufficient_by_rule(c) else '非 3 的倍數 → 有餘額'
        print(f'卡號 {c} | 初始餘額: {bal} | 規則：{rule}')
