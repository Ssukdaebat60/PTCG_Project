import sys
import requests
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QScrollArea, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QCompleter, QLineEdit, QComboBox
from PyQt5.QtWidgets import QTextEdit, QDesktopWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PTCG_DB_MAKER import *
from PTCG_TRANSLATOR import *


WORD_FILENAME = "WordDictionary.csv"
CARD_FILENAME = "CardDictionary.csv"

def get_Completer_list(df):
    return list(df['en'])+list(df['ko'])

def open_CSV_as_DF(FILENAME):
    return pd.read_csv(FILENAME)


class PTCG_Window(QWidget):
    def __init__(self):
        super().__init__()
        self.word_df = open_CSV_as_DF(WORD_FILENAME)
        self.card_df = open_CSV_as_DF(CARD_FILENAME)
        self.setWindowTitle("PTCG_Search")
        self.resize(800, 940)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.total_layout = QVBoxLayout()
        self.card_list=[]
        
        #검색창
        self.completer = QCompleter(get_Completer_list(self.card_df))
        self.line_edit_search = QLineEdit()
        self.line_edit_search.resize(100, 20)
        self.line_edit_search.setCompleter(self.completer)
        self.line_edit_search.setPlaceholderText("카드 이름으로 검색하세요 (영어추천)")
        #검색 버튼
        self.button_search = QPushButton("검색")
        self.button_search.clicked.connect(self.Button_Search_Function)
        #조건 초기화 버튼
        self.button_init = QPushButton("초기화")
        self.button_init.clicked.connect(self.Button_Init_Function)
        #검색 레이아웃 추가
        self.search_layout = QHBoxLayout()
        self.search_layout.addWidget(self.line_edit_search)
        self.search_layout.addWidget(self.button_search)
        self.search_layout.addWidget(self.button_init)
        self.total_layout.addLayout(self.search_layout)

        #조건 선택 창
        self.button_add_combobox = QPushButton("조건추가")
        self.button_add_combobox.clicked.connect(self.Button_Show_Combobox_Function)
        #조건 검색 레이아웃 추가
        self.condition_layout = QVBoxLayout()
        self.total_layout.addWidget(self.button_add_combobox)
        self.total_layout.addLayout(self.condition_layout)
        
        #이미지창
        self.img_scroll_area = QScrollArea(self)
        self.img_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn) 
        self.img_scroll_content = QWidget()
        self.img_scroll_layout = QHBoxLayout()
        #초기 이미지 (로고)
        self.pixmap_logo = QPixmap()
        self.pixmap_logo.load("Logo.png")
        #QLabel에 이미지 표시
        self.label_logo = QLabel(self)
        self.label_logo.setPixmap(self.pixmap_logo)
        self.label_logo.setFixedSize(self.pixmap_logo.width(), self.pixmap_logo.height())
        self.img_layout = QVBoxLayout()
        self.img_layout.addWidget(self.label_logo)
        self.img_scroll_layout.addLayout(self.img_layout)
        #이미지 레이아웃 추가
        self.img_scroll_content.setLayout(self.img_scroll_layout)
        self.img_scroll_area.setWidget(self.img_scroll_content)
        self.img_scroll_area.setWidgetResizable(True)
        self.total_layout.addWidget(self.img_scroll_area) # 안되면 layout으로

        #정보창
        #정보 레이아웃 추가
        self.en_info_label = QLabel("ENG INFO")
        self.kr_info_label = QLabel("한국 정보")
        self.en_info_textedit = QTextEdit()
        self.kr_info_textedit = QTextEdit()
        self.en_info_textedit.setPlainText("English information will be displayed.")
        self.kr_info_textedit.setPlainText("한국어 정보가 표시됩니다.")
        self.en_info_textedit.setReadOnly(True)
        self.kr_info_textedit.setReadOnly(True)
        self.en_info_layout = QVBoxLayout()
        self.kr_info_layout = QVBoxLayout()
        self.en_info_layout.addWidget(self.en_info_label)
        self.en_info_layout.addWidget(self.en_info_textedit)
        self.kr_info_layout.addWidget(self.kr_info_label)
        self.kr_info_layout.addWidget(self.kr_info_textedit)
        self.total_info_layout = QHBoxLayout()
        self.total_info_layout.addLayout(self.en_info_layout)
        self.total_info_layout.addLayout(self.kr_info_layout)
        self.total_layout.addLayout(self.total_info_layout)

        #사전입력창
        self.dict_eng_label = QLabel("ENG")
        self.dict_kor_label = QLabel("KOR")
        self.dict_eng_lineedit = QLineEdit()
        self.dict_eng_lineedit.textChanged.connect(self.check_text)
        self.dict_kor_lineedit = QLineEdit()
        #사전 저장/삭제 버튼
        self.dict_save_button = QPushButton("저장")
        self.dict_save_button.setEnabled(False)
        self.dict_delete_button = QPushButton("삭제")
        self.dict_delete_button.setEnabled(False)
        self.dict_save_button.clicked.connect(self.Button_Save)
        self.dict_delete_button.clicked.connect(self.Button_Delete)
        #사전 레이아웃 추가
        self.dict_layout = QHBoxLayout()
        self.dict_layout.addWidget(self.dict_eng_label)
        self.dict_layout.addWidget(self.dict_eng_lineedit)
        self.dict_layout.addWidget(self.dict_kor_label)
        self.dict_layout.addWidget(self.dict_kor_lineedit)
        self.dict_layout.addWidget(self.dict_save_button)
        self.dict_layout.addWidget(self.dict_delete_button)
        self.total_layout.addLayout(self.dict_layout)

        #메시지 출력창
        self.message_label = QLabel("MESSAGE : ")
        self.message_lineedit = QLineEdit()
        self.message_lineedit.setReadOnly(True)
        self.message_layout = QHBoxLayout()
        self.message_layout.addWidget(self.message_label)
        self.message_layout.addWidget(self.message_lineedit)
        self.total_layout.addLayout(self.message_layout)
        
        #레이아웃 보이기
        self.setLayout(self.total_layout)

        
    def Button_Search_Function(self): #검색 결과 보이기(수정필요) 조건 & 검색결과가 없을 때 & 한국어 입력
        name = ''.join(list((filter(str.isalpha,self.line_edit_search.text()))))
        if name == "":
            return 0
        self.card_list = search_by_card_name(name)
        self.clear_layout(self.img_scroll_layout)
        self.kr_info_textedit.clear()
        self.en_info_textedit.clear()
        if self.card_list:
            self.show_images()
        else:
            pixmap = QPixmap()
            pixmap.load("noresult.png")
            label = QLabel(self)
            label.setPixmap(pixmap)
            label.setFixedSize(pixmap.width(), pixmap.height())
            img_layout = QVBoxLayout()
            img_layout.addWidget(label)
            self.img_scroll_layout.addLayout(img_layout)

    def Button_Show_Combobox_Function(self): # 조건 추가하기(수정필요)
        combobox = QComboBox()
        combobox.addItems(["NULL", "항목 1", "항목 2", "항목 3"])
        combobox.setCurrentIndex(-1)
        self.condition_layout.addWidget(combobox)
    
    def Button_Init_Function(self): #scroll sub layout 초기화 (전부 비우기 + 버튼 보이기)
        while self.condition_layout.count():
            item = self.condition_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        self.clear_layout(self.img_scroll_layout)
        self.kr_info_textedit.clear()
        self.en_info_textedit.clear()
        self.message_lineedit.clear()
        self.line_edit_search.clear()
    
    def show_images(self):
        for idx, card in enumerate(self.card_list):
            # 이미지 데이터 가져오기
            response = requests.get(card.images.small)
            image_data = response.content
            # 이미지를 PyQt QPixmap으로 변환
            pixmap = QPixmap()
            pixmap.loadFromData(image_data)
            # QLabel에 이미지 표시
            label = QLabel(self)
            label.setPixmap(pixmap)
            label.setFixedSize(pixmap.width(), pixmap.height())
            #self.img_scroll_layout.addWidget(label)
            # 선택 버튼
            button_select = QPushButton(f"{str(idx+1)}")
            button_select.clicked.connect(self.Button_Select_Function)
            # 단위 이미지 레이아웃 추가
            img_layout = QVBoxLayout()
            img_layout.addWidget(label)
            img_layout.addWidget(button_select)
            self.img_scroll_layout.addLayout(img_layout)

    def show_info(self, card):
        self.kr_info_textedit.clear()
        self.en_info_textedit.clear()
        card_en_json = get_JSON_from_Card(card)
        card_kr_json = get_kr_from_en_json(card_en_json)
        self.en_info_textedit.setPlainText(json_to_str(card_en_json))
        self.kr_info_textedit.setPlainText(json_to_str(card_kr_json))
    
    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.layout():
                self.clear_layout(item.layout())
                item.layout().deleteLater()
            if item.widget():
                item.widget().deleteLater()
            del item
        
    def Button_Save(self):
        addWord_EN_KO(self.word_df, self.dict_eng_lineedit.text(), self.dict_kor_lineedit.text())
        DF_to_CSV(self.word_df)
        msg = self.dict_eng_lineedit.text() + " " + self.dict_kor_lineedit.text() + " " + "is saved"
        self.dict_eng_lineedit.clear()
        self.dict_kor_lineedit.clear()
        self.Alert_Message(msg)
    
    def Button_Delete(self):
        try:
            deleteWord(self.word_df, self.dict_eng_lineedit.text())
        except Exception as e:
            msg = self.dict_eng_lineedit.text()+"is not exist."
            self.Alert_Message(msg)
    
    def Button_Select_Function(self): #Card to JSON
        self.dict_eng_lineedit.clear()
        self.dict_kor_lineedit.clear()
        clicked_button = self.sender()
        self.show_info(self.card_list[int(clicked_button.text())-1])
    
    def Alert_Message(self, message):
        self.message_lineedit.setText(message)
    
    def check_text(self):
        if self.dict_eng_lineedit.text():
            self.dict_save_button.setEnabled(True)
        else:
            self.dict_save_button.setEnabled(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PTCG_Window()
    window.show()
    sys.exit(app.exec_())
