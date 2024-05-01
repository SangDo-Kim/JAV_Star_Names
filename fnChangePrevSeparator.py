#이 함수는 기존 구분자에 따라 기존 출연자 이름을 추출하여 파일 이름 변경하여 반환. 오류 시 ErrNoWork 오류 반환.
class ErrNoWork(Exception):
    pass
def fnChangePrevSeparator(sFileBaseName, sStarPosition = "b", sStarSeparator = "#", sStarPositionPrev = "b", sStarSeparatorPrev = "출)"):
    if len(sFileBaseName) <= 4:
        raise ErrNoWork
    sFileBaseNameNew = ""
    sOtherNames = ""
    s = ""

    if sStarSeparatorPrev == "출)" and sFileBaseName.find(", 출)") >= 0:  #기존 구분자가 출)일 경우, '출)'도 있고, ', 출)'도 있음.
        sStarSeparatorPrev = ", 출)"

    if sFileBaseName.find(sStarSeparatorPrev) == -1:    #기존 구분자를 파일 이름에서 찾지 못한 경우
        raise ErrNoWork

    if sStarPositionPrev == "b":    #기존 출연자 이름이 뒤에 붙은 경우
        iSepPosition = sFileBaseName.find(sStarSeparatorPrev)
        sOtherNames = sFileBaseName[:iSepPosition].strip()
        sStarNames = sFileBaseName[iSepPosition+len(sStarSeparatorPrev):].strip()
    else:                           #기존 출연자 이름이 앞에 붙은 경우
        iSepPosition = sFileBaseName.find(sStarSeparatorPrev)
        sStarNames = sFileBaseName[:iSepPosition].strip()
        sOtherNames = sFileBaseName[iSepPosition+len(sStarSeparatorPrev):].strip()

    if len(sOtherNames) <= 4 or len(sStarNames) < 1:     #분리된 파일 이름과 출연자 이름의 길이가 너무 짧으면 오류로 판단
        raise ErrNoWork

    if sStarPosition == "b":        #출연자 이름을 뒤에 붙여야 할 경우
        if sStarSeparator == "출)":
            sFileBaseNameNew = sOtherNames + " 출) " + sStarNames
        else:
            sFileBaseNameNew = sOtherNames + " " + sStarSeparator + sStarNames
    else:
        if sStarSeparator == "출)":
            sFileBaseNameNew = sStarNames + " 출) " + sOtherNames
        else:
            sFileBaseNameNew = sStarNames + sStarSeparator + " " + sOtherNames

    return sFileBaseNameNew

#테스트 실행
#for i in range(len(lSampleFileNames)):
#    print(lSampleFileNames[i], "\t|\t", fChangePrevSeparator(lSampleFileNames[i]))
