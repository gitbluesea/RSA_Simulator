import math

def is_prime(n):
    """소수 판별 함수"""
    if n < 2:
        return False
    for i in range(2, int(math.isqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def get_gcd(a, b):
    """최대공약수 구하기"""
    return math.gcd(a, b)

def get_mod_inverse(e, phi):
    """모듈러 역수 (d) 구하기: (e * d) % phi == 1"""
    try:
        return pow(e, -1, phi)
    except ValueError:
        return None

def run_rsa_example():
    print("=== RSA 암호화/복호화 시뮬레이터 ===")
    
    # 1. 소수 입력 받기
    try:
        p = int(input("첫 번째 소수 (p)를 입력하세요 (예: 3): "))
        q = int(input("두 번째 소수 (q)를 입력하세요 (예: 11): "))
    except ValueError:
        print("[오류] 올바른 정수를 입력해주세요.")
        return

    if not is_prime(p) or not is_prime(q):
        print("[오류] 입력한 값 중 소수가 아닌 수가 있습니다. 반드시 소수를 입력해주세요.")
        return
    if p == q:
        print("[오류] 서로 다른 두 개의 소수를 입력해야 합니다.")
        return

    # 2. n 및 phi(n) 계산
    n = p * q
    phi = (p - 1) * (q - 1)

    # 3. 공개 키 e 선택 (phi와 서로소인 가장 작은 홀수/또는 사용자 입력 추천)
    # 실제로는 65537을 주로 쓰지만, 작은 예시를 위해 phi와 서로소인 작은 수를 자동 탐색
    e_candidates = [i for i in range(3, phi) if get_gcd(i, phi) == 1]
    if not e_candidates:
        print("[오류] 적절한 공개 키(e)를 찾을 수 없습니다. 더 큰 소수를 입력하세요.")
        return
    
    print(f"\n* 추천하는 e 값 목록: {e_candidates[:5]}")
    try:
        e = int(input(f"사용할 공개 지수 (e)를 선택하세요 (추천: {e_candidates[0]}): "))
    except ValueError:
        e = e_candidates[0]

    if e not in e_candidates:
        print(f"[오류] 선택한 e({e})는 phi(n)인 {phi}와 서로소가 아닙니다.")
        return

    # 4. 개인 키 d 계산
    d = get_mod_inverse(e, phi)

    # 5. 평문 입력 받기
    try:
        message = int(input(f"\n암호화할 메시지 정수 (M)을 입력하세요 (M < {n}): "))
    except ValueError:
        print("[오류] 숫자를 입력해주세요.")
        return

    if message >= n:
        print(f"[오류] 메시지 M은 모듈러스 n({n})보다 작아야 정상적으로 복호화됩니다.")
        return

    # 6. 암호화 연산
    cipher = pow(message, e, n)

    # 7. 복호화 연산
    decrypted = pow(cipher, d, n)

    # 결과 출력 (설명 양식 일치)
    print("\n" + "="*40)
    print("   [ RSA 연산 및 결과 시각화 ]")
    print("="*40)
    print(f"* 조건: p = {p}, q = {q}로 가정")
    print(f"* 계산:")
    print(f"    - n = {p} × {q} = {n}")
    print(f"    - φ(n) = ({p}-1) × ({q}-1) = {phi}")
    print(f"    - e = {e} 선택 (φ(n)={phi}와 서로소)")
    print(f"    - {e} × d ≡ 1 (mod {phi})을 만족하는 d = {d} 결정 ({e} × {d} = {e*d} ≡ 1)")
    print(f"    - 공개 키: ({e}, {n}) / 개인 키: ({d}, {n})")
    print(f"* 암호화: 보낼 메시지 M = {message} 일 때")
    print(f"    - C = {message}^{e} (mod {n}) = {message**e} (mod {n}) = **{cipher}**")
    print(f"* 복호화: 암호문 C = {cipher}를 받았을 때")
    # 파이썬에서 거듭제곱 값이 너무 커져 출력 오류가 나는 것을 방지하기 위해 조건부 출력
    if cipher**d < 10**15:
        print(f"    - M = {cipher}^{d} (mod {n}) = {cipher**d} (mod {n}) = **{decrypted}** (원래 메시지 복원)")
    else:
        print(f"    - M = {cipher}^{d} (mod {n}) = **{decrypted}** (원래 메시지 복원)")
    print("="*40)

if __name__ == "__main__":
    run_rsa_example()
