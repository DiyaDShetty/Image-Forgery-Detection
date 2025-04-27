from sys import exit
import random
import string
import os
import numpy as np
from keras.models import load_model
from sklearn.metrics import accuracy_score
from PIL import Image, ImageDraw, ImageFont
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QLabel, QLineEdit, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from ela import convert_to_ela_image
from prediction import predict_result

class LoginDialog(QDialog):
    def __init__(self):
        super(LoginDialog, self).__init__()
        loadUi("login_dialog.ui", self)  # Load the login UI file
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pushButton.clicked.connect(self.attempt_login)
        self.checkBox.stateChanged.connect(self.toggle_password_visibility)

        # Generate and display CAPTCHA
        self.generate_captcha()
        
    def toggle_password_visibility(self, state):
        if state == Qt.Checked:
            self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)

    def generate_captcha(self):
        # Generate random CAPTCHA text
        captcha_text = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=6))
        self.correct_captcha = captcha_text

        # Create an image for CAPTCHA
        image = Image.new('RGB', (200, 100), color=(255, 255, 255))
        d = ImageDraw.Draw(image)
        font = ImageFont.truetype('arial.ttf', 36)
        d.text((10, 10), captcha_text, font=font, fill=(0, 0, 0))

        # Save the image or convert to bytes and set as pixmap
        image_path = "captcha_image.png"
        image.save(image_path)
        pixmap = QPixmap(image_path)
        self.captcha_label.setPixmap(pixmap)

    def attempt_login(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        captcha_response = self.captcha_input.text()

        # Dummy check for username, password, and CAPTCHA
        if username == "diya" and password == "password" and captcha_response == self.correct_captcha:
            QMessageBox.information(self, "Login Successful", "Welcome, Diya")
            self.accept()  # Close the dialog and return QDialog.Accepted
            self.lineEdit.setText("")
        else:
            QMessageBox.warning(self, "Login Failed", "Incorrect username, password, or CAPTCHA.")
            # Generate new CAPTCHA
            self.generate_captcha()
            self.captcha_input.setText("") 

class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("gui.ui", self)
        self.fname = ""  
        self.setWindowIcon(QIcon("icon.ico"))
        self.Browse.clicked.connect(self.open_image)
        self.Test.clicked.connect(self.result)
        self.Quit.clicked.connect(self.close_main_window)

    def open_image(self):
        # display original image
        self.fname = QFileDialog.getOpenFileName(
            self, "Open file", "C:'", ("*.png, *.xmp *.jpg")
        )
        self.filename.setText(self.fname[0])
        pixmap = QPixmap(self.fname[0])
        self.ORIGINAL_IMAGE.setPixmap(pixmap)
        self.ORIGINAL_IMAGE.setPixmap(
            pixmap.scaled(self.ORIGINAL_IMAGE.size(), Qt.IgnoreAspectRatio)
        )
        self.ORIGINAL_IMAGE.show()

        # display ela image
        convert_to_ela_image(self.fname[0], 90)
        pixmap1 = QPixmap("ela_image.png")
        self.ELA_IMAGE.setPixmap(pixmap1)
        self.ELA_IMAGE.setPixmap(
            pixmap1.scaled(self.ELA_IMAGE.size(), Qt.IgnoreAspectRatio)
        )
        self.ELA_IMAGE.show()
        
    
        

    def result(self):
        
        if not self.fname:
            QMessageBox.warning(self, "No Image Selected", "Please upload an image first.")
            return

        (prediction, confidence) = predict_result((self.fname))
        self.Result.setText(f"Prediction: {prediction}\nConfidence: {confidence} %")
        
    def close_main_window(self):
        # quit window
        reply = QMessageBox.question(
            self,
            "Quit",
            "Are you sure you want to quit?",
            QMessageBox.Cancel | QMessageBox.Close,
        )
        if reply == QMessageBox.Close:
            self.close()


def main():
    app = QApplication([])
    login_dialog = LoginDialog()
    if login_dialog.exec_() == QDialog.Accepted:
        # Login successful, proceed with main application logic
        main_window = MainWindow()
        main_window.show()
        exit(app.exec_())

if __name__ == "__main__":
    main()
