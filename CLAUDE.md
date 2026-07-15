# DummyDataGenerator

## 개요
테스트용 JSON 더미 데이터를 생성하는 도구의 PoC(Proof of Concept) 프로젝트입니다.

## 핵심 컨셉
- 로컬에 저장된 JSON 파일을 **스키마/템플릿**으로 사용합니다.
- 템플릿 JSON의 필드 구조와 타입(문자열, 숫자, 불리언, 배열, 중첩 객체 등)을 분석하여,
  동일한 구조를 유지하면서 값만 랜덤하게 채운 더미 데이터를 생성합니다.
- 생성된 더미 데이터는 테스트 코드/테스트 환경에서 사용하는 것을 목표로 합니다.

## 현재 상태
PoC 구현이 완료되어 로컬에서 동작을 확인했습니다. Python 3.13, 외부 의존성 없이 표준 라이브러리(`random`, `string`, `uuid`, `datetime`)만 사용합니다.

### 구조
- `dummy_data_generator/generator.py` — 핵심 생성 로직
- `main.py` — CLI 엔트리포인트
- `templates/sample_user.json` — 예시 템플릿
- `tests/test_generator.py` — unittest 기반 테스트
- `output/` — 생성 결과 저장 위치 (기본값)

### 결정된 규칙
- **타입 추론**: 템플릿 값의 파이썬 타입(int/float/bool/str/None)을 그대로 유지하며 값만 랜덤 생성
- **필드명 기반 추론**: 문자열 필드는 키 이름 패턴(`email`, `name`, `phone`, `city`, `zipcode`, `url`, `date`/`_at`, `id`)을 우선 확인해 그럴듯한 값을 생성하고, 매칭되지 않으면 랜덤 문자열로 대체
- **배열**: 첫 번째 요소를 템플릿으로 사용해 1~3개의 항목을 랜덤 생성 (빈 배열은 빈 배열 유지)
- **중첩 객체**: 재귀적으로 동일한 규칙 적용
- **출력 방식**: CLI에서 JSON 파일로 저장 (`--output`), 개수(`--count`)와 시드(`--seed`)로 재현 가능

### 실행 방법
```
.venv/Scripts/python.exe main.py --template templates/sample_user.json --count 3 --output output/dummy_data.json
```

## 향후 확장 아이디어
- 배열 반복 개수를 CLI 옵션으로 노출
- 필드명 기반 추론 규칙 확장 (주소, 통화, 국가 코드 등)
- 여러 템플릿 파일을 한 번에 처리하는 배치 모드
