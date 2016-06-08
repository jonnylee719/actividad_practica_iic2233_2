#!/usr/bin/env python
#-*- coding:utf-8 -*-

from PyQt4 import QtCore, QtGui
import datetime
import pickle
import os
import functools as func

# Usted debe:
# Escribir la clase Cliente
# Completar el método 'serializarCliente' de la clase 'VentanaCajero'
# Completar el método 'generarArchivo' de la clase 'VentanaAdmin'
# Completar el método 'on_pushButton_clicked' de la clase 'Input'

class Cliente:
    def __init__(self, nombre, _id, dinero):
        self.nombre = nombre
        self._id = _id
        self.dinero = dinero

    def __setstate__(self, _dict):
        self.__dict__ = _dict

    def __getstate__(self):
        state = self.__dict__.copy()
        return state

    def __eq__(self, obj):
        if not obj:
            return False
        if not isinstance(obj, Cliente):
            return False
        if obj.nombre != self.nombre:
            return False
        if obj._id != self._id:
            return False
        if obj.dinero != self.dinero:
            return False
        return True

    def __repr__(self):
        print(self.__dict__)
        return 'Cliente id: {s} \nNombre: {c.nombre} \nGastado: {c.dinero}'\
            .format(s=123, c=self)

class VentanaCajero(QtGui.QDialog):

    def __init__(self, parent=None, username=""):
        super(VentanaCajero, self).__init__(parent)

        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok)

        self.clienteLabel = QtGui.QLabel("Nombre cliente", self)
        self.clienteText = QtGui.QLineEdit(self)
        self.idLabel = QtGui.QLabel("RUT", self)
        self.idText = QtGui.QLineEdit(self)
        self.gastadoLabel = QtGui.QLabel("Gastado", self)
        self.gastadoText = QtGui.QLineEdit(self)

        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.verticalLayout.addWidget(self.clienteLabel)
        self.verticalLayout.addWidget(self.clienteText)
        self.verticalLayout.addWidget(self.idLabel)
        self.verticalLayout.addWidget(self.idText)
        self.verticalLayout.addWidget(self.gastadoLabel)
        self.verticalLayout.addWidget(self.gastadoText)
        self.verticalLayout.addWidget(self.buttonBox)

        self.buttonBox.accepted.connect(self.serializarCliente)
        self.buttonBox.rejected.connect(self.close)

    def serializarCliente(self):
        fnames = os.listdir('ClientesDB')
        print('Files: \n{}'.format(fnames))
        existentes = {fn.split('.')[0]: fn for fn in fnames}

        nombre = self.clienteText.text()
        _id = self.idText.text()
        gastado = self.gastadoText.text()
        if not nombre or not _id or not gastado:
            # si no tiene texto en cualquier edit text, no hace nada
            return
        nueva_entrada = Cliente(nombre, _id, gastado)
        existe = False
        if _id in existentes:
            # cliente ya esta en la carpeta
            fname = 'ClientesDB' + os.sep + existentes[_id]
            with open(fname, 'rb') as file:
                cliente = pickle.load(file)
                print(cliente)
                if nueva_entrada == cliente:
                    existe = True
                    # actualiza el dinero con nuevo gasto
                    nueva_entrada.dinero += cliente.dinero
            print(cliente)
        if not existe:
            fname = 'ClientesDB' + os.sep + _id + '.walkcart'
        # actualiza el cliente y pickle dump el cliente
        with open(fname, 'wb') as file:
            print('Actualiza cliente archivo')
            pickle.dump(nueva_entrada, file)
        self.clienteText.setText("")
        self.idText.setText("")
        self.gastadoText.setText("")


class VentanaAdmin(QtGui.QDialog):

    def __init__(self, parent=None):
        super(VentanaAdmin, self).__init__(parent)

        self.archivoButton = QtGui.QPushButton("TOP-LIST")
        self.archivoButton.clicked.connect(self.generarArchivo)

        self.cancelButton = QtGui.QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.close)

        self.horizontalLayout = QtGui.QVBoxLayout(self)
        self.horizontalLayout.addWidget(self.archivoButton)
        self.horizontalLayout.addWidget(self.cancelButton)

    def generarArchivo(self):

        #####

        # Completar

        #####
        pass


class Input(QtGui.QWidget):

    def __init__(self, parent=None):
        super(Input, self).__init__(parent)

        self.userNameText = QtGui.QLineEdit(self)

        self.pushButtonWindow = QtGui.QPushButton(self)
        self.pushButtonWindow.setText("Iniciar Sesión")
        self.pushButtonWindow.clicked.connect(self.on_pushButton_clicked)

        self.layout = QtGui.QHBoxLayout(self)
        self.layout.addWidget(self.userNameText)
        self.layout.addWidget(self.pushButtonWindow)

    @QtCore.pyqtSlot()
    def on_pushButton_clicked(self):
        # abrir el archivo 'cajeros.walkcart'
        with open('cajeros.walkcart', 'rb') as file:
            cajeros_lista = pickle.load(file)
            print(cajeros_lista)
            # Chaquear el texto en el widget self.userNameText
            nombre = self.userNameText.text()
            if nombre in cajeros_lista:
                self.window = VentanaCajero()
                self.window.show()


if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('Log-in WM')

    main = Input()
    main.show()

    sys.exit(app.exec_())
