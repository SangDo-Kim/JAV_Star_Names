#JAV Star Names Finder V1.14
#Written by SangDo_Kim, a user in AVDBS.com
#Anyone can freely change the code and use it for their usage, but please put the original writer -
#SangDo_Kim in their changed program.
#원하는 대로 수정해도 좋으나, 원작자 SangDo_Kim 이름을 수정된 프로그램에 기록해 주시기 바랍니다.

import os
import tkinter
from tkinter import filedialog
import sys
import time
import random
from bs4 import BeautifulSoup
import requests
from fnChangePrevSeparator import fnChangePrevSeparator, ErrNoWork
from JAV_ProdCode import fnExtractProdCode, ErrNoCode, lVideoFormats
from fnAddStarName import fnAddStarName

print("""JAV Star Names Finder, Written by SangDo_Kim, a user in AVDBS.com.
이 파이썬 프로그램은 JAV(일본 야동) 파일이 포함된 폴더와 그 하위 폴더들의 파일 이름들을 읽은 후, 
출연자(여배우) 이름을 한글로 각 파일에 붙입니다. JAV 파일 이름은 품번(예: JEL-223)을 포함해야 합니다.
출연자 정보는 구글 영국에 저장된 AVDBS.com의 페이지 제목에서 읽어 옵니다.""")
print("""이 프로그램은 출연자를 파일 이름 앞에 붙이거나 뒤에 붙일 수도 있으며, 
출연자 구분자를 선택할 수도 있습니다(예: 출), #, 등).""")

# 기존 설정 기본값 입력
sStarPosition = "b"
sStarSeparator = "#"
sStarPositionPrev = ""
sStarSeparatorPrev = ""
sWorkingPath = ""

#기존 설정 변수 읽어 오기(프로그램이 실행되는 경로에 JAV_Star_Names_Config.txt 설정 파일이 있는 경우).
dictConfig = {}
if os.path.isfile("JAV_Star_Names_Config.txt"):
    fileConfig = open("JAV_Star_Names_Config.txt", "r")
    lLines = fileConfig.readlines()
    for sLine in lLines:
        lLineSplit = sLine.split("=")
        dictConfig[lLineSplit[0].strip()] = lLineSplit[1].strip()
    fileConfig.close()
    try:
        sStarPosition = dictConfig["sStarPosition"]
    except KeyError:
        print(">>>기존 설정 파일 읽기 오류: sStarPosition. 기본 설정 적용.")
        sStarPosition = "b"
    try:
        sStarSeparator = dictConfig["sStarSeparator"]
    except KeyError:
        print(">>>기존 설정 파일 읽기 오류: sStarSeparator. 기본 설정 적용.")
        sStarSeparator = "#"
    try:
        sStarPositionPrev = dictConfig["sStarPositionPrev"]
    except KeyError:
        print(">>>기존 설정 파일 읽기 오류: sStarPositionPrev. 기본 설정 적용.")
        sStarPositionPrev = "b"
    try:
        sStarSeparatorPrev = dictConfig["sStarSeparatorPrev"]
    except KeyError:
        print(">>>기존 설정 파일 읽기 오류: sStarSeparatorPrev. 기본 설정 적용.")
        sStarSeparatorPrev = "출)"
    try:
        sWorkingPath = dictConfig["sWorkingPath"]
    except KeyError:
        print(">>>기존 설정 파일 읽기 오류: sWorkingPath. 기본 설정 적용.")
        sWorkingPath = ""

#기본 옵션으로 할지, 각 옵션을 사용자가 지정할지 질문
print("-"*10)
print(f"<기본 설정>")
#기존 구분자와 현재 구분자, 배치 위치가 다른 경우에만 기존 형태 표시
if sStarPositionPrev == "" or sStarSeparatorPrev == "":
    print(f"이 버전의 프로그램을 처음 실행하는 경우 파일 이름에 배우 구분자는 없는 것으로 간주합니다.\n"
        +"주의: 만일 이전 버전의 프로그램을 사용하여 '출)'을 붙여 출연자를 구분하여 기록했던 경우, 아래 단계에서 사용자 지정을 선택해야 합니다.")

if sStarPosition == "b":
    print(f"기본 파일 이름 형태(예시): JUL-756 동급생 {sStarSeparator}미즈노 아사히.mp4")
else:
    print(f"기본 파일 이름 형태(예시): 미즈노 아사히{sStarSeparator} JUL-756 동급생.mp4")

#기본 설정대로 할지, 사용자 설정할지 질문

