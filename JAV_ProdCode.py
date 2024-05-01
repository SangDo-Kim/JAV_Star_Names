#JAV_ProdCode_V1.14
#문자열(파일 기본 이름, 확장자 제외)을 받아서 JAV 품명 코드를 추출해서 반환. 오류 시 ErrNoCode 오류 발생
class ErrNoCode(Exception):
    pass

def fnExtractProdCode(sFileBaseName):
    lNonCode = ["'", "!", "#", "$", "%", "&", "(", ")", "*", ",", ".", "@", "[", "[", "^", "_", "`", "{", "}", "+", "=", "출)"]
    sFileBaseName = sFileBaseName.upper()
    for sNonCode in lNonCode:       #품번에 포함될 수 없는 문자열들을 다른 문자로 교체
        sFileBaseName = sFileBaseName.replace(sNonCode, " X ")

    for i in range(len(sFileBaseName)):   #영문자, 숫자, 대시를 제외한 일어, 한국어는 모두 공백으로 교체
        if sFileBaseName[i].encode().isalpha() or sFileBaseName[i].isdecimal() or sFileBaseName[i] == "-":
            continue
        else:
            sFileBaseName = sFileBaseName.replace(sFileBaseName[i], " ")
    sProdCode = ""

    #특수 품번 처리(FC2, 550ENE-154, T28-111 등에 대해 코드 앞 부분의 숫자를 영문자로 대체하여, 나중에 split()으로 분리되지 않도록 함.
    lSpecialCodes = [["550ENE", "FiveFiveZeoENE"], ["T28", "TTwoEight"], ["S2MBD", "STwoMBD"], ["S2M", "STwoM"],
                     ["FC2-PPV", "FCTwoDashPPV"], ["FC2PPV", "FCTwoDashPPV"], ["FC2 PPV", "FCTwoDashPPV"],
                     ["1P", "OneP"]]
    for i in range(len(lSpecialCodes)):
        sFileBaseName = sFileBaseName.replace(lSpecialCodes[i][0], lSpecialCodes[i][1])

    # 문자열을 숫자(d), 영문자(a), 대시(-)별로 구분. 중간에 공백 삽입 후 split())
    sCharTypePrev = ""      #이전 문자 유형
    sCharTypeCurr = ""      #현재 문자 유형
    sProdCodePrefix = ""
    sProdCodeSuffix = ""
    sFileBaseNameMod = ""
    for i in range(len(sFileBaseName)):
        if sFileBaseName[i].isalpha():    #현재 문자 유형 검사
            sCharTypeCurr = "d"
        elif sFileBaseName[i].isdecimal():
            sCharTypeCurr = "a"
        elif sFileBaseName[i] == "-":
            sCharTypeCurr = "-"
        else:
            sCharTypeCurr = ""
        if sCharTypePrev != sCharTypeCurr:
            sFileBaseNameMod += " "
            sCharTypePrev = sCharTypeCurr
        sFileBaseNameMod += sFileBaseName[i]

    sFileBaseNameMod = "& " + sFileBaseNameMod + " & & & &"         #인덱스 오류를 방지하기 위해 앞뒤에 더미 문자 삽입.
    lStringSplit = sFileBaseNameMod.split()

    # 1P 품번 처리(예: 1P-072023-001)
    if "OneP" in lStringSplit:
        sProdCodePrefix = "OneP"
        iOnePPosion = lStringSplit.index("OneP")
        while True:
            if lStringSplit[iOnePPosion+1] == "-" and lStringSplit[iOnePPosion+2].isdecimal():  #1P-072023 형태인 경우
                iOnePPosion += 1
            if lStringSplit[iOnePPosion+1].isdecimal():
                sProdCodeSuffix = lStringSplit[iOnePPosion+1]
            else:
                sProdCodePrefix = ""
                sProdCodeSuffix = ""
                break
            iOnePPosion += 1
            if lStringSplit[iOnePPosion+1] == "-" and lStringSplit[iOnePPosion+2].isdecimal():  #1P-072023-001 형태인 경우
                sProdCodeSuffix += "-"
                iOnePPosion += 1
            elif lStringSplit[iOnePPosion+1].isdecimal():
                sProdCodeSuffix += "-"
            if lStringSplit[iOnePPosion+1].isdecimal():
                sProdCodeSuffix += lStringSplit[iOnePPosion+1]
            else:
                sProdCodePrefix = ""
                sProdCodeSuffix = ""
                break
            break
        if len(sProdCodeSuffix) < 10:   #1P-072023-001에서 1P- 이후 뒷자리가 10자리 미만이면 품번으로 인정 안 함.
            sProdCodeSuffix = ""        #나중에 sProdCode 길이 제한으로 오류 발생될 예정

    #일반 품번 추출(예: JUL-333)
    if not sProdCodePrefix:  # 위 단계에서 품번을 추출하지 못한 경우에만 실행.
        iDashSearchPoint  = 0
        for iDashNo in range(lStringSplit.count("-")):
            iDashPosition = lStringSplit.index("-", iDashSearchPoint)
            if lStringSplit[iDashPosition-1].isalpha() and lStringSplit[iDashPosition+1].isdecimal():
                # 품번 불인정 대상: 1글자보다 작은 영문자, 1자리 숫자, 합쳐서 4글자 이하
                if len(lStringSplit[iDashPosition-1]) <= 1 or \
                   len(lStringSplit[iDashPosition+1]) <= 1 or \
                   (len(lStringSplit[iDashPosition-1]) + len(lStringSplit[iDashPosition+1]) <= 4):
                    if iDashNo < lStringSplit.count("-") - 1:
                        iDashSearchPoint = lStringSplit.index("-", iDashPosition + 1)
                        continue
                    break
                sProdCodePrefix = lStringSplit[iDashPosition-1]
                sProdCodeSuffix = lStringSplit[iDashPosition+1]
            else:
                if iDashNo < lStringSplit.count("-") - 1:
                    iDashSearchPoint = lStringSplit.index("-", iDashPosition + 1)
                    continue
                else:
                    break

    #대시가 없는 파일 이름에서 임의로 대시를 붙여 품번 생성
    if not sProdCodePrefix: #위 단계에서 품번을 추출하지 못한 경우에만 실행.
        for i in range(len(lStringSplit)):
            if lStringSplit[i].isdecimal() and len(lStringSplit[i]) >= 2:       #2자리 이상의 숫자를 찾음.
                if lStringSplit[i-1].isalpha() and 2 <= len(lStringSplit[i-1]) <= 6: #그 앞 문자열이 2~7글자 이상인 경우
                    if 5 <= len(lStringSplit[i-1]) + len(lStringSplit[i]) <= 6:      #합쳐서 5~6글자 품번만 임의 대시 부착 품번 인정
                        sProdCodePrefix = lStringSplit[i - 1]
                        sProdCodeSuffix = lStringSplit[i]
                    else:
                        continue


    #최종 품번을 만들기 및 글자 수 등 점검
    if sProdCodePrefix != "" and sProdCodeSuffix != "":
        sProdCode = sProdCodePrefix + "-" + sProdCodeSuffix

    for i in range(len(lSpecialCodes)):             #특수 코드(예:550ENE) 복원
        sProdCode = sProdCode.replace(lSpecialCodes[i][1], lSpecialCodes[i][0])

    if sProdCode.find("FC2-PPV") >= 0 and len(sProdCodeSuffix) < 7:    # FC2-PPV는 뒤의 숫자가 7자리임.
        raise ErrNoCode

    if 6 <= len(sProdCode) <= 16:
        return sProdCode
    else:
        raise ErrNoCode

