"""Menjalankan semua halaman KOSTAY (.ui) dengan alur navigasi.

Instal  : pip install PyQt5
Jalankan: python kostay_app.py
Letakkan file ini sekelompok dengan semua *.ui dan folder images/.
Alur    : login -> (User | Admin) -> menu sidebar -> logout -> login
"""
import os
import sys

from PyQt5 import QtWidgets, uic

BASE = os.path.dirname(os.path.abspath(__file__))

USER_NAV = {
    "btnUserDashboard": "user_dashboard", "btnUserKatalog": "user_katalog",
    "btnUserPenyewaan": "user_penyewaan", "btnUserPembayaran": "user_pembayaran",
    "btnUserNotifikasi": "user_notifikasi", "btnUserProfil": "user_profil",
    "btnUserLogout": "login",
}
ADMIN_NAV = {
    "btnAdminDashboard": "admin_dashboard", "btnAdminKamar": "admin_kamar",
    "btnAdminUser": "admin_user", "btnAdminValidasi": "admin_validasi",
    "btnAdminLaporan": "admin_laporan", "btnAdminNotif": "admin_notifikasi",
    "btnAdminLogout": "login",
}

# Tombol khusus per halaman: nama tombol -> halaman tujuan
EXTRA = {
    "register": {"btnDaftar": "login", "btnKembaliLogin": "login"},
    "user_dashboard": {"btnBayarTagihan": "user_pembayaran", "btnLihatRiwayat": "user_penyewaan"},
    "user_katalog": {**{f"btnDetail{i}": "user_detail_kamar" for i in range(1, 7)},
                     **{f"btnSewa{i}": "user_detail_kamar" for i in range(1, 7)}},
    "user_detail_kamar": {"btnKembali": "user_katalog", "btnSewaSekarang": "user_pembayaran"},
    "admin_dashboard": {"btnBukaValidasi": "admin_validasi"},
    "admin_kamar": {"btnTambahKamar": "admin_form_kamar", "btnEditKamar": "admin_form_kamar"},
    "admin_form_kamar": {"btnBatal": "admin_kamar", "btnSimpan": "admin_kamar"},
    "admin_user": {"btnTambahUser": "admin_form_user", "btnEditUser": "admin_form_user"},
    "admin_form_user": {"btnBatal": "admin_user", "btnSimpan": "admin_user"},
}


class Navigator:
    def __init__(self):
        self.windows = {}
        self.current = None

    def get(self, key):
        if key not in self.windows:
            win = uic.loadUi(os.path.join(BASE, key + ".ui"))
            self.windows[key] = win
            self.wire(key, win)
        return self.windows[key]

    def wire(self, key, win):
        links = {}
        if key.startswith("user_"):
            links.update(USER_NAV)
        if key.startswith("admin_"):
            links.update(ADMIN_NAV)
        links.update(EXTRA.get(key, {}))
        for btn_name, target in links.items():
            btn = win.findChild(QtWidgets.QPushButton, btn_name)
            if btn is not None:
                btn.clicked.connect(lambda _=False, t=target: self.go(t))
        if key == "login":
            win.btnLogin.clicked.connect(self.do_login)
            win.txtPassword.returnPressed.connect(self.do_login)
            win.btnRegister.clicked.connect(lambda: self.go("register"))

    def do_login(self):
        # TODO: ganti dengan AuthController.login(username, password)
        win = self.windows["login"]
        self.go("user_dashboard" if win.cmbRole.currentIndex() == 0 else "admin_dashboard")

    def go(self, key):
        win = self.get(key)
        if self.current is not None and self.current is not win:
            win.setGeometry(self.current.geometry())
            if self.current.isMaximized():
                win.showMaximized()
            self.current.hide()
        win.show()
        self.current = win


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    nav = Navigator()
    nav.go("login")
    sys.exit(app.exec_())
