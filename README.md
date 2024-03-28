# 방주로의 초대장
### Skillflo의 강의를 오프라인 환경에서 받을 수 있도록 합니다.

>주의! 해당 프로그램을 악용해서 강의를 임의로 배포하거나 판매하는 경우 책임을 지지 않습니다!

---
## 사용법

1. 해당 깃 주소를 본인의 기기에 클론합니다.
```
git clone https://github.com/stoneHee99/invitation-to-ark.git
```

2. 가상 환경을 생성하고 활성화 합니다.
```
    python -m venv .venv
```

3. 생성된 가상환경을 활성화합니다.
- Windows
```
    .venv\Scripts\activate
```
- macOS
```
    source .venv/bin/activate
```

4. 의존성을 설치합니다
```
    pip install -r requirements.txt
```

5. 프로젝트를 실행합니다
```
    python src/main.py
```

---

## 주요 기능

- `Selenium` 을 활용한 로그인 및 비디오 다운로드
- 멀티 스레딩 기법을 적용하여 이미지 다운로드 병렬 처리 및 성능 개선
- 기존 복잡한 과정을 거칠 필요없이 커맨드 기반의 편리한 다운로드 환경

