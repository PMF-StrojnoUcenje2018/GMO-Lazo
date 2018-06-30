import pandas as pd
import ujson as json

from tqdm import tqdm
from sklearn.externals import joblib

import datetime

def dataPreparation(samplesTxt, reportPath, newFeaturesPath):
    frameData = {}
    entropy = []
    frameData['entropy'] = entropy
    api = []
    frameData['api_num'] = api
    section_entropies = []
    frameData['avg_ent'] = section_entropies
    max_entropy = []
    frameData['max_entropy'] = max_entropy
    risky_section = []
    frameData['risky_section'] = risky_section
    size = []
    frameData['size'] = size
    sizeOfCode = []
    frameData['sizeOfCode'] = sizeOfCode
    stackReserve = []
    frameData['stackReserve'] = stackReserve
    sizeOfInitializedData = []
    frameData['sizeOfInitializedData'] = sizeOfInitializedData
    sizeOfUninitializedData = []
    frameData['sizeOfUninitializedData'] = sizeOfUninitializedData
    majorLinkerVersion = []
    frameData['majorLinkerVersion'] = majorLinkerVersion
    baseOfData = []
    frameData['baseOfData'] = baseOfData
    minorLinkerVersion = []
    frameData['minorLinkerVersion'] = minorLinkerVersion
    executable_sections = []
    frameData['executable_sections'] = executable_sections
    writable_sections = []
    frameData['writable_sections'] = writable_sections
    readble_sections = []
    frameData['readble_sections'] = readble_sections
    init_data = []
    frameData['init_data'] = init_data
    uninit_data = []
    frameData['uninit_data'] = uninit_data
    readble_writable = []
    frameData['readble_writable'] = readble_writable
    writable_executable = []
    frameData['writable_executable'] = writable_executable
    uninit_executable = []
    frameData['uninit_executable'] = uninit_executable
    frequencyMedian = []
    frameData['frequencyMedian'] = frequencyMedian
    frequencyExpected = []
    frameData['frequencyExpected'] = frequencyExpected
    frequencyQr = []
    frameData['frequencyQr'] = frequencyQr
    frequencyStdDev = []
    frameData['frequencyStdDev'] = frequencyStdDev
    frequencySkewness = []
    frameData['frequencySkewness'] = frequencySkewness
    frequencyQl = []
    frameData['frequencyQl'] = frequencyQl
    frequencyIRQ = []
    frameData['frequencyIRQ'] = frequencyIRQ
    localEntropiesMedian = []
    frameData['localEntropiesMedian'] = localEntropiesMedian
    localEntropiesExpected = []
    frameData['localEntropiesExpected'] = localEntropiesExpected
    localEntropiesQr = []
    frameData['localEntropiesQr'] = localEntropiesQr
    localEntropiesStdDev = []
    frameData['localEntropiesStdDev'] = localEntropiesStdDev
    localEntropiesSkewness = []
    frameData['localEntropiesSkewness'] = localEntropiesSkewness
    localEntropiesQl = []
    frameData['localEntropiesQl'] = localEntropiesQl
    localEntropiesIRQ = []
    frameData['localEntropiesIRQ'] = localEntropiesIRQ
    readble_writable_sqr = []
    frameData['readble_writable_sqr'] = readble_writable_sqr
    writable_readable_executable = []
    frameData['writable_readable_executable'] = writable_readable_executable
    startEntropy50 = []
    frameData['startEntropy50'] = startEntropy50
    startEntropy100 = []
    frameData['startEntropy100'] = startEntropy100
    startEntropy150 = []
    frameData['startEntropy150'] = startEntropy150
    charIFD = []
    frameData['charIFD'] = charIFD
    #api stuff
    apiNameK32 = [] #KERNEL32.dll 
    frameData['apiNameK32'] = apiNameK32
    adressesApiList = []
    frameData['adressesApiList'] = adressesApiList
    #api functions
    apiFunctions = ['GetCurrentProcess', 'GetProcAddress', 'LoadLibraryA', 'CloseHandle', 'WideCharToMultiByte', 'ExitProcess']
    apiFunctionsCount = {}
    for apiFunction in apiFunctions:
        apiFunctionsCount[apiFunction] = []
        frameData['apiFunctions-' + apiFunction] = apiFunctionsCount[apiFunction]
    certEntropy = []
    frameData['certEntropy'] = certEntropy
    otherSection = '___OTHER'
    sections = ['.rsrc', '.text', '.data', '.reloc', '.rdata', 'NO_NAME', 'pec1', '.imports', 'pec2', otherSection]
    sectionsCount = {}
    for section in sections:
        sectionsCount[section] = []
        frameData['section-' + section] = sectionsCount[section]

    shas = open(samplesTxt).read().splitlines()
    for sha in tqdm(shas):
        report = json.load(
            open(reportPath.format(sha[-2:], sha), 'rb')
        )
        newFeatures = json.load(
            open(newFeaturesPath.format(sha[-2:], sha), 'rb')
        )
        frequencyMedian.append(newFeatures['frequency']['median'])
        frequencyExpected.append(newFeatures['frequency']['expected'])
        frequencyQr.append(newFeatures['frequency']['qr'])
        frequencyQl.append(newFeatures['frequency']['ql'])
        frequencyIRQ.append(newFeatures['frequency']['IRQ'])
        frequencySkewness.append(newFeatures['frequency']['skewness'])
        frequencyStdDev.append(newFeatures['frequency']['stdDev'])
        localEntropiesMedian.append(newFeatures['localEntropies']['median'])
        localEntropiesExpected.append(newFeatures['localEntropies']['expected'])
        localEntropiesQr.append(newFeatures['localEntropies']['qr'])
        localEntropiesQl.append(newFeatures['localEntropies']['ql'])
        localEntropiesIRQ.append(newFeatures['localEntropies']['IRQ'])
        localEntropiesSkewness.append(newFeatures['localEntropies']['skewness'])
        localEntropiesStdDev.append(newFeatures['localEntropies']['stdDev'])
        startEntropy50.append(newFeatures['startEntropy'][50])
        startEntropy100.append(newFeatures['startEntropy'][100])
        startEntropy150.append(newFeatures['startEntropy'][150])
        entry = report['coreReport']['entries']['entry_list'][0]
        entropy.append(float(entry['info']['file']['entropy']))
        size.append(int(entry['info']['file']['size'],0))

        if 'imports' not in entry['metadata']['application']['pe']:
            api.append(0)
        else :
            if 'api_list' in entry['metadata']['application']['pe']['imports']['import_list'][-1]:
                api.append( len(entry['metadata']['application']['pe']['imports']['import_list'][-1]['api_list'] ))
            else:
                api.append(0)
                
        if 'optionalHeader' not in entry['metadata']['application']['pe']:
            sizeOfCode.append(0)
            sizeOfInitializedData.append(0)
            sizeOfUninitializedData.append(0)
            majorLinkerVersion.append(0)
            stackReserve.append(0)
            baseOfData.append(0)
            minorLinkerVersion.append(0)
        else:
            sizeOfCode.append(int(entry['metadata']['application']['pe']['optionalHeader']['sizeOfCode'],0))
            sizeOfInitializedData.append(int(entry['metadata']['application']['pe']['optionalHeader']['sizeOfInitializedData'],0))
            sizeOfUninitializedData.append(int(entry['metadata']['application']['pe']['optionalHeader']['sizeOfUninitializedData'],0))
            majorLinkerVersion.append(int(entry['metadata']['application']['pe']['optionalHeader']['majorLinkerVersion'],0))
            stackReserve.append(int(entry['metadata']['application']['pe']['optionalHeader']['sizeOfStackReserve'],0))
            baseOfData.append(int(entry['metadata']['application']['pe']['optionalHeader']['baseOfData'],0))
            minorLinkerVersion.append(int(entry['metadata']['application']['pe']['optionalHeader']['minorLinkerVersion'],0))
        if 'sections' not in entry['metadata']['application']['pe']:
            for section in sections:
                sectionsCount[section].append(0)
            executable_sections.append(0)
            writable_sections.append(0)
            readble_sections.append(0)
            init_data.append(0)
            uninit_data.append(0)
            readble_writable.append(0)
            writable_executable.append(0)
            uninit_executable.append(0)
            section_entropies.append(0)
            writable_readable_executable.append(0)
            max_entropy.append(0)
            risky_section.append(0)
            readble_writable_sqr.append(0)
        else:
            currSections = {}
            for section in sections:
                currSections[section] = 0
            for sec in entry['metadata']['application']['pe']['sections']['section_list']:
                if sec.get('name', 'NO_NAME') in sections:
                    currSections[sec.get('name', 'NO_NAME')] += 1
                else:
                    currSections[otherSection] += 1
            for section in sections:
                sectionsCount[section].append(currSections[section])
            en = [sec.get('entropy', 'NO_NAME')
                for sec in entry['metadata']['application']['pe']['sections']['section_list']]
            en = [float(i) for i in en]
            flags = [sec.get('flags')
                for sec in entry['metadata']['application']['pe']['sections']['section_list']]
            ex = 0
            w = 0
            r = 0
            init = 0
            unit = 0
            rw = 0
            we = 0
            wre = 0
            ue = 0
            for flag in flags:
                if( flag != None):
                    flag = flag['flag_list']
                    if 'IMAGE_SCN_CNT_INITIALIZED_DATA' in flag:
                        init = init+1
                    if 'IMAGE_SCN_CNT_UNINITIALIZED_DATA' in flag:
                        unit = unit +1
                    if 'IMAGE_SCN_MEM_EXECUTE' in flag:
                        ex = ex + 1
                    if 'IMAGE_SCN_MEM_READ' in flag:
                        r = r + 1
                    if ('IMAGE_SCN_MEM_WRITE' in flag) & ('IMAGE_SCN_MEM_EXECUTE' in flag):
                        we = we + 1
                    if ('IMAGE_SCN_MEM_WRITE' in flag) & ('IMAGE_SCN_MEM_READ' in flag):
                        rw = rw + 1
                    if ('IMAGE_SCN_MEM_WRITE' in flag):
                        w = w + 1
                    if ('IMAGE_SCN_MEM_EXECUTE' in flag) & ('IMAGE_SCN_CNT_UNINITIALIZED_DATA' in flag):
                        ue = ue + 1
                    if ('IMAGE_SCN_MEM_WRITE' in flag) & ('IMAGE_SCN_MEM_EXECUTE' in flag) & ('IMAGE_SCN_MEM_READ' in flag):
                        wre = wre + 1
            uninit_executable.append(ue)
            writable_readable_executable.append(wre)
            readble_writable.append(rw)
            readble_writable_sqr.append(rw**2)
            writable_executable.append(we)
            risky_section.append(sum(x > 7.0 for x in en))
            max_entropy.append(max(en))
            executable_sections.append(ex)
            init_data.append(init)
            uninit_data.append(unit)
            writable_sections.append(w)
            readble_sections.append(r)
            section_entropies.append(sum(en) / len(en))
        #characteristics list
        try:
            characteristics_list = entry['metadata']['application']['pe']['fileHeader']['characteristics']['characteristic_list']
            characteristics_list = map(str, characteristics_list)
            charIFD.append(int('IMAGE_FILE_DLL' in characteristics_list))
        except:
            pass
        #apistuffs
        currApiNameK32 = 0 #KERNEL32.dll 
        currApiNameA32 = 0 #ADVAPI32.dll
        currApiNameU32 = 0 #USER32.dll 
        currAdressesApiList = 0
        currApiFunctions = {}
        for apiFunction in apiFunctions:
            currApiFunctions[apiFunction] = 0
        if 'imports' in entry['metadata']['application']['pe']:
            if 'import_list' in entry['metadata']['application']['pe']['imports']:
                import_list = entry['metadata']['application']['pe']['imports']['import_list']
                for imp in import_list:
                    if str(imp['name']) == 'KERNEL32.dll':
                        currApiNameK32 += 1
                    if str(imp['name']) == 'ADVAPI32.dll':
                        currApiNameA32 += 1
                    if str(imp['name']) == 'USER32.dll':
                        currApiNameU32 += 1
                    if 'api_list' in imp:
                        for apis in imp['api_list']:
                            if str(apis).startswith('0x'):
                                currAdressesApiList += 1
                            if str(apis) in apiFunctions:
                                currApiFunctions[str(apis)] += 1
        for apiFunction in apiFunctions:
            apiFunctionsCount[apiFunction].append(currApiFunctions[apiFunction])
        apiNameK32.append(currApiNameK32)
        adressesApiList.append(currAdressesApiList)
        # certificates
        cEnt = 0
        if 'tags' in entry:
            if 'tag_list' in entry['tags']:
                for tag in entry['tags']['tag_list']:
                    cEnt += (int(str(tag) == 'entropy'))
        certEntropy.append(cEnt)
    for key, val in frameData.items():
        if len(val) != 6928:
            print(key)
    return frameData, shas

if __name__ == '__main__':
    samplesTxt = 'datasets/test/test.shas'
    clf = joblib.load('model_ada.pkl')
    features, shas = dataPreparation(samplesTxt, "datasets/test/reports/{}/{}.json",  "datasets/test/new-features/{}/{}.json")
    pred = clf.predict(pd.DataFrame(data=features))
    resultFile = open('output' + str(datetime.datetime.now()) + '.tsv', 'w')
    for sha, result in zip(shas, pred):
        #resultFile.write(sha + '\t' + str(result) + '\n')
        resultFile.write(str(result) + '\n')
    resultFile.close()
