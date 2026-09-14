import json
import time

# ---------------------------------------
# [1] MAC 연산
# ---------------------------------------
def calculate_mac(pattern,filter_):
    size=len(pattern)
    total=0
    for i in range(size):
        for j in range(size):
            product=pattern[i][j]*filter_[i][j]
            total+=product
    return total
# ---------------------------------------
# [2] 라벨 정규화
# ---------------------------------------
def normalize_label(label):
    """'+' -> 'Cross', 'x'/'cross' -> 표준 라벨로 변환"""
    label=label.strip().lower()
    if label=='+' or label=='cross':
        return 'Cross'
    if label=='x' :
        return 'X'
    return label
# ---------------------------------------
# [3] 모드 1: 사용자 입력 (3x3)
# ---------------------------------------
def input_grid_3x3(prompt):
    """3줄 입력받아 3x3 2차원 리스트로 반환, 입력 검증 포함"""
    print(prompt)
    grid = []
    while len(grid)<3: #3x3 행렬 완성시 루프 종료
        try:
            line = input()          # 한 줄 입력받기
            numbers = line.split()  # 공백 기준으로 쪼개기 -> 문자열 리스트
            if len(numbers)!=3:
                print("입력 형식 오류. 다시 입력하세요. ")
                continue
            else:
                temp=[]
                temp.append(float(numbers[0]))
                temp.append(float(numbers[1]))
                temp.append(float(numbers[2]))
        except ValueError:
            print("입력 형식 오류. 다시 입력하세요. ")
            continue
        grid.append(temp)
    return grid

def run_mode_1():
    filter_a=input_grid_3x3("필터 A (3줄 입력, 공백 구분)")
    filter_b=input_grid_3x3("필터 B (3줄 입력, 공백 구분)")
    pattern=input_grid_3x3("패턴 (3줄 입력, 공백 구분)")
    a=calculate_mac(pattern,filter_a)
    b=calculate_mac(pattern,filter_b)
    if abs(a-b)<1e-9:
        result='판정 불가'
    elif a>b:
        result='A'
    else: 
        result='B'
    average_time = measure_performance(pattern, filter_a)

    print(f"A 점수: {a}")
    print(f"B 점수: {b}")
    print(f"연산 시간(평균/10회): {average_time:.6f} ms")
    print(f"판정: {result}")

    


# ---------------------------------------
# [4] 모드 2: data.json 로드 및 검증
# ---------------------------------------
def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data=json.load(f)

        return data
    except (FileNotFoundError,json.JSONDecodeError):
        print("파일 읽기 오류")
        return None

def extract_size_from_key(pattern_key):
    """'size_5_1' 같은 키에서 크기(5)를 정수로 뽑아 반환"""
    try:
        parts = pattern_key.split("_")

        if len(parts) < 2 or parts[0] != "size":
            return None

        return int(parts[1])

    except (ValueError, IndexError):
        return None

def sizes_match(filter_grid, pattern_grid):
    """필터와 패턴의 행/열 크기가 같은지 확인"""

    if len(filter_grid) != len(pattern_grid):
        return False

    if not filter_grid or not pattern_grid:
        return False

    if len(filter_grid[0]) != len(pattern_grid[0]):
        return False

    return True

def process_pattern(pattern_key, pattern_data, filters):
    """패턴 하나를 처리해서 판정, PASS/FAIL, 사유, 점수를 반환"""

    # 1. 패턴 키에서 크기 추출
    size = extract_size_from_key(pattern_key)

    if size is None:
        return None, "FAIL", "패턴 키 형식이 올바르지 않음", None, None

    # 2. 해당 크기의 필터 선택
    filter_key = f"size_{size}"

    if filter_key not in filters:
        return None, "FAIL", f"{filter_key} 필터를 찾을 수 없음", None, None

    # 3. 필터와 패턴 데이터 가져오기
    filter_set = filters[filter_key]
    pattern_grid = pattern_data["input"]

    # 4. Cross 필터와 패턴 크기 확인
    if not sizes_match(filter_set["cross"], pattern_grid):
        return None, "FAIL", "Cross 필터와 패턴의 크기 불일치", None, None

    # 5. X 필터와 패턴 크기 확인
    if not sizes_match(filter_set["x"], pattern_grid):
        return None, "FAIL", "X 필터와 패턴의 크기 불일치", None, None

    # 6. Cross 필터로 MAC 연산
    result_cross = calculate_mac(
        pattern_grid,
        filter_set["cross"]
    )

    # 7. X 필터로 MAC 연산
    result_x = calculate_mac(
        pattern_grid,
        filter_set["x"]
    )

    # 8. epsilon을 이용해 판정
    if abs(result_cross - result_x) < 1e-9:
        result = "UNDECIDED"
    elif result_cross > result_x:
        result = "Cross"
    else:
        result = "X"

    # 9. expected 값 정규화
    normalized_expected = normalize_label(
        pattern_data["expected"]
    )

    # 10. 판정 결과와 expected 비교
    if result == normalized_expected:
        return result, "PASS", None, result_cross, result_x
    else:
        reason = "예상 결과와 다릅니다."
        return result, "FAIL", reason, result_cross, result_x
    
