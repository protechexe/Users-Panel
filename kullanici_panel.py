from art import text2art
from tabulate import tabulate
from termcolor import colored
import sqlite3
import time
import hashlib
import os

def ClearScreen():
    os.system("cls" if os.name == "nt" else "clear")

def PrintBanner():
    banner = text2art("USERS PANEL", font="big", chr_ignore=True)
    print(banner)
    print("Kullanıcı Paneline Hoş Geldiniz!")
    print("Paneli yazan/oluşturan: Yunus Emre")
    print("İnstagram: @yuns.eemrree")
    print("-"*65,"\n")

def PrintMenu():
    table = [
        ["1.","Kullanıcı Kayıt İşlemleri"],
        ["2.","Kullanıcı Giriş İşlemleri"],
        ["3.","Kayıtlı Kullanıcı Bilgileri Gösterme"],
        ["4.","Kayıtlı Kullanıcı Silme İşlemleri"],
        ["5.","Çıkış"],
    ]

    headers = ["Numara","İşlem"]
    print(tabulate(table, headers, tablefmt="grid"))

def CalismaSuresi():
    while True:
        islem = GetInput("Programa devam etmek için entera, çıkış için 5 e basın: ")
        if islem == "5":
            PrintInfo("Çıkış Yapılıyor..")
            time.sleep(1)
            exit()
        else:
            break

def GetInput(prompt):
    return input("[?] " + prompt)

def PrintInfo(message):
    print(colored("[INFO] ","green") + message)

def PrintSuccess(message):
    print(colored("[SUCCESS] ","light_green") + message)

def PrintError(message):
    print(colored("[ERROR] ","red") + message)


class Veritabani():
    def __init__(self, database="users.db"):
        self.connect = sqlite3.connect(database)
        self.cursor = self.connect.cursor()
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS kullanicilar (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        kullanici_adi TEXT UNIQUE,
        sifre TEXT
    )
""")
        self.connect.commit()

    def UsersInput(self, username, password):
        try:
            self.cursor.execute("INSERT INTO kullanicilar (kullanici_adi,sifre) VALUES (?,?)", (username,password))
            self.connect.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        
    def KullaniciDogrula(self, username, password):
        self.cursor.execute("SELECT * FROM kullanicilar WHERE kullanici_adi=? AND sifre=?", (username,password))
        return self.cursor.fetchone() is not None
    
    def GetAllUsers(self):
        self.cursor.execute("SELECT id, kullanici_adi FROM kullanicilar")
        return self.cursor.fetchall()
    
    def KullaniciSil(self, username):
        self.cursor.execute("DELETE FROM kullanicilar WHERE kullanici_adi=?", (username,))
        self.connect.commit()
        return self.cursor.rowcount > 0
   
    def PasswordHashing(password):
        return hashlib.sha256(password.encode()).hexdigest()
    

class KullaniciPanel():
    def __init__(self):
        self.database = Veritabani()
        self.login = False

    def KullaniciKayit(self):
        print("-"*65)
        username = GetInput("Kullanıcı Adınız: ")
        password = GetInput("Şifreniz: ")
        password_hash = Veritabani.PasswordHashing(password)
        if self.database.UsersInput(username,password_hash):
            PrintInfo("Kayıt Yapılıyor, Lütfen Bekleyin..")
            time.sleep(3)
            PrintSuccess("Kayıt İşlemi Tamamlandı!")
        else:
            PrintError("Kullanıcı Adı Mevcut.")

        print("-"*65)
        CalismaSuresi()
        
    def KullaniciGiris(self):
        print("-"*65)
        username = GetInput("Kullanıcı Adınız: ")
        password = GetInput("Şifreniz: ")
        password_hash = Veritabani.PasswordHashing(password)
        if self.database.KullaniciDogrula(username,password_hash):
            PrintInfo("Lütfen Bekleyin..")
            time.sleep(3)
            self.login = True
            PrintSuccess("Giriş Başarılı!")
        else:
            PrintError("Kullanıcı Adı ve Şifre Yanlış.")

        print("-"*65)
        CalismaSuresi()

    def Login(self):
        if not self.login:
            PrintError("Bu işlemi yapmak için giriş yapmalısınız.")
            print("-"*65)
            return False
        return True

    def KullaniciBilgi(self):
        print("-"*65)
        if not self.Login():
            return CalismaSuresi()
        users = self.database.GetAllUsers()
        if users:
            table = [["ID","Kullanıcı Adı"]]
            table.extend(users)
            print(tabulate(table, headers="firstrow", tablefmt="grid"))
        else:
            PrintError("Kayıtlı Kullanıcı Bulunamadı.")

        print("-"*65)
        CalismaSuresi()


    def KullaniciSil(self):
        print("-"*65)
        if not self.Login():
            return CalismaSuresi()
        username = GetInput("Silmek istediğiniz kullanıcı adı: ")
        PrintInfo("Kullanıcı Kontrol Ediliyor..")
        time.sleep(1)
        if self.database.KullaniciSil(username):
            PrintInfo("Kullanıcı Siliniyor, Lütfen Bekleyin..")
            time.sleep(2)
            PrintSuccess("Kullanıcı başarıyla silindi.")
        else:
            PrintError("Kullanıcı bulunamadı veya işlem başarısız oldu.")

        print("-"*65)
        CalismaSuresi()


def AnaMenu():
    ana_menu = KullaniciPanel()
    while True:
        ClearScreen()
        PrintBanner()
        PrintMenu()
        islem = GetInput("İşleminiz: ")
        if islem == "1":
            print("-"*65)
            PrintInfo("Lütfen bekleyin..")
            time.sleep(2)
            ana_menu.KullaniciKayit()
        elif islem == "2":
            print("-"*65)
            PrintInfo("Lütfen bekleyin..")
            time.sleep(2)
            ana_menu.KullaniciGiris()
        elif islem == "3":
            print("-"*65)
            PrintInfo("Lütfen Bekleyin..")
            time.sleep(2)
            ana_menu.KullaniciBilgi()
        elif islem == "4":
            print("-"*65)
            PrintInfo("Lütfen Bekleyin..")
            time.sleep(2)
            ana_menu.KullaniciSil()
        elif islem == "5":
            PrintInfo("Çıkış yapılıyor..")
            time.sleep(1)
            break
        else:
            PrintError("Geçersiz seçim, lütfen tekrar deneyin..")

if __name__ == "__main__":
    AnaMenu()
