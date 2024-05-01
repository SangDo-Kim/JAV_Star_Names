This Python program reads file names in a folder which is containing JAV (Japanese Adult Video) files, and put a star (actress) name in Korean to each files. 
이 파이썬 프로그램은 JAV(일본 야동) 파일이 포함된 폴더와 모든 하위 폴더의 파일 이름들을 읽은 후 출연자(여배우) 이름을 한글로 각 파일에 붙입니다.
JAV 파일 이름은 품번(예: JEL-223)을 포함해야 합니다.
Written by SangDo_Kim in AVDBS.com

유효한 JAV 파일 이름:
[HD]JUL-222 유모 야동.mp4 (품번이 맨 앞에 있지 않아도 상관 없음)
CutyGirl.JUL-222-Uncensored.srt (자막 파일이라도 상관 없음)
JUL222 High Quality.mp4             (품번이 영문자가 2~3개이고 숫자가 3개인 경우 중간에 대시 '-'가 없어도 품번으로 인식)

유효하지 않은 파일 이름:
히마리 야동.mp4         (품번이 없음)
히마리 JUL 222.mp4    (품번 중간에 공백이 있으면 안 됨)

출연자 정보는 구글 영국에 저장된 AVDBS.com의 페이지 제목에서 읽어 옵니다.
-----------------------------
V1.12 변경 사항
- 출연자 구분자를 4개로 제한: "#", "^", "`", "출)"
   기존에 허용했던 구분자 "@", "$", ";"는 파일 이름에서 흔히 사용되므로 구분자로 쓰지 않기로 함.
- 품번 인식: 특수 문자(@, $, ', & 등)이 포함된 파일 이름에서 품번 인식을 제대로 하지 못함.
예) HD@JUL-333의 품번을 HDJUL-333으로 잘못 인식했음. 이를 JUL-333로 바로 잡음.

V1.13 변경 사항
- 품번 인식: 품번 뒤에 대시가 또 붙어 있는 경우 품번 인식 오류
   예) JUL-333-Uncensored.mp에서 품번을 JUL-333-으로 잘못 인식하던 것을 바로 잡음.
- 독립 실행 파일(EXE 파일)이 실행 안 되는 문제 해결(특정 모듈이 포함 안 됨)

V1.14 변경 사항
- 품번 인식 개선
