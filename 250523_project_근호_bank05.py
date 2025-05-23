import json # json파일 읽기 및 쓰기
import os # 파일 존재 여부 확인 # 날짜 비교 및 처리
import csv
from datetime import datetime, timedelta

class HistoryManager:
    '''
    * 거래내역 조회 기능을 관리하는 클래스
    -입출금 및 이체 내역 확인
    -날짜별 필터링
    -최근 5건 내역 조회 
    -CSV 형식으로 내보내기 기능
    '''
    
    def __init__(self):
        # 거래내역 파일 경로 설정
        self.history_file = "history.json"
        self.export_file = "export_history.csv"
        
        # 파일이 없을 경우 빈 JSON 파일 생성
        if not os.path.exists(self.history_file): # file이 없다면..
            with open(self.history_file, 'w') as f:
                json.dump([], f)


    def get_all_history(self, account_no):
        '''계좌번호에 해당하는 모든 거래내역 조회'''
        try:
            # 파일 읽기
            with open(self.history_file, "r") as f:
                all_history = json.load(f)

            # 해당 계좌의 거래내역만 필터링
            account_history = []
            for transaction in all_history:
                # 송금자 또는 수취인이 해당 계좌인 경우만
                if transaction.get("from_account") == account_no or transaction.get("to_account") == account_no:
                    account_history.append(transaction)
            return account_history
        except Exception as e: # 에러가 발생하면 Exception as e (에러 원인 파악)
            print(f"거래 내역 조회 중 오류 발생: {e}")
            return []


    def get_recent_history(self, account_no, count=5):
        '''최근 count개의 거래내역 조회'''
        # 모든 내역 가져오기
        all_history = self.get_all_history(account_no)

        # 날짜 기준으로 정렬 (최신순)
        sorted_history = sorted(
            all_history, 
            key=lambda x: datetime.strptime(x.get("date", "1900-01-01"), "%Y-%m-%d %H:%M:%S"),
            reverse=True
        )
        # count 개만 반환
        return sorted_history[:count]


    def search_by_date(self, account_no, start_date, end_date):
        '''날짜 범위로 거래내역 검색'''
        try:
            # 날짜 형식 변환
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")

            # 모든 내역 가져오기
            all_history = self.get_all_history(account_no)

            # 날짜 범위에 맞는 거래내역만 필터링
            filtered_history = []
            for transaction in all_history:
                # 날짜 문자열을 datetime 객채로 변환
                transaction_date = datetime.strptime(
                    transaction.get("date", "1900-01-01")[:10], "%Y-%m-%d" # 날짜 부분만 추출 
                )
                # 날짜 범위 내에 있는지 확인
                if start <= transaction_date <= end:
                    filtered_history.append(transaction)

            return filtered_history
        except Exception as e:
            print(f"날짜 검색 중 오류 발생: {e}")
            return []


    def export_csv(self, account_no):
        '''거래내역을 CSV 형식으로 내보내기'''
        try:
            # 모든 내역 가져오기
            all_history = self.get_all_history(account_no)

            if not all_history:
                print("거래 내역이 없습니다.")
                return False
##################여기부터는 모르겠다###################
            # CSV 파일 생성 (JSON 확장자 사용)
            with open(self.export_file, "w", newline="") as f:
                # CSV 작성을 위한 필드 정의
                fieldnames = ["date", "type", "amount", "from_account", "to_account", "balance"]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                
                # 헤더 작성
                writer.writeheader()
                
                # 데이터 작성
                for transaction in all_history:
                    writer.writerow({
                        "date": transaction.get("date", ""),
                        "type": transaction.get("type", ""),
                        "amount": transaction.get("amount", 0),
                        "from_account": transaction.get("from_account", ""),
                        "to_account": transaction.get("to_account", ""),
                        "balance": transaction.get("balance", 0)
                    })
            
            print(f"거래내역이 {self.export_file}에 저장되었습니다.")
            return True
        except Exception as e:
            print(f"CSV 내보내기 중 오류 발생: {e}")
            return False



    def add_transaction(self, transaction_data):
        """새로운 거래내역 추가 (다른 매니저 클래스에서 호출)"""
        try:
            # 현재 날짜/시간 추가
            transaction_data["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # 기존 내역 읽기
            all_history = []
            if os.path.exists(self.history_file) and os.path.getsize(self.history_file) > 0:
                with open(self.history_file, "r") as f:
                    all_history = json.load(f)
            
            # 새 거래내역 추가
            all_history.append(transaction_data)
            
            # 파일에 저장
            with open(self.history_file, "w") as f:
                json.dump(all_history, f, indent=4)
            
            return True
        except Exception as e:
            print(f"거래내역 추가 중 오류 발생: {e}")
            return False
    


    def display_transactions(self, transactions):
        """거래내역을 예쁘게 출력"""
        if not transactions:
            print("표시할 거래내역이 없습니다.")
            return
        
        print("\n===== 거래 내역 =====")
        print("날짜/시간\t\t종류\t금액\t\t계좌번호\t\t잔액")
        print("="*70)
        
        for t in transactions:
            # 거래 유형에 따라 표시 방식 변경
            t_type = t.get("type", "")
            amount = t.get("amount", 0)
            
            if t_type == "입금":
                account_info = f"입금 → {t.get('to_account', '')}"
            elif t_type == "출금":
                account_info = f"출금 ← {t.get('from_account', '')}"
            else:  # 이체
                account_info = f"{t.get('from_account', '')} → {t.get('to_account', '')}"
            
            print(f"{t.get('date', '')}\t{t_type}\t{amount:,}원\t{account_info}\t{t.get('balance', 0):,}원")
        
        print("="*70)

##################################### 사용 예시
if __name__ == "__main__":
    manager = HistoryManager()
    
    # 테스트를 위한 거래 내역 추가
    manager.add_transaction({
        "type": "입금",
        "amount": 10000,
        "to_account": "1001",
        "balance": 10000
    })
    
    manager.add_transaction({
        "type": "출금",
        "amount": 5000,
        "from_account": "1001",
        "balance": 5000
    })
    
    manager.add_transaction({
        "type": "이체",
        "amount": 3000,
        "from_account": "1001",
        "to_account": "1002",
        "balance": 2000
    })
    
    # 최근 거래내역 조회
    recent = manager.get_recent_history("1001")
    manager.display_transactions(recent)
    
    # CSV로 내보내기
    manager.export_csv("1001")