print("위에 표시된 기본 파일 이름 형태로 실행하시겠습니까?")
print(f"주의: 구분자 '{sStarSeparator}'(이)가 아닌 다른 구분자를 사용하려고 하거나 기존 구분자가 다른 것이었다면 사용자 지정을 선택해야 합니다.")
while True:
    sDefault = str(input("기본 설정 [a] 또는 사용자 지정 [b]: "))
    sDefault = sDefault.lower()
    if sDefault not in ("a", "b"):
        continue
    else:
        break

#사용자 설정을 선택한 경우
if sDefault == "b":
    print("-" * 10)
    while True:  #출연자 이름을 앞에 붙일지, 뒤에 붙일지 선택
        sStarPosition = str(input("출연자 이름을 파일 이름 앞에 붙일까요[a], 뒤에 붙일까요[b]? "))
        sStarPosition = sStarPosition.lower()
        if sStarPosition not in ("a", "b"):
            continue
        else:
            break

    print("-" * 10)  #출연자 구분자를 어떤 문자로 할지 결졍
    lPossibleSeparators = ["#", "^", "`", "출)"]
    while True:
        print(f"출연자 이름을 구분하기 위해 어떤 특수 문자를 붙일까요?")
        sStarSeparator = str(input(f"다음 중 하나를 입력하십시오(따옴표 빼고 입력). {lPossibleSeparators}: "))
        if sStarSeparator not in lPossibleSeparators:
            continue
        else:
            break
    if sStarPosition == "a":
        print(f"다음과 같이 변경될 예정입니다: 미즈노 아사히{sStarSeparator} JUL-756 동급생에게 돌려짐.mp4")
    else:
        print(f"다음과 같이 변경될 예정입니다: JUL-756 동급생에게 돌려짐 {sStarSeparator}미즈노 아사히.mp4")

    print("-" * 10)  #기존의 출연자 구분자가 무엇이었는지 질문
    while True:
        print(f"기존에 쓰던 출연자 이름 구분자는 무엇이었습니까?")
        sStarSeparatorPrev = str(input(f"기존 구분자가 없었던 경우 그냥 엔터 입력: {lPossibleSeparators}: "))
        sStarSeparatorPrev = sStarSeparatorPrev.lower()
        if sStarSeparatorPrev == "":
            break
        elif sStarSeparatorPrev not in lPossibleSeparators:
            continue
        else:
            break

    if sStarSeparatorPrev == "":
        sStarPositionPrev = ""
    else:
        print("-" * 10)  # 기존의 출연자 위치 질문
        while True:
            sStarPositionPrev = str(input(f"기존에 출연자 이름이 파일 이름 앞에 붙었었나요[a], 뒤에 붙었었나요[b]? "))
            if sStarPositionPrev not in ("a", "b"):
                continue
            else:
                break

#작업 경로 질문
sPathSelect = "b"  #기본적으로 새 폴더 선택
if sWorkingPath:  #기존 작업 폴더가 있는 경우
    print(f"기존 작업 폴더: {sWorkingPath}")
    while True:
        sPathSelect = input(f"기존 폴더에 또 작업하기 [a], 새 폴더 선택하기 [b] ")
        sPathSelect.lower()
        if sPathSelect not in ("a", "b"):
            continue
        else:
            break
if sPathSelect == "b":  #작업할 폴더를 사용자에게 묻기
    print("동영상 폴더를 선택하세요.")
    root = tkinter.Tk()
    root.withdraw()
    sWorkingPath = filedialog.askdirectory(parent=root, initialdir="/", title="동영상 폴더를 선택하세요.")

if len(sWorkingPath) <= 0:
    input("작업 폴더가 선택되지 않은 것 같습니다. 프로그램을 종료합니다.")
    sys.exit()

if sWorkingPath in ("C:/", "C:/Windows", "C:/Program Files (x86)", "C:/Program Files"):
    sWorkingPath = ""
    input("C 드라이브 최상위 경로 또는 Windows 주요 폴더를 선택했습니다. 이러한 시스템 폴더에 대한 작업은 위험하므로 프로그램을 중지합니다.")
    sys.exit()

print(f"선택 작업 폴더: {sWorkingPath}\n위 폴더와 하위 폴더 전체에 대해 검색하여 출연자 정보를 파일 이름에 붙입니다.")
while True:
    sProceed = input("작업을 진행하려면 [a]를, 중지하려면 [b]를 입력하십시오: ")
    if sProceed.lower() not in ("a", "b"):
        continue
    break
if sProceed == "b":
    input("사용자가 프로그램을 중지했습니다. 감사합니다.")
    sys.exit()

