#!/usr/bin/env python
#-*- coding:utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from datetime import datetime
import pickle
import os
import functools as func
import json

# Usted debe:
# Escribir la clase Cliente
# Completar el método 'serializarCliente' de la clase 'VentanaCajero'
# Completar el método 'generarArchivo' de la clase 'VentanaAdmin'
# Completar el método 'on_pushButton_clicked' de la clase 'Input'

class Cliente:
    def __init__(self, ID, Nombre, GastoAcumulado, UltimaCompra=None):
        if UltimaCompra:
            assert isinstance(UltimaCompra, datetime)
        assert isinstance(ID, int)
        assert isinstance(GastoAcumulado, int)
        self.ID = ID
        self.Nombre = Nombre
        self.GastoAcumulado = GastoAcumulado
        self.UltimaCompra = UltimaCompra

    def __setstate__(self, _dict):
        if isinstance(_dict['UltimaCompra'], float):
            print("Setting time stamp")
            _dict['UltimaCompra'] = datetime.fromtimestamp(_dict['UltimaCompra'])
        # _dict['ID'] = int(_dict['ID'])
        # _dict['GastoAcumulado'] = int(_dict['GastoAcumulado'])
        self.__dict__ = _dict

    def __getstate__(self):
        state = self.__dict__.copy()
        if state['UltimaCompra']:
            state['UltimaCompra'] = datetime.now().timestamp()
        # state['ID'] = str(state['ID'])
        # state['GastoAcumulado'] = str(state['GastoAcumulado'])
        return state

    def to_json(self, fname=None):
        # change datetime to timestamp
        state = self.__dict__.copy()
        state['UltimaCompra'] = state['UltimaCompra'].timestamp()
        if fname:
            with open(fname, 'w') as file:
                json.dump(obj=state, fp=file)
        else:
            return json.dumps(state)

    @classmethod
    def from_json(cls, json_str=None, fname=None):
        if not json_str and not fname:
            raise ValueError
        if json_str:
            _dict = json.loads(json_str)
        elif fname:
            with open(fname, 'rb') as file:
                _dict = json.load(file)
        # change time stamp
        return cls(**_dict)

    def __eq__(self, obj):
        if not obj:
            return False
        if not isinstance(obj, Cliente):
            return False
        if obj.Nombre != self.Nombre:
            return False
        if obj.ID != self.ID:
            return False
        if obj.GastoAcumulado != self.GastoAcumulado:
            return False
        if obj.UltimaCompra != self.UltimaCompra:
            return False
        return True

    def __repr__(self):
        print(self.__dict__)
        return 'Cliente id: {c.ID} \nNombre: {c.Nombre} ' \
               '\nGastado: {c.GastoAcumulado} \nUltima Compra: {compra}'\
            .format(c=self, compra=self.UltimaCompra)

class VentanaCajero(QtGui.QDialog):

    def __init__(self, parent=None, username=""):
        super(VentanaCajero, self).__init__(parent)
        self.setWindowTitle(username)

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

        nombre = self.clienteText.text().strip()
        _id = self.idText.text().strip()
        gastado = self.gastadoText.text().strip()
        if not nombre or not _id or not gastado:
            # si no tiene texto en cualquier edit text, no hace nada
            return
        if not _id.isdigit() or not gastado.isdigit():
            return
        nueva_entrada = Cliente(Nombre=nombre, ID=int(_id), GastoAcumulado=int(gastado))
        existe = False
        if _id in existentes:
            # cliente ya esta en la carpeta
            fname = 'ClientesDB' + os.sep + existentes[_id]
            with open(fname, 'rb') as file:
                cliente = pickle.load(file)
                print(cliente)
                existe = True
                # actualiza el dinero con nuevo gasto
                cliente.GastoAcumulado += nueva_entrada.GastoAcumulado
                nueva_entrada = cliente
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
        fnames = os.listdir('ClientesDB')
        clientes = []
        for f in fnames:
            with open('ClientesDB' + os.sep + f, 'rb') as file:
                cliente = pickle.load(file)
                clientes.append(cliente)
        # sort by GastoAcumulado
        best_c = max(clientes, key=lambda c: c.GastoAcumulado)
        # save as json
        best_c.to_json('TOP.walkcart')
        print(best_c.to_json())


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
                self.window = VentanaCajero(username=nombre)
                self.window.show()
            elif nombre == 'WalkcartUnlimited':
                self.admin = VentanaAdmin()
                self.admin.show()


if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('Log-in WM')

    main = Input()
    main.show()

    sys.exit(app.exec_())
