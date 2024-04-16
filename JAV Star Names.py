import tkinter
from tkinter import filedialog
import os
import sys
import time
import random
from bs4 import BeautifulSoup
import requests

print('\033[92m' +"JAV Star name finder, V1.0, written by SangDo_Kim, a user in AVDBS.com."+"\033[0m")
sIsRun = input("Info: This program does not crawl AVDBS, but it reads Google UK's saved pages.\n"
                "Warning: I recommend running it in a small folder with 10 or more files first.\n" +
                "Running it in a big folder with hundreds of files without a test is not recommended.\n" +
                "Press 'a' and Enter to proceed, or press just Enter to abort:\n" +
                "정보: 이 프로그램은 AVDBS를 크롤링하지 않습니다. Google UK의 저장된 페이지를 읽습니다.\n"
                "경고: 10여 개의 파일이 있는 작은 폴더에 대해 먼저 실행해 볼 것을 권장합니다.\n" +
                "이 프로그램을 테스트해 보지 않고 수백 개 파일이 있는 폴더에 실행하는 것은 권장하지 않습니다.\n" +
                "진행하려면 'a'와 엔터를 누르고, 중단하려면 그냥 엔터를 누르십시오: ")
sIsRun = sIsRun.lower()
if sIsRun != 'a':
    sys.exit("The program is aborted. 프로그램을 중단합니다.")

root = tkinter.Tk()                         #작업할 폴더를 사용자에게 묻기
root.withdraw()
sFolderPath = filedialog.askdirectory(parent=root, initialdir="/", title="Select the AV folder. 동영상 폴더를 선택하세요.")
os.chdir(sFolderPath)
lFileList = [x for x in os.listdir() if os.path.isfile(x)]  #지정된 폴더 내 파일만 목록으로 저장하고 하위 폴더는 제외

iChangedFiles = 0                           #이 프로그램이 변경하는 총 파일 수

print("--------------------")
print("Analyzing and connecting Google UK...")

