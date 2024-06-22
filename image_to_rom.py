import math
from PIL import Image

def resize_image(image_path, new_height):
    # 이미지 파일을 열기
    image = Image.open(image_path)
    # 이미지의 원래 해상도를 구하기
    original_width, original_height = image.size
    # 이미지의 너비와 높이의 비율을 구하기
    ratio = original_width / original_height
    # 이미지의 새로운 너비를 구하기
    new_width = int(new_height * ratio)
    # 이미지의 새로운 해상도를 설정
    new_size = (new_width, new_height)
    # 이미지의 해상도를 바꾸기
    image = image.resize(new_size)
    # 결과 출력
    print(f"이미지의 해상도가 {original_width}x{original_height}에서 {new_width}x{new_height}로 바뀌었습니다.")
    return image

# 이미지의 배경을 검은색으로 바꾸는 함수
def change_background (image_path, new_color):
    # 이미지를 열고 RGBA 모드로 변환
    img = Image.open (image_path).convert ("RGBA")

    # 이미지의 픽셀 데이터를 가져옴
    pixels = img.getdata ()

    # 새로운 픽셀 데이터를 저장할 리스트
    new_pixels = []

    # 픽셀 데이터를 순회하면서 배경이 없는 픽셀을 찾음
    for pixel in pixels:
        # 투명도 값이 0인 픽셀이면 배경이 없는 픽셀
        if pixel[3] == 0:
            # 배경이 없는 픽셀을 새로운 색으로 바꿈
            new_pixels.append (new_color)
        else:
            # 배경이 있는 픽셀은 그대로 유지
            new_pixels.append (pixel)

    # 이미지에 새로운 픽셀 데이터를 적용
    img.putdata (new_pixels)

    # 이미지를 반환
    return img

def get_pixel_data(image_path):
    # 이미지 파일을 열기
    image = Image.open(image_path)
    # 이미지의 너비와 높이를 구하기
    width, height = image.size
    # 픽셀 데이터를 저장할 빈 리스트 생성
    pixel_data = []
    # 각 픽셀에 대해 반복
    for x in range(width):
        for y in range(height):
            # 픽셀의 RGB 값을 구하기
            r, g, b = image.getpixel((x, y))[0:3]
            # 픽셀의 좌표와 RGB 값을 튜플로 묶어서 리스트에 추가
            pixel_data.append(((x, y), (r, g, b)))
    # 픽셀 데이터 리스트 반환
    return pixel_data, width, height

def save_pixel_data_4bit_color(pixel_data, width, height, file_path):
    
    width_bit = int(math.log2(width-1) + 1)
    height_bit = int(math.log2(height-1) + 1)

    # 텍스트 파일을 쓰기 모드로 열기
    file = open(file_path, "w")
    file.write(f"\t\t\t// right: {width_bit}'d{width-1}, bottom: {height_bit}'d{height-1}\n")

    # 픽셀 데이터 리스트에 대해 반복
    for pixel in pixel_data:
        # 픽셀의 좌표와 RGB 값을 구하기
        coord, rgb = pixel
        # 픽셀의 좌표와 RGB 값을 문자열로 변환하기
        x, y = coord
        coord_str = '{' + str(width_bit) + "'d" + str(x) + ', ' + str(height_bit) + "'d" + str(y) +'}'
        rgb_str = "12'h" + str(hex(int(rgb[0]/16)))[2:] + str(hex(int(rgb[1]/16)))[2:] + str(hex(int(rgb[2]/16)))[2:]
        # 픽셀의 좌표와 RGB 값을 형식에 맞게 결합하기
        pixel_str = "\t\t\t" + coord_str + ": color_data = " + rgb_str + ";\n"
        # 텍스트 파일에 픽셀 데이터 쓰기
        file.write(pixel_str)

    # 텍스트 파일 닫기
    file.close()

# 함수 호출
image = resize_image("background.jpg", 480) # 이미지 파일 이름, 세로 픽셀 갯수 (가로 세로 비율 맞게 resizing)

#####################디버깅용##################################
image.save("resized_image.png")
image = change_background("resized_image.png", (0, 0, 0))
image.save("changed_background.png")
###############################################################

pixel_data, width, height = get_pixel_data("changed_background.png")
save_pixel_data_4bit_color(pixel_data, width, height, "pixel_data_4bit.txt")

print("픽셀 데이터가 파일에 저장되었습니다.")
