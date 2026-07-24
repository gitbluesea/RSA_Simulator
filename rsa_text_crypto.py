import math

def is_prime(n):
    """소수 판별"""
    if n < 2:
        return False
    for i in range(2, int(math.isqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def get_mod_inverse(e, phi):
    """모듈러 역수 구하기"""
    try:
        return pow(e, -1, phi)
    except ValueError:
        return None

def encrypt_string(text, e, n):
    """문자열을 한 글자씩 암호화하여 숫자 리스트로 반환"""
    cipher_list = []
    for char in text:
        # ord(char)를 통해 문자를 아스키(ASCII) 숫자로 변환 (예: 'A' -> 65)
        m = ord(char)
        if m >= n:
            raise ValueError(f"문자 '{char}'(값:{m})의 아스키 코드가 모듈러스 n({n})보다 큽니다. 더 큰 소수를 사용하세요.")
        c = pow(m, e, n)
        cipher_list.append(c)
    return cipher_list

def decrypt_string(cipher_list, d, n):
    """암호화된 숫자 리스트를 한 글자씩 복호화하여 문자열로 합침"""
    decrypted_chars = []
    for c in cipher_list:
        m = pow(c, d, n)
        # chr(m)을 통해 숫자를 다시 문자로 복원
        decrypted_chars.append(chr(m))
    return "".join(decrypted_chars)

def run_rsa_text_crypto():
    print("=== 영어 문자열 RSA 암호화/복호화 프로그램 ===")
    print("* 문자 암호화를 위해 이전보다 조금 더 큰 소수를 입력하는 것을 추천합니다. (예: p=61, q=53)")
    
    # 1. 소수 입력 받기
    try:
        p = int(input("첫 번째 소수 (p)를 입력하세요 (추천: 61): "))
        q = int(input("두 번째 소수 (q)를 입력하세요 (추천: 53): "))
    except ValueError:
        print("[오류] 올바른 정수를 입력해주세요.")
        return

    if not is_prime(p) or not is_prime(q):
        print("[오류] 입력한 값 중 소수가 아닌 수가 있습니다.")
        return
    if p == q:
        print("[오류] 서로 다른 두 개의 소수를 입력해야 합니다.")
        return

    n = p * q
    phi = (p - 1) * (q - 1)

    # 2. 공개 지수 e 추천 및 선택
    e_candidates = [i for i in range(3, phi) if math.gcd(i, phi) == 1]
    print(f"\n* 추천하는 e 값 목록 (앞에서 5개): {e_candidates[:5]}")
    try:
        e = int(input(f"사용할 공개 지수 (e)를 선택하세요 (추천: {e_candidates[0] if e_candidates else ''}): "))
    except ValueError:
        print("[오류] 정수를 입력해주세요.")
        return

    if e not in e_candidates:
        print(f"[오류] 선택한 e({e})는 phi(n)인 {phi}와 서로소가 아닙니다.")
        return

    # 3. 개인 키 d 계산
    d = get_mod_inverse(e, phi)
    
    print("\n" + "-"*40)
    print(f" 키 생성 완료!")
    print(f" - 공개 키: (e={e}, n={n})")
    print(f" - 개인 키: (d={d}, n={n})")
    print("-"*40)

    # 4. 영어 문자열 입력 받기
    text = input("\n암호화할 영어 문자열을 입력하세요 (예: Hello RSA): ")
    if not text:
        print("[오류] 문자열이 비어있습니다.")
        return

    # 5. 암호화 진행
    try:
        cipher_result = encrypt_string(text, e, n)
    except ValueError as e_msg:
        print(f"[오류] {e_msg}")
        return

    # 6. 복호화 진행
    decrypted_result = decrypt_string(cipher_result, d, n)

    # 결과 출력
    print("\n" + "="*40)
    print("   [ RSA 문자열 연산 결과 ]")
    print("="*40)
    print(f"* 입력한 평문: {text}")
    print(f"* 암호화된 데이터 (숫자 배열): \n  {cipher_result}")
    print(f"\n* 복호화된 결과: {decrypted_result}")
    
    if text == decrypted_result:
        print("\n[성공] 복호화된 문자열이 원본과 정확히 일치합니다!")
    else:
        print("\n[실패] 복호화 결과가 원본과 다릅니다.")
    print("="*40)

if __name__ == "__main__":
    run_rsa_text_crypto()
