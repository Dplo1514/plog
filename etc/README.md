# plog Local 환경 구성

> 1. 해당 README.md 문서는 plog project 의 Local 개발 환경 구성에 관하여 서술 합니다.
> 2. 해당 문서를 바탕으로 개발 환경 구성 진행 후 plog project 의 정상 구동이 불가능 할 시 아래 기재된 담당자 에게 연락 바랍니다.
     >    * 임인혁 : dladlsgur3334@gmail.com

## 0.주의사항(선행작업)
- 환경 설정을 진행 하는 개발자의 local 환경에는 아래의 세가지 package가 존재 해야한다.
  - brew

## 1. podman install
```bash
# 1. brew로 podman install
brew install podman  
brew install podman-compose
# 2. podman machine 실행  
podman machine init  
podman machine start
# 3. machine 실행 여부 확인
podman machine list
```

## 2. podman compose Start
```bash
# 1. plog/etc 경로에서 실행
cd etc
# 2. podman compose container set 실행
podman-compose up -d
```