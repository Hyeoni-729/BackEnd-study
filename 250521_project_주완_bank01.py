import json #json 파일 저장용
import hashlib #공인인증서 비밀번호 암호화

with open("certs.json","r",encoding="utf-8") as f:
    dict1 = json.load(f)


class LoginManager:
    def __init__(self):
        self.login = False
        
    def issue_certificate(self): #공인인증서 발급
        print("\n공인인증서 발급페이지입니다.")
        while True:
            data1 = input("성함을 입력해주세요. [0.나가기] : ")
            if data1 == "0":
                break
            out1 = False
            if len(data1) > 1:
                for value in data1:
                    if 44032 <= ord(value) <=55203:
                        out1 = True
                    else:
                        out1 = False
            if out1 == False:
                print("올바르지 않은 이름입니다. 다시 입력해주세요.")
            elif out1 == True:
                print(f"반갑습니다 {data1}님 비밀번호를 설정해주세요.")
                out1 = False
                break
                
        while True:
            if data1 == "0":
                break
            data2 = input("8자 이상, 영문, 특수기호(!,@,#,$)를 포함하여 비밀번호를 설정해주세요. [0.나가기] : ")
            if data2 == "0":
                break
            self.out_num = False
            self.out_eng = False
            self.out_spe = False
            if len(data2) >= 8:
                self.out_num = True
            for value1 in data2:
                if 65 <= ord(value1) <= 90 or 97 <= ord(value1) <= 122:
                    self.out_eng = True
            for value2 in data2:
                if 33 <= ord(value2) <= 47 or 58 <= ord(value2) <= 64 or 91 <= ord(value2) <= 96 or 123 <= ord(value2) <= 127:
                    self.out_spe = True
            if self.out_num == True and self.out_eng == True and self.out_spe == True:
                print("비밀번호 설정이 완료되었습니다.")
                hashed_pw = hashlib.sha256(data2.encode()).hexdigest()
                dict_up = {data1:hashed_pw}
                dict1.update(dict_up)
                break
            elif self.out_num == False and self.out_eng == True and self.out_spe == True:
                print("8자 이상 설정해주세요.")
            elif self.out_num == True and self.out_eng == False and self.out_spe == True:
                print("영문을 포함해 설정해주세요.")
            elif self.out_num == True and self.out_eng == True and self.out_spe == False:
                print("특수기호(!,@,#,$,%,^,&,*,\(,\ 등)를 포함하여 설정해주세요.)")
            else:
                print("올바른 비밀번호를 설정해주세요.")
        with open("certs.json","w",encoding="utf-8") as f:
            json.dump(dict1,f,ensure_ascii=False)

    def verify_password(self): #공인인증서 로그인
        if self.login == True:
            print("\n이미 로그인상태입니다.")
        elif self.login == False:
            print("\n공인인증서 로그인을 진행합니다.")
            while True:
                data1 = input("이름을 입력해주세요. [0.나가기] : ")
                if data1 == "0":
                    break
                elif dict1.get(data1) == None:
                    print("이름이 존재하지 않습니다.")
                else:
                    print(f"반갑습니다 {data1}님")
                    break

            while True:
                if data1 == "0":
                    break
                data2 = input("비밀번호를 입력해주세요. [0.나가기] : ")
                hashed_pw = hashlib.sha256(data2.encode()).hexdigest()
                if data2 == "0":
                    break
                elif dict1.get(data1) == hashed_pw:
                    print("\n로그인 성공")
                    self.login = True
                    break
                else:
                    print("\n비밀번호를 다시 입력해주세요.")

    def logout_user(self): #공인인증서 로그아웃
        if self.login == False:
            print("\n이미 로그아웃상태입니다.")
        elif self.login == True:
            data3 = input("\n로그아웃 하시겠습니까? [1.예/2.아니오] : ")
            if data3 == "1":
                print("\n로그아웃이 완료되었습니다.")
                self.login = False
            elif data3 == "2":
                print("\n로그아웃이 취소되었습니다.")

    def test_bank(self):
        if self.login == False:
            print("\n공인인증서 로그인 후 이용해주세요.")
        elif self.login == True:
            print("\n개발중입니다..")

user1 = LoginManager()



print("반갑습니다")
while True:
    print(f'''
--모두연은행 관리시스템--
1. 공인인증서 만들기
2. 공인인증서 로그인
3. 로그아웃
4. 계좌이체
0. 나가기''')
    select_menu = input("사용하실 기능을 선택해주세요.")
    
    if select_menu == "1":
        user1.issue_certificate()
    elif select_menu == "2":
        user1.verify_password()
    elif select_menu == "3":
        user1.logout_user()
    elif select_menu == "4":
        user1.test_bank()
    elif select_menu == "0":
        print("안녕히 가세요!")
        break
        