#비디오 형식. 모두 소문자로 써야 함.
lVideoFormats = ["3g2", "3gp", "3gp2", "3gpp", "amr", "amv", "asf", "avi", "bdmv", "d2v", "divx", "drc", "dsa", "dsm", "dss", "dsv", "evo", "f4v", "flc", "fli", "flic", "flv", "hdmov", "ifo", "ivf", "m1v", "m2p", "m2t", "m2ts", "m2v", "m4v", "mkv", "mp2v", "mp4", "mp4v", "mpe", "mpeg", "mpg", "mpls", "mpv2", "mpv4", "mov", "mts", "ogm", "ogv", "pss", "pva", "qt", "ram", "ratdvd", "rm", "rmm", "rmvb", "roq", "rpm", "smil", "smk", "swf", "tp", "tpr", "ts", "vob", "vp6", "webm", "wm", "wmp", "wmv", "ts", "mts", "srt", "smi", "vtt"]

#테스트 실행
#JUL-322, 550ENE-323, FC2-PPV-3806605, 1P-072023-001, Tokyo-Hot-n0588
#오류 주의: 071312-073, EUN#-232, EUN영상JUL-333-한국어Uncensored,
if __name__ == "__main__":
    sFileBaseName = ("Tokyo-Hot-n0588")
    try:
        print(f"파일 이름: {sFileBaseName}, 품번: {fnExtractProdCode(sFileBaseName)}")
    except ErrNoCode:
        print(f"파일 이름: {sFileBaseName}, 품번 추출 실패")
    except ValueError:
        print(f"파일 이름: {sFileBaseName}, ValueError")