def run_mode_2():
    data = load_json("data.json")

    if data is None:
        return

    filters = data["filters"]
    patterns = data["patterns"]

    fail_list = []

    total = 0
    passed = 0

    print("\n----------------------------------------")
    print("[1] 패턴 분석")
    print("----------------------------------------")

    for pattern_key, pattern_data in patterns.items():

        judgement, pass_fail, reason, score_cross, score_x = process_pattern(
            pattern_key,
            pattern_data,
            filters
        )

        total += 1

        if pass_fail == "PASS":
            passed += 1
        else:
            fail_list.append((pattern_key, reason))

        print(f"\n[{pattern_key}]")

        if score_cross is not None:
            print(f"Cross 점수: {score_cross}")
            print(f"X 점수: {score_x}")

        print(f"판정: {judgement}")
        print(f"expected: {normalize_label(pattern_data['expected'])}")
        print(f"결과: {pass_fail}")

        if reason is not None:
            print(f"사유: {reason}")

    run_performance_analysis()

    failed = total - passed

    print("\n----------------------------------------")
    print("[3] 결과 요약")
    print("----------------------------------------")

    print(f"총 테스트: {total}개")
    print(f"통과: {passed}개")
    print(f"실패: {failed}개")

    if fail_list:
        print("\n실패 케이스:")

        for key, reason in fail_list:
            print(f"- {key}: {reason}")

# ---------------------------------------
# [5] 성능 측정
# ---------------------------------------
def measure_performance(pattern, filter_, repeat=10):
    """MAC 연산을 repeat번 반복 측정하여 평균 시간(ms) 반환"""
    total=0
    for i in range(repeat):
        start=time.time()
        calculate_mac(pattern, filter_)
        end=time.time()
        elapsed= end - start
        total+=elapsed
    average_ms=(total/repeat)*1000
    return average_ms
    #print(f"{average_time}ms")

def run_performance_analysis():
    data = load_json("data.json")
    if data is None:
        return

    filters = data["filters"]
    patterns = data["patterns"]

    print("\n----------------------------------------")
    print("[2] 성능 분석")
    print("----------------------------------------")
    print(f"{'크기':<10} | {'평균 시간(ms)':<15} | {'연산 횟수':<10}")
    print("-" * 45)

    for size in [5, 13, 25]:
        # 해당 크기의 필터 찾기
        filter_key = f"size_{size}"

        if filter_key not in filters:
            print(f"{size}x{size:<7} | 필터 없음")
            continue

        filter_grid = filters[filter_key]["cross"]

        # 해당 크기의 패턴 하나 찾기
        pattern_grid = None

        for pattern_key, pattern_data in patterns.items():
            if extract_size_from_key(pattern_key) == size:
                pattern_grid = pattern_data["input"]
                break

        if pattern_grid is None:
            print(f"{size}x{size:<7} | 패턴 없음")
            continue

        avg_time = measure_performance(
            pattern_grid,
            filter_grid,
            repeat=10
        )

        operation_count = size ** 2

        print(
            f"{size}x{size:<7} | "
            f"{avg_time:<15.6f} | "
            f"{operation_count:<10}"
        )
# ---------------------------------------
# [6] 메인 실행
# ---------------------------------------
def main():
    print("=== Mini NPU Simulator ===")
    print("1. 사용자 입력 (3x3)")
    print("2. data.json 분석)")
    
    choice = input("선택 (1 또는 2): ").strip()
    if choice == "1":
        run_mode_1()
    elif choice == "2":
        run_mode_2()
    else:
        print("잘못된 입력입니다.")

if __name__ == "__main__":
    main()