import datetime
import os
import re

import cv2
import numpy as np
import pytesseract


rus_to_lat = {
    'А': 'A',
    'Б': 'B',
    'В': 'V',
    'Г': 'G',
    'Д': 'D',
    'Е': 'E',
    'Ё': 'E',
    'Ж': 'ZH',
    'З': 'Z',
    'И': 'I',
    'Й': 'Y',
    'К': 'K',
    'Л': 'L',
    'М': 'M',
    'Н': 'N',
    'О': 'O',
    'П': 'P',
    'Р': 'R',
    'С': 'S',
    'Т': 'T',
    'У': 'U',
    'Ф': 'F',
    'Х': 'H',
    'Ц': 'TS',
    'Ч': 'CH',
    'Ш': 'SH',
    'Щ': 'SHCH',
    'Ъ': '',
    'Ы': 'Y',
    'Ь': '',
    'Э': 'E',
    'Ю': 'YU',
    'Я': 'IA',
    '.': '.',
    '-': '-'
}

lat_to_rus = {value: key for key, value in rus_to_lat.items()}


def transliterate_to_lat(text):
    return ''.join(rus_to_lat.get(char, char) for char in text)


def preprocess_image(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    median_blur = cv2.medianBlur(gray_image, 3)

    kernel = np.ones((2, 2), np.uint8)
    opening = cv2.morphologyEx(median_blur, cv2.MORPH_OPEN, kernel, iterations=1)

    _, otsu_thresh = cv2.threshold(opening, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return otsu_thresh


def extract_and_replace_dates(text_list):
    date_pattern = re.compile(r'\d{2}\.\d{2}\.\d{4}')
    new_text_list = []

    for text in text_list:
        dates = date_pattern.findall(text)
        if dates:
            new_text_list.extend(dates)
        else:
            new_text_list.append(text)

    return new_text_list


def clean_list_elements(text_list):
    cleaned_list = []
    for text in text_list:
        if re.fullmatch(r'\d{2}\.\d{2}\.\d{4}', text):
            cleaned_list.append(text)
        else:
            cleaned_text = re.sub(r'[^\w\s.]|(?<!\.\s)(?<!\w)\.', '', text)
            cleaned_list.append(cleaned_text.strip())
    return cleaned_list


def remove_leading_spaces(text_list):
    cleaned_list = [text.strip() for text in text_list]
    return cleaned_list


def transliterate(text, layout, ftype):
    text_ = text.copy()
    if ftype == 'vu1':
        for layout_ in layout[ftype]:
            target_1, target_2 = layout_
            text_[target_2] = transliterate_to_lat(text[target_1])
    return text_


def combine_elements(combiner_layout, text_list, layout_key):
    rules = combiner_layout.get(layout_key, [])

    combined_result = text_list.copy()

    processed_indices = set()

    for indexes, separator in rules:
        filtered_indexes = [i for i in indexes if i not in processed_indices and i < len(combined_result)]

        if not filtered_indexes:
            continue

        combined_text = separator.join(combined_result[i] for i in filtered_indexes)
        combined_result[filtered_indexes[0]] = combined_text

        for index in filtered_indexes[1:]:
            processed_indices.add(index)
    for index in sorted(processed_indices, reverse=True):
        del combined_result[index]

    return combined_result


def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")
    
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    
    return rect

def warp_perspective(image):
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    edged = cv2.Canny(blurred, 75, 200)
    
    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    doc_cnt = None
    
    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        
        if len(approx) == 4:
            doc_cnt = approx
            break
    
    if doc_cnt is None:
        return image
    
    rect = order_points(doc_cnt.reshape(4, 2))
    dst = np.array([
        [0, 0],
        [image.shape[1] - 1, 0],
        [image.shape[1] - 1, image.shape[0] - 1],
        [0, image.shape[0] - 1]], dtype="float32")
    
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (image.shape[1], image.shape[0]))
    
    return warped


def remove_grid(binary, horizontal_lines_positions, vertical_lines_positions, line_thickness=3):
    h, w = binary.shape

    for y in horizontal_lines_positions:
        cv2.line(binary, (0, y), (w, y), (255, 255, 255), line_thickness)

    for x in vertical_lines_positions:
        cv2.line(binary, (x, 0), (x, h), (255, 255, 255), line_thickness)
    cv2.rectangle(binary, (51, 30), (131, 277), (255, 255, 255), thickness=-1)

    return binary


def enhance_contrast(image):
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced_image = clahe.apply(image)

    return enhanced_image


def split_dates(text_list):
    result = []
    for text in text_list:
        if text is None:
            result.append(None)
            continue
        
        numbers_str = ''.join([x for x in text if x.isdigit()])
        
        if len(numbers_str) < 8:
            result.append(None)
            continue
        
        temp_dates = []
        for i in range(0, len(numbers_str), 8):
            date_str = numbers_str[i:i+8]
            try:
                date = datetime.datetime.strptime(date_str, '%d%m%Y').date()
                temp_dates.append(date.strftime('%d.%m.%Y'))
            except ValueError:
                continue
        
        result.append(temp_dates if temp_dates else None)

    return result


def clean_and_split(text):
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        line = line.replace('(', '1').replace(')', '1')
        cleaned_line = re.sub(r'\D', '', line)
        if cleaned_line and len(cleaned_line) > 4:
            cleaned_lines.append(cleaned_line)
        else:
            cleaned_lines.append(None)
    return cleaned_lines


def shorten_text(text_list):
    for i in range(len(text_list)):
        if text_list[i] is None:
            continue
        text_list[i] = text_list[i][::-1]
        if len(text_list[i]) > 24:
            text_list[i] = text_list[i][:24]
        text_list[i] = text_list[i][::-1]
    return text_list

def extract_first_number(input_string):
    numbers = re.findall(r'\d+', input_string)
    if numbers:
        return int(numbers[0])
    else:
        return None

def process_list(input_list):
    first_non_none = next((i for i, item in enumerate(input_list) if item is not None), None)
    
    if first_non_none is not None and first_non_none > 1:
        input_list = input_list[first_non_none-1:] 
    
    return input_list[:9]

def read(image, ftype, batch_model, launch_type, debugging):
    if launch_type == 'linux':
        from cv.nn import core as nn_core
        pytesseract.pytesseract.tesseract_cmd = fr'{os.getcwd()}/tesseract/tesseract'
    elif launch_type == 'windows':
        from nn import core as nn_core
        pytesseract.pytesseract.tesseract_cmd = fr"C:\Program Files\Tesseract-OCR\tesseract.exe"

    logger = nn_core.get_logger(__name__)
    return_format = {
        'vu1': ['1', '2', '3', '4a', '4b', '4c', '5', '8'],
        'vu2': ['A', 'B', 'C', 'D', 'BE', 'CE', 'DE', 'tram', 'troll'],
        'sts1':['regnum', 'vin', 'model', 'type', 'category', 'year', 'chassis', 'body', 'color', 'power', 'eco_class', 'maxmass', 'mass']
    }
    transliterate_layout = {
        'vu1': [
            [0, 1],
            [2, 3],
            [5, 6],
            [9, 10],
            [12, 13]
        ]
    }
    combiner_layout = {
        'vu1': [
            [[0, 1], '\n'],
            [[2, 3], '\n'],
            [[4, 5, 6], '\n'],
            [[9, 10], '\n'],
            [[11, 12, 13], '\n']
        ]
    }

    # get text batch from image
    results = batch_model(image, verbose=False, save=debugging)
    for result in results:
        boxes = result.boxes.xyxy.tolist()[0]
    if ftype in ['vu1', 'vu2']:
        image = image[int(boxes[1] * 0.98):int(boxes[3]), int(boxes[0] * 0.98):int(boxes[2])]
        logger.info('[reader] cropped image')

        # smaller
        height, width = image.shape[:2]
        scale = min(500.0, max(width, height)) / max(width, height)
        new_width = int(width * scale)
        new_height = int(height * scale)
        image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
    elif ftype in ['sts1', 'sts2']:
        # smaller
        height, width = image.shape[:2]
        scale = min(1500.0, max(width, height)) / max(width, height)
        new_width = int(width * scale)
        new_height = int(height * scale)
        image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)

    # preprocess for pytesseract
    if ftype == 'vu1':
        image = preprocess_image(image)
        logger.info('[reader] vu1 image recognition started')
        # get text from image
        logger.info('[reader] reading text')
        text = [element for element in
                pytesseract.image_to_string(image, lang='rus', config='--oem 1 --psm 6').split('\n') if element != '']
        if debugging: logger.info('[reader] result: %s' % text)
        if not text[0].isupper(): text = text[1:]

        # format text
        logger.info('[reader] formatting text')
        if len(text[0].split()) > 1: text = text[1:]
        text = extract_and_replace_dates(text)
        text = clean_list_elements(text)
        text = remove_leading_spaces(text)
        text = transliterate(text, transliterate_layout, ftype)
        text = combine_elements(combiner_layout, text, ftype)
        return_text = dict(zip(return_format['vu1'], text))
        gibdd = f"ГИБДД {extract_first_number(return_text['4c'])}\nGIBDD {extract_first_number(return_text['4c'])}"
        return_text['4c'] = gibdd
        logger.info('[reader] returned result')
        return return_text

    elif ftype == 'vu2':
        image = preprocess_image(image)
        logger.info('[reader] vu2 image recognition started')
        image = warp_perspective(image)
        image = remove_grid(
            image,
            [1, 35, 70, 106, 141, 175, 210, 246, 279, 315, 350],
            [1, 135, 230, 326, 498],
            line_thickness=7
        )
        image = enhance_contrast(image)
        
        logger.info('[reader] reading text')
        text = pytesseract.image_to_string(image, lang='eng', config='--oem 1 --psm 6')
        if debugging: logger.info('[reader] result: %s' % text)
        logger.info('[reader] formatting text')
        text = clean_and_split(text)[1:]
        text = shorten_text(text)
        text = split_dates(text)
        text = process_list(text)
        return_text = dict(zip(return_format['vu2'], text))
        logger.info('[reader] returned result')
        return return_text
    
    elif ftype == 'sts1':
        logger.info('[reader] pts1 image recognition started')
        # preprocessing
        cv2.rectangle(image, (0, 0), (width, 200), (255, 255, 255), -1)
        height, width = image.shape[:2]

        image = image[200:height, 0:width]
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        text_en = [element for element in
                pytesseract.image_to_string(image, lang='eng', config='--oem 1 --psm 4').split('\n') if element != '']
        text = [element for element in
                pytesseract.image_to_string(image, lang='rus', config='--oem 1 --psm 4').split('\n') if element != '']
        return_text = [None]*13
        return_text[0] = text[0].split()[-1]
        text = text[3:]
        return_text[1] = text_en[2].replace(' ', '') # vin
        return_text[2] = ' '.join(text[0].replace('—', '').split()[2:]) # model
        return_text[3] = ' '.join(text[1].split()[2:]) # type
        return_text[4] = text[2].split()[-1].lower() # category
        return_text[5] = text[3].split()[-1] # year
        text = text[4:]
        return_text[6] = ' '.join(text[0].split()[3:]) # chassis
        return_text[12] = text[-1].split()[-1] # mass
        return_text[11] = text[-2].split()[-1] # maxmass
        return_text[10] = text[-3].split('класс ')[1] # eco_class
        try: return_text[9] = text[1].split('с. ')[1].replace(' ', '') # power
        except: None
        try: 
            if return_text[9] != None: return_text[9] = text[1].split('с ')[1].replace(' ', '') # power
        except: None
        return_text[7] = return_text[1] # body

        for x in text:
            if 'цвет' in x.lower(): return_text[8] = ' '.join(x.split()[1:])

        return_text = dict(zip(return_format['sts1'], return_text))
        return return_text