def fnAddStarName(sFileBaseName, sStarNames, sStarPosition = "b", sStarSeparator = "#"):
    sFileBaseNameNew = ""
    if sStarPosition == "b":        #출연자 이름을 뒤에 붙여야 할 경우
        if sStarSeparator == "출)":
            sFileBaseNameNew = sFileBaseName + " 출) " + sStarNames
        else:
            sFileBaseNameNew = sFileBaseName + " " + sStarSeparator + sStarNames
    else:
        if sStarSeparator == "출)":
            sFileBaseNameNew = sStarNames + " 출) " + sFileBaseName
        else:
            sFileBaseNameNew = sStarNames + sStarSeparator + " " + sFileBaseName

    return sFileBaseNameNew

#테스트 실행
#print(f"[HD]MPA-334 유모|{fnAddStarName("[HD]MPA-334 유모", "미아쟈키 하야오", "a","@")}")
