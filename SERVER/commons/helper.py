def tuple2dict(tpl, nameCol):
    newDict = {}
    for i in range(len(tpl)):
        newDict[nameCol[i]] = tpl[i]
    return newDict

def listDict(lst, nameCol):
    allUser = []
    for x in lst:
        allUser.append(tuple2dict(x, nameCol))
    return allUser