# 설정 변수를 파일에 기록하기.
fileConfig = open("JAV_Star_Names_Config.txt", "w")
fileConfig.write(f"sStarPosition={sStarPosition}\n"
                 + f"sStarSeparator={sStarSeparator}\n"
                 + f"sStarPositionPrev={sStarPositionPrev}\n"
                 + f"sStarSeparatorPrev={sStarSeparatorPrev}\n"
                 + f"sWorkingPath={sWorkingPath}")
fileConfig.close()

#기존 구분자와 현재 구분자가 다른 경우, 모든 파일을 검사하여 일괄적으로 이름을 바꿈. 이때 구글 검색하지 않음.
if (sStarPositionPrev != "" and sStarSeparatorPrev != "") and (sStarPosition != sStarPositionPrev or sStarSeparator != sStarSeparatorPrev):
    print("-" * 10)
    print("기존 구분자와 현재 구분자 또는 배치 위치가 다르므로, 기존 구분자가 포함된 전체 파일에 대해 일괄적으로 이름을 바꿉니다.")
    print("이 일괄 작업을 진행하기 전에 Everything 등의 프로그램을 사용하여 혹시 기존 구분자가 잘못 들어가 있는 파일이 있는지 확인해 보기를 권장합니다.")
    input("작업을 진행하려면 엔터를 누르십시오.")

    iFileNewlyChanged = 0  # 이 프로그램이 변경하는 총 파일 수
    iRequestNo = 0
    sProdCode = ""
    sProdCodePrev = ""
    sFileBaseNameNew = ""
    iWorkFileNo = 0
    iFileReplacedNo = 0
    for (sPath, lSubFolders, lFiles) in os.walk(sWorkingPath):      #작업 폴더 및 그 하위 폴더들에서 파일 목록 가져오기
        for sFileName in lFiles:                                    #현재 폴더의 파일 목록 가져오기
            iWorkFileNo += 1                                    #현재 작업 파일 번호
            sFileBaseName, sExt = os.path.splitext(sFileName)
            if sExt[1:].lower() not in lVideoFormats:       #확장자가 비디오 또는 자막이 아닌 경우 무시
                print(f"[{str(iWorkFileNo):>2}] 건너 뛰기(비디오 또는 자막 파일이 아님): {sFileName}")
                continue
            if len(sFileBaseName) <= 4:
                print(f"[{str(iWorkFileNo):>2}] 건너 뛰기(파일 이름이 4자리 이하임): {sFileName}")
                continue
            try:                                    #파일 기본 이름에서 품번 추출하기
                sProdCode = fnExtractProdCode(sFileBaseName)
                if sFileBaseName.find(sStarSeparatorPrev) < 0:     #기존 구분자가 없는 경우
                    print(f"[{str(iWorkFileNo):>2}] 건너 뛰기(품번 있는 영상이지만 구분자 변경 일괄 작업 중에는 구글 검색 안 함): {sFileName}")
            except ErrNoCode:
                print(f"[{str(iWorkFileNo):>2}] 건너 뛰기(파일 이름에서 품번을 찾을 수 없음): {sFileName}")
                continue
            except IndexError:
                print(f"[{str(iWorkFileNo):>2}] 품번 추출 함수 인덱스 오류. 다음 파일 이름을 개발자에게 알려 주시면 프로그램을 수정하겠습니다.): {sFileName}")
                continue
            except ValueError:
                print(f"[{str(iWorkFileNo):>2}] 품번 추출 함수 값 오류. 다음 파일 이름을 개발자에게 알려 주시면 프로그램을 수정하겠습니다.): {sFileName}")
                exit()

            if sFileBaseName.find(sStarSeparatorPrev) >= 0:       #기존 구분자가 있는 파일 이름 변경
                try:
                    sFileBaseNameNew = fnChangePrevSeparator(sFileBaseName, sStarPosition, sStarSeparator, sStarPositionPrev, sStarSeparatorPrev)
                except ErrNoWork:
                    print(f"[{str(iWorkFileNo):>2}] 건너 뛰기(파일 이름에 기존 구분자가 있지만 문제가 있어 파일 이름을 바꾸지 않음): {sFileName}")
                    continue
                except IndexError:
                    print(f"[{str(iWorkFileNo):>2}] fnChangePrevSeparator 인덱스 오류. 다음 파일 이름을 개발자에게 알려 주시면 프로그램을 수정하겠습니다.): {sFileName}")
                    continue

                sFullPathPrev = os.path.join(sPath, sFileName)      #기존, 현재 구분자 기준으로 파일 이름 변경
                sFullPathNew = os.path.join(sPath, sFileBaseNameNew + sExt)
                os.rename(sFullPathPrev, sFullPathNew)
                print(f"[{str(iWorkFileNo):>2}] 성공(기존 구분자 교체): {sFileName} -> {sFileBaseNameNew + sExt}")
                iFileReplacedNo += 1
                continue

    print("-"*10)                               #작업 완료 후 메시지
    print("기본 구분자 또는 배치 형식이 변경되었습니다.")
    print(f"확인한 파일: {str(iWorkFileNo):>2}개. 기존 구분자 변경: {str(iFileReplacedNo)}개")
    input("진행하려면 엔터를 누르십시오.")

