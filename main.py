from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QProgressBar, QLabel, QListWidget, QInputDialog,QMessageBox, QGraphicsOpacityEffect, QHBoxLayout
from PyQt5.QtCore import Qt,QTimer, QPropertyAnimation, pyqtProperty, QSize
from PyQt5.QtGui import QIcon,QPixmap, QPainter
import pickle
import os


class RainbowLabel(QLabel):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.color_shift = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_text_color)
        self.timer.start(10)  # Update every 10 ms

    def update_text_color(self):
        # Update the color shift
        self.color_shift = (self.color_shift + 1) % 100

        # Calculate the color stops based on the color shift
        stops = [(i + self.color_shift) % 100 / 100 for i in range(0, 101, 20)]

        # Create the stylesheet string with the new color stops
        stylesheet = """
            QLabel {{
                color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:{} red, stop:{} orange, stop:{} yellow, stop:{} green, stop:{} blue, stop:{} purple);
                font-weight: bold;
                font-family: Impact;
                font-size: 75px;
            }}
        """.format(*stops)

        # Apply the new stylesheet to the label
        self.setStyleSheet(stylesheet)

class RainbowImageLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGraphicsEffect(QGraphicsOpacityEffect())
        self.graphicsEffect().setOpacity(1)
        self.color_shift = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_border_color)
        self.timer.start(10)  # Update every 10 ms

    def update_border_color(self):
        # Update the color shift
        self.color_shift = (self.color_shift + 1) % 100

        # Calculate the color stops based on the color shift
        stops = [(i + self.color_shift) % 100 / 100 for i in range(0, 101, 20)]

        # Create the stylesheet string with the new color stops
        stylesheet = """
            QLabel {{
                border: 3px solid qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:{} red, stop:{} orange, stop:{} yellow, stop:{} green, stop:{} blue, stop:{} purple);
                border-radius: 5px;
            }}
        """.format(*stops)

        # Apply the new stylesheet to the label
        self.setStyleSheet(stylesheet)
    @pyqtProperty(float)
    def opacity(self):
        return self.graphicsEffect().opacity()

    @opacity.setter
    def opacity(self, value):
        self.graphicsEffect().setOpacity(value)

class RainbowListbox(QListWidget):
    def __init__(self,user):
        super().__init__()
        self.user = user  # Store a reference to the user
        self.color_shift = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_border_color)
        self.timer.start(22)  # Update every 100 ms
        self.setDragDropMode(QListWidget.InternalMove)

    def dropEvent(self, event):
        super().dropEvent(event)  # Call the superclass's dropEvent method
        self.user.update_task_order()  # Update the task order

    def update_border_color(self):
        # Update the color shift
        self.color_shift = (self.color_shift + 1) % 100

        # Calculate the color stops based on the color shift
        stops = [(i + self.color_shift) % 100 / 100 for i in range(0, 101, 20)]

        # Create the stylesheet string with the new color stops
        stylesheet = """
            QListWidget {{
                border: 3px solid qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:{} red, stop:{} orange, stop:{} yellow, stop:{} green, stop:{} blue, stop:{} purple);
                border-radius: 5px;
                color: white;
                font-weight: bold;
                font-family: Papyrus;
                background-color: rgba(0, 0, 0, 0.7);
            }}
        """.format(*stops)

        # Apply the new stylesheet to the listbox
        self.setStyleSheet(stylesheet)


class AnimatedButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self._gradient_stops = 0
        self.color_shift = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_border_color)
        self.timer.start(10)  # Update every 100 ms

        # Create the animation
        self.animation = QPropertyAnimation(self, b'gradientStops')
        self.animation.setDuration(2000)  # 2 seconds
        self.animation.setStartValue(0)
        self.animation.setEndValue(100)
        self.animation.setLoopCount(-1)  # Loop indefinitely
        self.animation.start()

    @pyqtProperty(int)
    def gradientStops(self):
        return self._gradient_stops

    @gradientStops.setter
    def gradientStops(self, value):
        self._gradient_stops = value
        self.update_border_color()

    def update_border_color(self):
        # Update the color shift
        self.color_shift = (self.color_shift + 1) % 100

        # Calculate the color stops based on the color shift
        stops = [(i + self.color_shift + self._gradient_stops) % 100 / 100 for i in range(0, 101, 20)]

        # Create the stylesheet string with the new color stops
        stylesheet = """
            QPushButton {{
                border: 2px solid qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:{} red, stop:{} orange, stop:{} yellow, stop:{} green, stop:{} blue, stop:{} purple);
                border-radius: 5px;
                color: white;
                font-weight: bold;
                font-family: Papyrus;
                background-color: rgba(0, 0, 0, 0.9);
            }}
            QPushButton:hover {{
                border: 2px solid qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:{} red, stop:{} orange, stop:{} yellow, stop:{} green, stop:{} blue, stop:{} purple);
                border-radius: 5px;
                color: black;
                background-color: rgba(255, 255, 255, 0.9);
            }}
        """.format(*stops, *stops)

        # Apply the new stylesheet to the button
        self.setStyleSheet(stylesheet)



class MyWidget(QWidget):
    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent)
        self.pixmap = QPixmap(".\Background.png")
        image_size = self.pixmap.size()
         # Specify a maximum size for the image
        max_size = QSize(1500, 1500)  # Change this to your desired maximum size
        # Scale down the image if it's larger than the maximum size
        if image_size.width() > max_size.width() or image_size.height() > max_size.height():
            image_size.scale(max_size, Qt.KeepAspectRatio)
        # Resize the window to the size of the image
        self.resize(image_size)

    def paintEvent(self,event):
        painter = QPainter(self)
        pixmap = self.pixmap.scaled(
            self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
        )
        painter.drawPixmap(self.rect(), pixmap)

class Task:
    def __init__(self, name, exp):
        self.name = name
        self.exp = exp

