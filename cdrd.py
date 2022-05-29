def countOne(mDic):
    cDic = {}
    # key 리스트 만들기
    keyList = list(mDic.keys())

    # for문으로 하나씩 1의 개수 세서 cDic에 넣기
    for k in keyList:
        c = k.count("1")
        # key값 존재 확인
        if c in cDic:
            # cList는 1의 개수를 key로 갖는 value(리스트), get으로 해당 key의 value가져옴
            cList = cDic.get(c)
            # 중복확인
            if k not in cList:
                cList.append(k)
                cDic[c] = cList
        else:
            cDic[c] = [k]

    return cDic


def solution(minterm):
    answer = []

    mDic = {}
    cDic = {}
    notComb = {}
    checkDic = {}

    digit = minterm[0]
    n = minterm[1]
    dt = minterm[2]
    dtList = []
    if dt != 0:
        dtList = minterm[-dt:]

    for i in range(3, n + 3):
        m = [minterm[i]]

        b = bin(minterm[i])[2:]
        if (len(b) < digit):
            b = "0" * (digit - len(b)) + b
        mDic[b] = [m, "false"]
    # cDic호출
    cDic = countOne(mDic)

    # merge할거 없으면 중복 멈춰야함
    while (len(cDic) > 0 ):
        mergeDic = {}

        ckeyList = sorted(cDic.keys())

        for i in range(len(ckeyList) - 1):
            if ckeyList[i + 1] - ckeyList[i] == 1:
                for a in cDic[ckeyList[i]]:
                    for b in cDic[ckeyList[i + 1]]:
                        merge = ''
                        diff = 0
                        for d in range(0, digit):
                            if a[d] == b[d]:
                                merge += a[d]
                            else:
                                merge += "2"
                                diff += 1
                        if diff == 1:
                            mDic[a][1] = "true"
                            mDic[b][1] = "true"
                            # 합병한 거 넣기, 중복확인 필요
                            if merge not in mergeDic:
                                mValue = mDic[a][0] + mDic[b][0]
                                mergeDic[merge] = [mValue, "false"]

        # false인거 notComb에 쌍으로 넣기
        mkeyList = list(mDic.keys())

        for i in mkeyList:
            if mDic[i][1] == "false":
                notComb[i] = mDic[i][0]

        mDic = mergeDic
        cDic = countOne(mDic)

    # notComb 정렬 후 2를 "-"로 바꾸기

    answer = sorted(notComb.keys())
    for i in range(len(answer)):
        for j in range(len(notComb[answer[i]])):
            if notComb[answer[i]][j] in checkDic:
                checkDic[notComb[answer[i]][j]][0] += 1
                checkDic[notComb[answer[i]][j]].append(answer[i].replace("2", "-"))
            else:
                checkDic[notComb[answer[i]][j]] = [1, answer[i].replace("2", "-")]
        answer[i] = answer[i].replace("2", "-")

    #print("checkDic",checkDic)


    #epi 찾기
    epiList = ["EPI"]
    secondEpi = []
    result = ["RESULT"]

    first = True

    # 여기서부터 반복
    while(True):
        checkList = list(checkDic.keys())
        for i in checkList:
            if checkDic[i][0] == 1:

                if (first) and (checkDic[i][1] not in epiList):
                    epiList.append(checkDic[i][1])
                elif (first == False) and (checkDic[i][1] not in secondEpi):
                    secondEpi.append(checkDic[i][1])

        nepiMList = []
        for i in checkList:
            if (i not in dtList) and (set(epiList).isdisjoint(set(checkDic[i]))) and (set(secondEpi).isdisjoint(set(checkDic[i]))):
                nepiMList.append(i)
            else:
                checkDic.pop(i)

        #nepi남아있는지 확인
        if len(checkDic)==0:
            result = result + epiList[1:] + secondEpi
            answer = answer+epiList +result

            return answer
        else:
            first = False

            #CD
            delList = []
            for i in nepiMList:
                for j in nepiMList:
                    if i!=j and set(checkDic[i][1:]).issuperset(set(checkDic[j][1:])):
                        if i not in delList:
                            delList.append(i)
            for i in delList:
                del checkDic[i]
            nepiMList = [x for x in nepiMList if x not in delList]

            #RD
            nepiDic = {}
            delList = []
            for i in nepiMList:
                for e in checkDic[i][1:]:
                    if e not in nepiDic:
                        nepiDic[e] = [i]
                    else:
                        eList = nepiDic.get(e)
                        if i not in eList:
                            eList.append(i)
                            nepiDic[e] = eList

            notdel = []
            nepiKeyList = list(nepiDic.keys())
            for i in nepiKeyList:
                for j in nepiKeyList:
                    if i!=j and set(nepiDic[i]).issubset(set(nepiDic[j])):
                        if nepiDic[i] != nepiDic[j]:
                            delList.append(i)
                        else:
                            if i not in notdel:
                                delList.append(i)
                            notdel.append(j)

            for i in delList:
                del nepiDic[i]
                for j in nepiMList:
                    if i in checkDic[j][1:]:
                        checkDic[j][0] -=1
                        checkDic[j].remove(i)


# 입력형식: [변수의 개수, minterm의 개수, don't care의 개수, minterm #1, minterm #2, ..., don't care #1, ...]
print(solution([4, 8, 2, 0, 4, 8, 10, 12, 11, 13, 15]))
print(solution([4, 11, 0, 0, 2, 5, 6, 7, 8, 10, 12, 13, 14, 15]))
print(solution([4, 9, 3, 2, 3, 7, 9, 11, 13, 1, 10, 15]))