# 설정 변수를 파일에 기록하기
# 기존 구분자가 없었던 경우에도 현재 구분자 값과 동일하게 저장. 왜냐하면 이 프로그램이 한 번 실행되면 기존 구분자는 현재 구분자와 같아지기 때문.
sStarPositionPrev = sStarPosition
sStarSeparatorPrev = sStarSeparator
fileConfig = open("JAV_Star_Names_Config.txt", "w")
fileConfig.write(f"sStarPosition={sStarPosition}\n"
                 + f"sStarSeparator={sStarSeparator}\n"
                 + f"sStarPositionPrev={sStarPositionPrev}\n"
                 + f"sStarSeparatorPrev={sStarSeparatorPrev}\n"
                 + f"sWorkingPath={sWorkingPath}")
fileConfig.close()

#구글 검색을 포함한 새 출연자 추가 작업 시작. 작업 폴더 및 그 하위 폴더 전체를 다시 검색함.
print("-"*10)
print("품번을 구글 영국에 검색하여 새 출연자 추가 작업을 시작합니다.")
input("진행하려면 엔터를 누르십시오.")

iFileNewlyChanged = 0  # 이 프로그램이 변경하는 총 파일 수
iRequestNo = 0
sProdCode = ""
sProdCodePrev = ""
sFileBaseNameNew = ""
iWorkFileNo = 0