class User:
    def __init__(self):
        self.tasks = []
        self.exp = 0
        self.level = 1
        self.progress = QProgressBar()
        self.level_up_label = RainbowLabel("LEVEL UP!", window)
        self.level_up_label.setAlignment(Qt.AlignCenter)
        self.level_up_label.setGeometry(window.rect())
        self.level_up_effect = QGraphicsOpacityEffect(self.level_up_label)
        self.level_up_label.setGraphicsEffect(self.level_up_effect)
        self.level_up_label.hide()
        self.level_up_animation = QPropertyAnimation(self.level_up_effect, b"opacity")
        self.image_label = RainbowImageLabel()
        self.image_label.setAlignment(Qt.AlignCenter)  # Center the image
        self.image_animation = QPropertyAnimation(self.image_label, b"opacity")
        self.level_label = QLabel(f"Level: {self.level}")
        self.level_label.setAlignment(Qt.AlignCenter)  # Center the text
        self.level_label.setStyleSheet("""
            color: Black;
            font-weight: bold;
            font-family: Papyrus;
            font-size: 30px;
        """)
        self.task_listbox = RainbowListbox(self)
        self.task_listbox.setStyleSheet("""
            color: black;
            font-weight: bold;
            font-family: Papyrus;
            background-color: rgba(255, 255, 255, 0.8);
        """)
        self.load_data()
        self.old_title = self.get_title()
        self.update_image()
        # Initialize the timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress_color)
        self.timer.start(10)  # Update every 100 ms

        # Initialize the color shift
        self.color_shift = 0

    def update_progress_color(self):
        # Update the color shift
        self.color_shift = (self.color_shift + 1) % 100

        # Calculate the color stops based on the color shift
        stops = [(i + self.color_shift) % 100 / 100 for i in range(0, 101, 20)]

        # Create the stylesheet string with the new color stops
        stylesheet = """
            QProgressBar {{
                border: 3px solid black;
                border-radius: 5px;
                text-align: center;
            }}

            QProgressBar::chunk {{
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:{} red, stop:{} orange, stop:{} yellow, stop:{} green, stop:{} blue, stop:{} purple);
            }}
        """.format(*stops)

        # Apply the new stylesheet to the progress bar
        self.progress.setStyleSheet(stylesheet)

    def load_data(self):
        if os.path.exists('anotherpro\data.pkl'):
            with open('anotherpro\data.pkl', 'rb') as f:
                data = pickle.load(f)
            self.tasks, self.exp, self.level = data
            for task in self.tasks:
                self.task_listbox.addItem(task.name)
            self.show_progress()
            title = self.get_title()  # Get the title based on the current level
            self.level_label.setText(f"Level: {self.level} - {title}")  # Display the level and title
    def save_data(self):
        with open('anotherpro\data.pkl', 'wb') as f:
            pickle.dump((self.tasks, self.exp, self.level), f)

    def add_task(self):
        task_name, ok = QInputDialog.getText(None, "Add Task", "Enter task name:")
        if task_name:
            task_exp, ok = QInputDialog.getInt(None, "Add Task", "Enter task experience points:")
            if task_exp <= 0:
                QMessageBox.warning(None, "Invalid Input", "Experience points must be greater than zero.")
            else:
                task = Task(task_name, task_exp)
                self.tasks.append(task)
                self.task_listbox.addItem(task.name)
                print(f"Added task: {task_name}. Experience points: {task_exp}")
                self.save_data()


    def complete_task(self):
        try:
            task_name = self.task_listbox.currentItem().text()
            for task in self.tasks:
                if task.name == task_name:
                    self.exp += task.exp
                    self.tasks.remove(task)
                    self.task_listbox.takeItem(self.task_listbox.currentRow())
                    print(f"Completed task: {task_name}. Gained {task.exp} exp.")
                    self.level_up()
                    self.show_progress()  # Update the progress bar
                    self.save_data()
        except:
            pass
    def delete_task(self):
        try:
            task_name = self.task_listbox.currentItem().text()
            for task in self.tasks:
                if task.name == task_name:
                    self.tasks.remove(task)
                    self.task_listbox.takeItem(self.task_listbox.currentRow())
                    print(f"Deleted task: {task_name}")
                    self.save_data()
        except:
            pass
    def get_title(self):
        if 1 <= self.level <= 25:
            return "Newbie"
        elif 26 <= self.level <= 50:
            return "Apprentice"
        elif 51 <= self.level <= 75:
            return "Intermediate"
        elif 76 <= self.level <= 100:
            return "High Class"
        elif 101 <= self.level <= 125:
            return "Journeyman"
        elif 126 <= self.level <= 150:
            return "Master"
        elif 151 <= self.level <= 175:
            return "Grandmaster"
        elif 176 <= self.level <= 200:
            return "Legend"
        elif 201 <= self.level <= 225:
            return "Epic"
        elif 226 <= self.level <= 250:
            return "Mythic"
        elif 251 <= self.level <= 275:
            return "Ascended"
        elif 276 <= self.level <= 300:
            return "Immortal"
        elif 301 <= self.level <= 325:
            return "Demigod"
        elif 326 <= self.level <= 350:
            return "God"
        elif 351 <= self.level <= 375:
            return "Transcendent"
        elif 376 <= self.level <= 400:
            return "Eternal"
        elif 401 <= self.level <= 425:
            return "Infinite"
        elif 426 <= self.level <= 450:
            return "Ultimate"
        elif 451 <= self.level <= 475:
            return "Absolute"
        elif 476 <= self.level <= 500:
            return "Supreme"
        elif 501 <= self.level <= 525:
            return "Unbounded"
        elif 526 <= self.level <= 550:
            return "Boundless"
        elif 551 <= self.level <= 575:
            return "The One"
        else:
            return "Unknown"

    def level_up(self):
        if self.exp >= self.level * 100:
            while self.exp >= self.level * 100:
                self.exp -= self.level * 100
                self.level += 1
                title = self.get_title()  # Get the title based on the new level
            if title != self.old_title:
                self.level_up_label.setText("TIER UP!")
            else:
                self.level_up_label.setText("LEVEL UP!")
            self.level_label.setText(f"Level: {self.level} - {title}")  # Display the level and title
            self.update_image()  # Update the image

            # Show the level up message
            self.level_up_label.show()
            self.level_up_label.raise_()  # Raise the label to the top of the window stack

            # Configure the animation
            self.level_up_animation.setDuration(2000)  # 2 seconds
            self.level_up_animation.setStartValue(1)  # Fully opaque
            self.level_up_animation.setEndValue(1)  # Fully transparent
            self.level_up_animation.finished.connect(self.level_up_label.hide)  # Hide the label when the animation finishes
            self.level_up_animation.start()

            print(f"Leveled up! Current level: {self.level}, Title: {title}")
            self.show_progress()  # Update the progress bar
            self.save_data()  # Save the data
        else:
            pass
    def show_progress(self):
        progress = self.exp / (self.level * 100)
        self.progress.setValue(int(progress * 100))
        QApplication.processEvents()
    
    def update_task_order(self):
        # Get the current order of tasks from the list box
        task_names = [self.task_listbox.item(i).text() for i in range(self.task_listbox.count())]
        
        # Reorder self.tasks based on the order of task_names
        self.tasks.sort(key=lambda task: task_names.index(task.name))
        
        self.save_data()  # Save the data
    def update_image(self):
        title = self.get_title()
        if title != self.old_title:  # Check if the title has changed
            self.start_image_animation()  # Start the animation
            self.old_title = title  # Update the current title
        title = self.get_title()
        image_path = f"anotherpro/pic_title/{title}.png"  # load the image in the pic_title folder
        pixmap = QPixmap(image_path).scaled(100, 100, Qt.KeepAspectRatio)
        self.image_label.setPixmap(pixmap)
        self.image_label.setFixedSize(pixmap.size())
    def start_image_animation(self):
        self.image_animation.setDuration(1000)  # 1 second
        self.image_animation.setStartValue(1)  # Fully opaque
        self.image_animation.setEndValue(1)  # Fully transparent
        self.image_animation.setKeyValueAt(0.5, 0)  # Fully opaque at the halfway point
        self.image_animation.setLoopCount(2)  # Blink twice
        self.image_animation.start()


