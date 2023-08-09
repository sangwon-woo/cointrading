# Coin Trading

## Project Architecture
- autotrading : project home
- conf : 환경설정이나 사용자 정보를 보관
- logs : 프로젝트가 구동될 때 생성되는 로그를 보관
- notebooks : 데이터 분석을 위한 주피터 노트북 보관
- tests : 개발하면서 필요한 테스트 모듈을 보관

## autotrading
- db : 데이터베이스 작업을 위한 파이썬 모듈
- machine : 거래소 모듈이 저장되는 디렉터리
- scheduler : 주기적으로 구동하기 위한 모듈
- strategy : 트레이딩 로직이 들어가는 디렉터리
- pusher : 메신저로 푸시하기 위한 모듈이 들어가는 디렉터리
# cointrading