for (sPath, lSubFolders, lFiles) in os.walk(sWorkingPath):      #작업 폴더 및 그 하위 폴더들에서 파일 목록 가져오기
    for sFileName in lFiles:                                    #현재 폴더의 파일 목록 가져오기
        iWorkFileNo += 1                                    #현재 작업 파일 번호
        sFileBaseName, sExt = os.path.splitext(sFileName)
        if sExt[1:].lower() not in lVideoFormats:       #확장자가 비디오 또는 자막이 아닌 경우 무시
            print(f"[{str(iWorkFileNo):>2}] 건너 뛰기(비디오 또는 자막 파일이 아님): {sFileName}")
            continue
        if sFileBaseName.upper().find("FC2") >= 0:   #FC2 파일들은 AVDBS에 등록되지 않으므로 건너뛰기
            print(f"[{str(iWorkFileNo):>2}] 건너 뛰기(FC2 품번은 ABDBS에 등록되지 않음): {sFileName}")
            continue
        if len(sFileBaseName) <= 4:
            print(f"[{str(iWorkFileNo):>2}] 건너 뛰기(파일 이름이 4자리 이하임): {sFileName}")
            continue
        if sFileBaseName.find(sStarSeparator) >= 0:
            print(f"[{str(iWorkFileNo):>2}] 건너 뛰기(이미 출연자 있음. 구분자 '{sStarSeparator}'): {sFileName}")
            continue

        try:                                    #파일 기본 이름에서 품번 추출하기
            sProdCode = fnExtractProdCode(sFileBaseName)
        except ErrNoCode:
            print(f"[{str(iWorkFileNo):>2}] 건너 뛰기(파일 이름에서 품번을 찾을 수 없음): {sFileName}")
            continue
        except IndexError:
            print(f"[{str(iWorkFileNo):>2}] 품번 추출 함수 인덱스 오류. 다음 파일 이름을 개발자에게 알려 주시면 프로그램을 수정하겠습니다.): {sFileName}")
            continue
        except ValueError:
            print(f"[{str(iWorkFileNo):>2}] 품번 추출 함수 값 오류. 다음 파일 이름을 개발자에게 알려 주시면 프로그램을 수정하겠습니다.): {sFileName}")

        if sProdCode != sProdCodePrev:      #방금 전 단계에서 이미 검색한 품번이 아닌 경우에만 검색 진행
            if iRequestNo > 50:                                   #웹 검색을 50회 이상 실시한 경우, 프로그램 중단
                print("반복적인 웹 검색 횟수가 50회를 넘었습니다.\n"
                        + "구글이 차단을 먹일 수도 있으니 그 전에 프로그램을 중지합니다.\n"
                        + "잠시 다른 일을 하다가 나중에 다시 시도하십시오(대략 몇 시간 후).")
                print(f"확인한 파일: {str(iWorkFileNo):>2}개. 새로 출연자 추가: {str(iFileNewlyChanged)}개. 구글 검색: {str(iRequestNo)}번")
                input()
                sys.exit()
            if iRequestNo > 0:                                    #구글의 차단을 회피하기 위해 잠시 대기
                print("     나 로봇 아님(아마도?). 잠깐 노는 중...")
                time.sleep(random.uniform(2, 7))

            sHeaders = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"}
            httpContents = requests.get("https://www.google.co.uk/search?q=" + sProdCode + "%20AVDBS&gl=uk", headers=sHeaders)
            iRequestNo += 1
            sProdCodePrev = sProdCode

            soup = BeautifulSoup(httpContents.text, "html.parser")  # 구글 검색 결과를 파싱.
            iWarnTextLocation = soup.text.find("Our systems have detected unusual traffic")  # 구글에서 차단 안내문을 보냈는지 확인
            if iWarnTextLocation > 0:       #차단 안내문이 있는 경우 프로그램 중단.
                print(
                    f"[{str(iWorkFileNo):>2}] 웹 검색 오류: 'Unusual Traffic', 주의 문자열 위치: {str(iTextLocation)}, 작업 파일: {sFileName}\n"
                    + "반복적인 웹 검색으로 인해 구글이 귀하를 로봇으로 생각하는 모양입니다. 나중에 다시 시도하십시오(대략 몇 시간 후).")
                print(f"확인한 파일: {str(iWorkFileNo):>2}개. 새로 출연자 추가: {str(iFileNewlyChanged)}개. 구글 검색: {str(iRequestNo)}번")
                input()
                sys.exit()

            sWebTitle = soup.find("h3", "LC20lb MBeuO DKV0Md")  # AVDBS의 제목 줄 찾기
            if sWebTitle == None:  # AVDBS의 제목 줄 찾기 실패. 원인 불명.
                print(f"[{str(iWorkFileNo):>2}] 건너 뛰기(품번을 구글 검색 실패): {sFileName}")
                continue

            # AVDBS의 제목 줄 형태가 두 가지임. 1형) BDA-179 모치즈키 아야카, 2형) 시라토 하나 - APNS-246
            if sWebTitle.text.find(" - ") > 0:
                sWebStarName = sWebTitle.text[:sWebTitle.text.find(" - ")]
                sWebProdCode = sWebTitle.text[sWebTitle.text.find(" - ") + 3:]
            else:
                sWebStarName = sWebTitle.text[sWebTitle.text.find(' ') + 1:]
                sWebProdCode = sWebTitle.text[:sWebTitle.text.find(" ")]

            ###
            if sProdCode != sWebProdCode:       #AVDBS에서 정확히 일치하는 품번이 아니라 다른 유사 품번 검색 결과를 제출한 경우
                print(f"[{str(iWorkFileNo):>2}] 건너 뛰기(정확히 일치하는 품번 검색 실패): {sFileName}")
                continue

        #이전 품번과 현재 품번이 다른 경우 위에서 구글 검색을 했고, 같은 경우에는 재검색 없이 아래 작업 수행. 즉, 동일한 출연자 정보 재사용.
        sStarNames = sWebStarName
        sStarNames = sStarNames.replace("/", "")
        sStarNames = sStarNames.replace(".", "")
        sStarNames = sStarNames.strip()

        if len(sStarNames) == 0:     #AVDBS에 출연자가 등록되지 않았거나 기타 다른 이유로 출연자 이름이 공백으로 나오는 경우
            print(f"[{str(iWorkFileNo):>2}] 건너 뛰기(출연자 이름이 AVDBS에 등록되지 않았거나 기타 이유로 검색 실패): {sFileName}")
            continue

        #파일 이름 변경
        sFileBaseNameNew = fnAddStarName(sFileBaseName, sStarNames, sStarPosition, sStarSeparator)
        sFullPathPrev = os.path.join(sPath, sFileName)
        sFullPathNew = os.path.join(sPath, sFileBaseNameNew + sExt)
        os.rename(sFullPathPrev, sFullPathNew)
        print(f"[{str(iWorkFileNo):>2}] 성공(출연자 추가): {sFileName} -> {sFileBaseNameNew + sExt}")
        iFileNewlyChanged += 1

#작업 완료 후 메시지
print("-"*10)
print(f"확인한 파일: {str(iWorkFileNo):>2}개. 새로 출연자 추가: {str(iFileNewlyChanged)}개. 구글 검색: {str(iRequestNo)}번")
print("이 폴더에 대한 작업이 완료되었습니다. 행복하십시오! Written by SangDo_Kim in AVDBS.com")
input()