app = QApplication([])
window = MyWidget()
# for changing the window background you can change the image you want into "Background.png" (or you can set it in the MyWidget class)
# Set the window title
window.setWindowTitle("Daily Quest v1.20 by Void")

# Set the window icon
window.setWindowIcon(QIcon('.\Logo.png'))

layout = QVBoxLayout()

user = User()

image_label_layout = QHBoxLayout()
image_label_layout.addWidget(user.image_label, 0, Qt.AlignCenter)

layout.addWidget(user.level_label)
layout.addLayout(image_label_layout)

add_button = AnimatedButton("Add Task")
add_button.setMaximumWidth(200)  # Adjust the width as needed
add_button.setStyleSheet("""
    color: black;
    font-weight: bold;
    font-family: Papyrus;
    background-color: rgba(255, 255, 255, 0.9);
    
""")  # Make the button transparent
add_button.clicked.connect(user.add_task)

# Create a layout for the button to center it
button_layout = QVBoxLayout()
button_layout.addWidget(add_button, 0, Qt.AlignCenter)

layout.addLayout(button_layout)

complete_button = AnimatedButton("Complete Task")
complete_button.setMaximumWidth(200)  # Adjust the width as needed
complete_button.setStyleSheet("""
    color: black;
    font-weight: bold;
    font-family: Papyrus;
    background-color: rgba(255, 255, 255, 0.9);
""")  # Make the button transparent
complete_button.clicked.connect(user.complete_task)

# Create a layout for the button to center it
complete_button_layout = QVBoxLayout()
complete_button_layout.addWidget(complete_button, 0, Qt.AlignCenter)

layout.addLayout(complete_button_layout)

delete_button = AnimatedButton("Delete Task")
delete_button.setMaximumWidth(200)  # Adjust the width as needed
delete_button.setStyleSheet("""
    color: black;
    font-weight: bold;
    font-family: Papyrus;
    background-color: rgba(255, 255, 255, 0.9);
""")  # Make the button transparent
delete_button.clicked.connect(user.delete_task)

# Create a layout for the button to center it
delete_button_layout = QVBoxLayout()
delete_button_layout.addWidget(delete_button, 0, Qt.AlignCenter)

layout.addLayout(delete_button_layout)

layout.addWidget(user.task_listbox)
layout.addWidget(user.progress)

window.setLayout(layout)
window.show()

app.exec_()
