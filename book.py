import json
import re
import sys
import fitz


def getBookName_and_author_name(file_name):
    with open(book, 'rb') as f:
        pdf = PdfFileReader(f)
        info = pdf.getDocumentInfo()
        
    title = info.title
    print("Title : ",title)
    author = info.author
    print("Author : ",author)
    return ""



def getBookLanguage(text):
    total = 0
    hindi = 0
    english = 0

    for i in text:
        if ord(i) in range(ord('\u0900'), ord('\u097F') + 1):
            hindi += 1
        else:
            english += 1
        total += 1

    print(hindi / total)
    print(english)
    print(total)
    if ((hindi / total) * 100) > 25:
        return "Hindi"
    return "English"


def isScanned(file_name):
    page_num = 0
    text_perc = 0.0

    doc = fitz.open(file_name)

    for page in doc:
        page_num = page_num + 1

        page_area = abs(page.rect)
        text_area = 0.0
        for b in page.getTextBlocks():
            r = fitz.Rect(b[:4])  # rectangle where block text appears
            text_area = text_area + abs(r)
        text_perc = text_perc + (text_area / page_area)

    text_perc = text_perc / page_num
    # If the percentage of text is very low, the document is most likely a scanned PDF
    if text_perc < 0.09:
        return True
    return False


def getQuestionStart(file_name):
    pass


def isAnswerKeySeparate(s):
    start_index_q1=s.find('1.')
    end_index_q1=s.find('(d)',start_index_q1)
    start_index_q2=s.find('2.',end_index_q1)

    #------------------finding Substring----------------------#
    st2 = s[end_index_q1:start_index_q2]

    #-------------------searcing Pattern----------------------#
    m = re.search(r"([a-d])", st2)

    if m is not None:
         return True
    else:
        return False


def getTopics(file_name):
    f = open('C:/Users/DELL/Downloads/' + file_name + '.txt', "r", encoding='utf-8')
    data = f.read()
    text = data.split('\n')
    temp = []
    list = ['Contents', 'Content', 'CONTENT', 'Index', 'index', 'Table of Contents']

    for i in list:
        if i in text:
            st = text.index(i) + 2
            g = text[st:]
            break

    c = 0
    try:
        for i in g:
            if i.startswith('\x0c'):
                break
            for j in range(len(temp)):
                if (i != '' and i != ' ') and re.search(i, temp[j]):
                    if re.match(r'\d', i):
                        continue
                    else:
                        # print(i)
                        c = 1
                        break
            if (c == 0):
                temp.append(i)
            else:
                break
    except:
        print('Questions regarding ', filename)
    t = ('\n').join(temp)
    return t


def isExamYearMentioned(s):
    start_index=s.find('1.')
    end_index=s.find('2.')
    mylist = [s[start_index:end_index]] 
    match = re.match(r'.*([1-3][0-9]{3})',mylist )
    if match is not None:
        return True
    else:
        return False
 


def getContentType():
    pass


def areQuestionsImageBased():
    pass


if __name__ == "__main__":
    pdf_file = sys.argv[1]

    result = {}

    result['Book'] = getBookName_and_author_name(file)

    result['Language'] = getBookLanguage(text)

    result['Scanned'] = isScanned(pdf_file)

    result['Topics'] = getTopics(file_name)
    result['Exam year mentioned'] = isExamYearMentioned(text)
    result['Ans with ques']= isAnswerKeySeparate(text)
