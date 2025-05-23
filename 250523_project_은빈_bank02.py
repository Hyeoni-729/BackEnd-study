
class AccountManager:
    def __init__(self):
        self.next_account_no = 1001  # 시작 번호를 그냥 1001로 고정
        self.accounts = {}
        self.balances = {}
 
    def create_account(self, user_name, resident_id):  # 계좌 생성
        if not self.validate_resident_id(resident_id):
            print("잘못된 주민등록번호 형식입니다. 다시 시도해주세요.")
            return
        
        account_no = self.next_account_no
        self.accounts[account_no] = {
            "user_name": user_name,
            "resident_id": resident_id
        }
        self.balances[account_no] = 0  # 잔액 0원으로 초기화

        print(f"{account_no}번 계좌가 생성되었습니다.")
        self.next_account_no += 1 

    def close_account(self, account_no):  #계좌 삭제(잔액이 일때)
        if account_no not in self.accounts:
            print("존재하지 않는 계좌번호입니다.")
            return
        balance = self.balances.get(account_no, 0)
        if balance == 0:
            del self.accounts[account_no]
            del self.balances[account_no]
            print(f"{account_no}번 계좌가 해지되었습니다.")
        else:
            print("잔액이 남아있습니다.")

    def verify_account(self, account_no):  # 계좌 존재 여부 확인
        if account_no in self.accounts:
            print(f"✅ {account_no}번 계좌가 존재합니다.")
            return True
        else:
            print(f"❌ {account_no}번 계좌가 존재하지 않습니다.")
            return False

    def validate_resident_id(self, resident_id):
    
        if len(resident_id) != 14:  # 주민번호는 총 14자리임. 
            return False
        if resident_id[6] != '-':  # 가운데에 '-'가 있어야 함
            return False
   
        front = resident_id[:6]   # '-'를 뺀 나머지 13자리가 모두 숫자인지 확인
        back = resident_id[7:]
        if not (front.isdigit() and back.isdigit()):
            return False
        return True
        

def account_menu(manager):
    while True:
        print(f'''
--계좌 관리 시스템--
1. 계좌 생성
2. 계좌 삭제
3. 계좌 확인
0. 뒤로 가기
        ''')
        select = input("원하는 기능을 선택하세요: ")

        if select == "1":
            name = input("이름을 입력하세요: ")
            resident_id = input("주민등록번호 (XXXXXX-XXXXXXX) 형식으로 입력하세요: ")
            manager.create_account(name, resident_id)

        elif select == "2":
            try:
                acc_no = int(input("삭제할 계좌번호를 입력하세요: "))
                manager.close_account(acc_no)
            except ValueError:
                print("계좌번호는 숫자만 입력해주세요.")

        elif select == "3":
            try:
                acc_no = int(input("확인할 계좌번호를 입력하세요: "))
                manager.verify_account(acc_no)
            except ValueError:
                print("계좌번호는 숫자만 입력해주세요.")

        elif select == "0":
            print("계좌 관리 메뉴를 종료합니다.")
            break

        else:
            print("올바른 메뉴를 선택해주세요.")

if __name__ == "__main__":
    manager = AccountManager()
    account_menu(manager)
    