import unittest
import main
import os


class TestCorrector(unittest.TestCase):
    def setUp(self):
        self.file = '19242871-8_bernardita_pineda'
        self.nota = 6.0
        self.palabras = ['bb']
        self.crear_archivo(self.file, self.nota, self.palabras)
        self.test_corr = main.Corrector(self.file)

    def crear_archivo(self, fname, nota, palabras):
        f = open('Trabajos/' + fname, 'w')
        print('{0}'.format(nota), file=f)
        print(' '.join(palabras), file=f)
        f.close()

    def tearDown(self):
        if self.file is not None:
            os.remove('Trabajos/' + self.file)

    def test_revisar_formato_no_tiene_txt(self):
        # formato que no tiene el string 'txt'
        formato = ''
        self.assertFalse(self.test_corr.revisar_formato(formato),
                        'Debe retorna False si no tiene "txt"')

    def test_revisar_formato_ttxtt(self):
        # formato que tiene substring "txt"
        formato = 'txtt'
        self.assertFalse(self.test_corr.revisar_formato(formato),
                         'Debe retorna False porque "txt" es un substring')

    def test_revisar_formato_txt(self):
        formato = 'txt'
        self.assertTrue(self.test_corr.revisar_formato(formato),
                        'Debe retorna True')

    def test_revisar_verificador_formato_incorrecto(self):
        '''
        if not rut[:-2].isdigit():
            return False
        revisar_verificador puede recibir un rut mal formato porque solamente
        verificar rut[:-2] no es digito
        '''
        rut_mal_formato = '192428721--8'
        self.assertFalse(self.test_corr.revisar_verificador(rut_mal_formato),
                        'Debe retorna Falso por el mal formato del RUT: {0}'
                         .format(rut_mal_formato))

    def test_revisar_verificador_correcto(self):
        rut_correcto = '19242871-8'
        self.assertTrue(self.test_corr.revisar_verificador(rut_correcto),
                        'Debe retorna True por rut: {0}'.format(rut_correcto))

    def test_revisar_verificador_falso(self):
        rut_falso = '19242872-8'
        self.assertFalse(self.test_corr.revisar_verificador(rut_falso),
                        'Debe retorna False por rut: {0}'.format(rut_falso))

    def test_revisar_orden_correcto(self):
        corr = '11939010-k_Andrea_Valdes'
        self.assertTrue(self.test_corr.revisar_orden(corr),
                        'Debe retorna True por el formato: {0}'.format(corr))

    def test_revisar_orden_nombre_no_existe(self):
        nombre = '11293099-0_Jon_Lee'
        self.assertFalse(self.test_corr.revisar_orden(nombre),
                        'Debe retorna False por el nombre no existe: {0}'
                        .format(nombre))

    def test_revisar_orden_empty_string(self):
        archivo = ''
        self.assertFalse(self.test_corr.revisar_orden(archivo),
                         'Debe retorna False por el nombre no existe: {0}'
                         .format(archivo))

    def test_revisar_orden_archivo_mal_formato(self):
        archivo = '11923192-k__Jon'
        self.assertFalse(self.test_corr.revisar_orden(archivo),
                         'Debe retorna False por el mal formato {0}'
                         .format(archivo))

    def test_revisar_orden_archivo_mal_formato_dos(self):
        archivo = '11923192-k__Jon_Lee'
        self.assertFalse(self.test_corr.revisar_orden(archivo),
                         'Debe retorna False por el mal formato {0}'
                         .format(archivo))

    def test_descontar_no_descuento(self):
        # Set descuento 0
        setattr(main.Corrector, 'descuento', 0)
        self.test_corr.descontar()
        self.assertTrue(self.check_archivo(self.file, self.nota))

    def test_descontar_zero_con_cinco(self):
        # Set descuento 0.5
        setattr(main.Corrector, 'descuento', 0.5)
        self.test_corr.descontar()
        self.assertTrue(self.check_archivo(self.file, self.nota - 0.5))

    def test_descontar_uno(self):
        # Set descuento 0.5
        setattr(main.Corrector, 'descuento', 1)
        self.test_corr.descontar()
        self.assertTrue(self.check_archivo(self.file, self.nota - 1))

    def test_get_palabras_una_palabra(self):
        string = '6.0\npalabra1 '
        contenido = list(map(lambda o : o.strip(), string.split('\n')))
        setattr(main.Corrector, 'contenido', contenido)
        self.assertEqual(self.test_corr.palabras, 1)

    def test_get_palabras_500_palabras(self):
        palabras = [str(i) for i in range(0, 500)]
        string = '6.0\n{0}'.format(' '.format(palabras))
        contenido = list(map(lambda o : o.strip(), string.split('\n')))
        setattr(main.Corrector, 'contenido', contenido)
        self.assertEqual(self.test_corr.get_palabras(), len(palabras))

    def test_get_descuento_no_descuento(self):
        # Revisar nombre is True
        setattr(main.Corrector, 'revisar_nombre', lambda x: True)
        setattr(main.Corrector, 'palabras', 500)
        self.assertEqual(self.test_corr.get_descuento(), 0)

    def test_get_descuento_falso_nombre(self):
        setattr(main.Corrector, 'revisar_nombre', lambda x: False)
        setattr(main.Corrector, 'palabras', 500)
        self.assertEqual(self.test_corr.get_descuento(), 0.5)

    def test_get_descuento_menor_que_500(self):
        setattr(main.Corrector, 'revisar_nombre', lambda x: True)
        setattr(main.Corrector, 'palabras', 400)
        self.assertEqual(self.test_corr.get_descuento(), 1)

    def test_get_descuento_mas_que_500(self):
        setattr(main.Corrector, 'revisar_nombre', lambda x: True)
        setattr(main.Corrector, 'palabras', 501)
        self.assertEqual(self.test_corr.get_descuento(), 1,
                         'Debe tener descuento por no cumple 500 palabras')

    def test_revisar_nombre_bien_formato(self):
        bien_formato = '19242871-8_bernardita_pineda'
        setattr(main.Corrector, 'nombre', bien_formato)
        self.assertTrue(self.test_corr.revisar_nombre())

    def test_revisar_nombre_mal_formato(self):
        bien_formato = '19242871-8bernardita_pineda'
        setattr(main.Corrector, 'nombre', bien_formato)
        self.assertFalse(self.test_corr.revisar_nombre())

    def check_archivo(self, fname, nota):
        f = open('Trabajos/' + fname, 'r')
        lines = f.readlines()
        # first line is the note should be equal to nota
        equal = False
        try:
            f_note = float(lines[0].strip())
            equal = (f_note == nota)
        except ValueError as ve:
            print('Error: {0}'.format(ve))
        f.close()
        return equal



tsuite = unittest.TestLoader().loadTestsFromTestCase(TestCorrector)
unittest.TextTestRunner().run(tsuite)