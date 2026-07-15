# DummyDataGenerator

## 개요
테스트용 JSON 더미 데이터를 생성하는 도구의 PoC(Proof of Concept) 프로젝트입니다.

## 핵심 컨셉
- 로컬에 저장된 JSON 파일을 **스키마/템플릿**으로 사용합니다.
- 템플릿 JSON은 콘솔 애플리케이션이 실제로 다룰 데이터 구조를 그대로 반영할 수 있으며,
  `templates/sample_user.json`과 다른 임의의 구조(필드 구성, 중첩 깊이, 배열 등)도 그대로 읽어
  동일한 구조를 유지하면서 값만 랜덤하게 채운 더미 데이터를 생성합니다.
- 자동 추론만으로 부족한 필드는 **힌트 파일**을 통해 개발자가 필드별 타입을 직접 지정할 수 있습니다.
- 생성된 더미 데이터는 테스트 코드/테스트 환경에서 사용하는 것을 목표로 합니다.

## 현재 상태
PoC 구현이 완료되어 로컬에서 동작을 확인했습니다. Python 3.13, 외부 의존성 없이 표준 라이브러리(`random`, `string`, `uuid`, `datetime`)만 사용합니다.

### 구조
- `dummy_data_generator/generator.py` — 핵심 생성 로직 (템플릿 재귀 순회, 경로 기반 힌트 적용)
- `dummy_data_generator/type_registry.py` — 지원하는 값 타입과 필드명 기반 자동 추론 규칙
- `dummy_data_generator/hints.py` — 힌트 파일 로딩 및 기본 경로 규칙
- `main.py` — CLI 엔트리포인트
- `templates/sample_user.json` — 예시 템플릿
- `templates/sample_user_hints.json` — 예시 힌트 파일
- `tests/test_generator.py` — unittest 기반 테스트 (임의 구조 템플릿, 힌트 오버라이드 포함)
- `output/` — 생성 결과 저장 위치 (기본값, 결과물은 git에 커밋하지 않음)

### 결정된 규칙
- **템플릿은 임의 구조 허용**: 템플릿 JSON의 키 구성이나 중첩 구조에 제약이 없습니다. 콘솔 앱에서 쓰는 실제 예시 JSON을 그대로 `templates/`에 넣고 `--template`으로 지정하면 됩니다.
- **타입 추론(기본값)**: 힌트가 없는 필드는 템플릿 값의 파이썬 타입(int/float/bool/str/None)을 유지하며 값만 랜덤 생성합니다.
- **필드명 기반 추론(기본값)**: 문자열 필드는 키 이름 패턴(`email`, `name`, `phone`, `city`, `zipcode`, `url`, `date`/`_at`, `id`)을 우선 확인해 그럴듯한 값을 생성하고, 매칭되지 않으면 랜덤 문자열로 대체합니다.
- **배열**: 첫 번째 요소를 템플릿으로 사용해 1~3개의 항목을 랜덤 생성 (빈 배열은 빈 배열 유지)
- **중첩 객체**: 재귀적으로 동일한 규칙 적용
- **출력 방식**: CLI에서 JSON 파일로 저장 (`--output`), 개수(`--count`)와 시드(`--seed`)로 재현 가능

### 힌트 파일로 필드 타입 직접 지정하기
자동 추론이 원하는 결과를 만들지 못하거나(예: 정수 `id`를 UUID 문자열로 바꾸고 싶은 경우), 특정 값 범위/후보군을 강제하고 싶을 때 힌트 파일을 사용합니다.

**파일 위치 규칙**: `--hints`를 지정하지 않으면 `<템플릿파일명>_hints.json`을 템플릿과 같은 폴더에서 자동으로 찾습니다.
예) `templates/sample_user.json` → `templates/sample_user_hints.json`

**경로(key) 표기법**:
- 최상위 필드: `"age"`
- 중첩 객체 필드: `"address.city"` (점으로 연결)
- 배열 항목: `"tags[]"` (배열 필드명 뒤에 `[]`를 붙임)

**지원 타입** (`dummy_data_generator/type_registry.py`의 `TYPE_REGISTRY`):

| type 값 | 설명 | 추가 파라미터 |
|---|---|---|
| `email` | 랜덤 이메일 | - |
| `name` | 샘플 이름 목록 중 랜덤 선택 | - |
| `phone` | `010-xxxx-xxxx` 형식 | - |
| `city` | 샘플 도시 목록 중 랜덤 선택 | - |
| `zipcode` | 5자리 숫자 문자열 | - |
| `url` | 랜덤 URL | - |
| `date` | ISO 8601 날짜/시간 문자열 | - |
| `uuid` | UUID4 문자열 | - |
| `string` | 랜덤 소문자 문자열 | `length` (기본 8) |
| `int_range` | 범위 내 랜덤 정수 | `min`, `max` |
| `float_range` | 범위 내 랜덤 실수(소수 2자리) | `min`, `max` |
| `bool` | 랜덤 true/false | - |
| `enum` | 지정한 목록 중 랜덤 선택 | `values` (리스트, 필수) |

**예시** (`templates/sample_user_hints.json`):
```json
{
  "id": { "type": "uuid" },
  "age": { "type": "int_range", "min": 18, "max": 65 },
  "score": { "type": "float_range", "min": 0, "max": 100 },
  "address.city": { "type": "enum", "values": ["Seoul", "Busan", "Jeju"] },
  "tags[]": { "type": "enum", "values": ["admin", "user", "guest", "vip"] }
}
```
힌트가 지정된 필드는 템플릿 값의 원래 타입과 무관하게 힌트의 `type`을 우선 적용합니다 (예: 템플릿에서 `id`가 정수여도 힌트로 `uuid`를 지정하면 문자열로 생성됩니다).

**새 타입 추가 방법**: `dummy_data_generator/type_registry.py`에 `_gen_xxx(**params)` 함수를 작성하고 `TYPE_REGISTRY` 딕셔너리에 이름을 등록하면, 힌트 파일에서 바로 `"type": "xxx"`로 사용할 수 있습니다.

### 실행 방법
```
.venv/Scripts/python.exe main.py --template templates/sample_user.json --count 3 --output output/dummy_data.json
# 힌트 파일을 명시적으로 지정하려면:
.venv/Scripts/python.exe main.py --template templates/my_app.json --hints templates/my_app_hints.json --count 3
```

## 향후 확장 아이디어
- 배열 반복 개수를 CLI 옵션(또는 힌트)으로 노출
- 필드명 기반 추론 규칙 확장 (주소, 통화, 국가 코드 등)
- 여러 템플릿 파일을 한 번에 처리하는 배치 모드
