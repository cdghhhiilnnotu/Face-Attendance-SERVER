import json

fileJSON = 'api.json'

# Opening JSON file
def openJSON():
    data = {}
    with open(fileJSON, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def get_link_img():
    data = openJSON()
    listMSV = []
    for s in data['sinhvien']:
        listMSV.append(s)
    return listMSV

def data_by_key(keyDict):
    data = openJSON()
    return data[keyDict]

def get_msv_by_class(classID):
    dsmsv = []
    for item in data_by_key('dslop'):
        if item['MaLop'] == classID:
            dsmsv.append(item['MaSV'])
    return dsmsv

def get_sv_by_msv(msv):
    data = openJSON()
    for s in data['sinhvien']:
        if s['MSV'] == msv:
            return s

if __name__ == "__main__":
    student_msv = get_msv_by_class('TH5216_20CN3')
    # for msv in student_msv:

    # download_dataset(student_links)