sHeaders = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"}
iRequest = 0
sPreviousCodeNum = ""
for i in range(len(lFileList)):
    sCodeNum = lFileList[i].replace(".", " ")       #파일 이름에서 마침표 제거
    sCodeNum = sCodeNum.replace(",", " ")           #파일 이름에서 쉼표 제거
    if sCodeNum.find("출)") != -1:                              #이미 출연자를 기록한 파일은 건너뛰기
        print("["+str(i+1)+"/"+str(len(lFileList))+"] Skip: Already has a star name: " + lFileList[i])
        continue
    if sCodeNum[0:3].lower() == "fc2":                        #FC2 파일들은 AVDBS에 등록되지 않으므로 건너뛰기
        print("["+str(i+1)+"/"+str(len(lFileList))+"] Skip: FC2 files cannot be processed." + lFileList[i])
        continue
    sCodeNum = sCodeNum[:sCodeNum.find(" ")]  # 파일 이름에서 첫 번째 공백까지를 품번으로 간주
    if sCodeNum.find("-") == -1:                              #파일 이름에 '-'가 없으면 품번이 아닌 것으로 간주
        print("["+str(i+1)+"/"+str(len(lFileList))+"] Skip: Invalid AV name: " + lFileList[i])
        continue
    if sCodeNum != sPreviousCodeNum:                        #방금 전 단계에서 이미 검색한 품번이 아닌 경우에만 검색 진행
        if iRequest > 50:                                   #웹 검색을 50회 이상 실시한 경우, 프로그램 중단
            input("Repeated web search has been done over 50 times.\n" +
                  "Google may block the program, so it stops before that.\n"+
                  "Please do something else and try it later (maybe in a few hours).\n"+
                  "반복적인 웹 검색 횟수가 50회를 넘었습니다.\n"+
                  "구글이 차단을 먹일 수도 있으니 그 전에 프로그램을 중지합니다.\n"+
                  "잠시 다른 일을 하다가 나중에 다시 시도하십시오(대략 몇 시간 후)."
                  )
            sys.exit()
        if iRequest > 0:                                    #구글의 차단을 회피하기 위해 잠시 대기
            print("\033[93m     I no robot (I guess?) I'm idling for a while... 나는 로봇 아님(아마도?). 잠깐 노는 중...\033[0m")
            time.sleep(random.uniform(2, 7))
        r = requests.get("https://www.google.co.uk/search?q=" + sCodeNum + "%20avdbs&gl=uk", headers=sHeaders)
        iRequest += 1
        sPreviousCodeNum = sCodeNum

    soup = BeautifulSoup(r.text, "html.parser")     #구글 검색 결과를 파싱. 방금 전 단계에서 이미 검색한 경우, 기존 검색 내용을 재사용
    iTextLocation = soup.text.find("Our systems have detected unusual traffic")     #구글에서 차단 안내문을 보냈는지 확인
    if iTextLocation > 0:
        sys.exit("["+str(i+1)+"/"+str(len(lFileList))+"] 'Unusual Traffic' Text Location: "+str(iTextLocation)+".\n"
                 "Due to repeated web search, it seems Google think you are a robot.\n"+
                 "Please try it later (maybe in a few hours).\n" +
                 "반복적인 웹 검색으로 인해 구글이 귀하를 로봇으로 생각하는 모양입니다.\n"+
                 "나중에 다시 시도하십시오(대략 몇 시간 후).")

    #items = soup.find("div", "BNeawe vvjwJb AP7Wnd")
    items = soup.find("h3", "LC20lb MBeuO DKV0Md")      #AVDBS의 제목 줄 찾기
    if items == None:                                               #AVDBS의 제목 줄 찾기 실패. 성인 인증 문제일지, 다른 문제일지 불명확
        print("["+str(i+1)+"/"+str(len(lFileList))+"] Skip: Cannot find the AV number: ", lFileList[i])
        continue

    # AVDBS의 제목 줄 형태가 두 가지임. 1형) BDA-179 모치즈키 아야카, 2형) 시라토 하나 - APNS-246
    if items.text.find(" - ") > 0:
        sExtractedStarName = items.text[:items.text.find(" - ")]
        sExtractedCodeNum = items.text[items.text.find(" - ")+3:]
    else:
        sExtractedStarName = items.text[items.text.find(' ')+1:]
        sExtractedCodeNum = items.text[:items.text.find(" ")]
    if sCodeNum != sExtractedCodeNum:       #AVDBS에서 정확히 일치하는 품번이 아니라 다른 유사 품번 검색 결과를 제출한 경우
        print("["+str(i+1)+"/"+str(len(lFileList))+"] Skip: Cannot find the exact AV number: ", lFileList[i])
        continue
    sStarName = sExtractedStarName
    sStarName = sStarName.replace("/", "")
    sStarName = sStarName.replace(".", "")
    sStarName = sStarName.strip()

    if len(sStarName) == 0:                                 #AVDBS에 출연자가 등록되지 않았거나 기타 다른 이유로 출연자 이름이 공백으로 나오는 경우
        print("["+str(i+1)+"/"+str(len(lFileList))+"] Skip: Cannot extract AV star name: ", lFileList[i])
        continue
    name, ext = os.path.splitext(lFileList[i])              #파일 이름 변경 시작
    if name.find(" ") == -1:                                #파일 이름에 품명만 있고 다른 내용이 붙지 않은 경우
        name += " 출) " + sStarName
    else:
        name += ", 출) " + sStarName
    name.replace("/","")                        #파일 이름 오류 방지를 위해 '/' 문자 제거
    sNewFileName = name + ext
    sOldFileName = lFileList[i]
    os.rename(sFolderPath + "/" + sOldFileName, sFolderPath + "/" + sNewFileName)
    print("["+str(i+1)+"/"+str(len(lFileList))+"] Success: " + sOldFileName, " -> ", sNewFileName)
    iChangedFiles += 1

print("--------------------")                               #작업 완료 후 메시지
print("File name changed:", iChangedFiles, 'out of',len(lFileList), 'files.')
print("변경된 파일:", iChangedFiles, '개. 전체 파일:',len(lFileList), '개.')
input("The work in the folder is completed. Be happy!\n" +
      "Contact(in-web message): User ID SangDo_Kim in AVDBS.com.\n" +
      "이 폴더에 대한 작업이 완료되었습니다. 행복하십시오!\n"+
      "연락(웹 사이트 내 쪽지): 사용자 ID SangDo_Kim, AVDBS.com.")