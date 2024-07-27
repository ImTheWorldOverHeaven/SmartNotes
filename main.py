from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QInputDialog, QHBoxLayout, QVBoxLayout
import json

app = QApplication([])

# Define the dark theme stylesheet
dark_stylesheet = """
    QWidget {
        background-color: #2E2E2E;
        color: #F0F0F0;
    }
    QLineEdit, QTextEdit, QListWidget {
        background-color: #3E3E3E;
        color: #F0F0F0;
        border: 1px solid #4A4A4A;
    }
    QPushButton {
        background-color: #4A4A4A;
        color: #F0F0F0;
        border: 1px solid #5A5A5A;
    }
    QPushButton:hover {
        background-color: #5A5A5A;
    }
    QLabel {
        color: #F0F0F0;
    }
"""

win = QWidget()
win.setWindowTitle("Умные заметки")
win.resize(900, 600)
win.setStyleSheet(dark_stylesheet)  # Apply the dark theme stylesheet to the main window

list_notes = QListWidget()
list_notes_label = QLabel("Список заметок")

button_create = QPushButton("Создать заметку")
button_del = QPushButton("Удалить заметку")
button_save = QPushButton("Сохранить заметку")

field_tag = QLineEdit("")
field_tag.setPlaceholderText("Введите тег ...")
field_text = QTextEdit()
button_tag_add = QPushButton("Добавить к заметке")
button_tag_del = QPushButton("Открепить от заметки")
button_tag_search = QPushButton("Искать заметку")
list_tags = QListWidget()
list_tags_label = QLabel("Список тегов")

layout_notes = QHBoxLayout()
col_1 = QVBoxLayout()
col_1.addWidget(field_text)

col_2 = QVBoxLayout()
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)
row_1 = QHBoxLayout()
row_1.addWidget(button_create)
row_1.addWidget(button_del)
row_2 = QHBoxLayout()
row_2.addWidget(button_save)
col_2.addLayout(row_1)
col_2.addLayout(row_2)

col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)
row_3 = QHBoxLayout()
row_3.addWidget(button_tag_add)
row_3.addWidget(button_tag_del)
row_4 = QHBoxLayout()
row_4.addWidget(button_tag_search)

col_2.addLayout(row_3)
col_2.addLayout(row_4)

layout_notes.addLayout(col_1, stretch=2)
layout_notes.addLayout(col_2, stretch=1)
win.setLayout(layout_notes)

def show_note():
    key = list_notes.selectedItems()[0].text()
    print(key)
    field_text.setText(notes[key]["текст"])
    list_tags.clear()
    list_tags.addItems(notes[key]["теги"])

def add_note():
    note_name, ok = QInputDialog.getText(win, "Добавить заметку", "Название заметки: ")
    if ok and note_name != "":
        notes[note_name] = {"текст": "", "теги": []}
        list_notes.addItem(note_name)
        list_tags.addItems(notes[note_name]["теги"])
        print(notes)

def save_note():
    # Проверяем, есть ли выбранные элементы в списке заметок
    if list_notes.selectedItems():
        # Получаем ключ выбранного элемента (заметки)
        key = list_notes.selectedItems()[0].text()
        # Обновляем текст заметки в словаре notes
        notes[key]["текст"] = field_text.toPlainText()
        # Открываем файл notes_data.json для записи обновленных данных
        with open("notes_data.json", "w") as file:
            # Сохраняем обновленный словарь notes в файл в формате JSON
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        # Выводим текущие заметки в консоль
        print(notes)
    else:
        # Если ни одна заметка не выбрана, выводим сообщение об ошибке
        print("Заметка для сохранения не выбрана!")


def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        list_notes.addItems(notes)
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("Заметка для удаления не выбрана!")

def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        if not tag in notes[key]["теги"]:
            notes[key]["теги"].append(tag)
            list_tags.addItem(tag)
            field_tag.clear()
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("Заметка для добавления тега не выбрана!")

def del_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[key]["теги"].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[key]["теги"])
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("Заметка для удаления тега не выбрана!")

def search_tag():
    print(button_tag_search.text())
    tag = field_tag.text()
    if button_tag_search.text() == "Искать заметку по тегу" and tag:
        print(tag)
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]["теги"]:
                notes_filtered[note] = notes[note]
        button_tag_search.setText("Сбросить поиск")
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filtered)
        print(button_tag_search.text())
    elif button_tag_search.text() == "Сбросить поиск":
        field_tag.clear()
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes)
        button_tag_search.setText("Искать заметку по тегу")
        print(button_tag_search.text())
    else:
        pass

button_create.clicked.connect(add_note)
list_notes.itemClicked.connect(show_note)
button_save.clicked.connect(save_note)
button_del.clicked.connect(del_note)
button_tag_add.clicked.connect(add_tag)
button_tag_del.clicked.connect(del_tag)
button_tag_search.clicked.connect(search_tag)

with open("notes_data.json", "r") as file:
    notes = json.load(file)
list_notes.addItems(notes)

win.show()
app.exec_()
