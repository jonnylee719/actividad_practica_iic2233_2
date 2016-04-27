import unittest
import main


class TestCorrector(unittest.TestCase):
    def setUp(self):
        self.test_corr = main.Corrector('5435466-5_lucas_hidalgo.txt')

    def tearDown(self):
        pass

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

    def test_revisar_verificador_correcto(self):
        rut_correcto = '19242871-8'
        self.assertTrue(self.test_corr.revisar_verificador(rut_correcto),
                        'Debe retorna True por rut: {0}'.format(rut_correcto))

    def test_revisar_verificador_falso(self):
        rut_falso = '19242872-8'
        self.assertFalse(self.test_corr.revisar_verificador(rut_falso),
                        'Debe retorna False por rut: {0}'.format(rut_falso))

    def test_revisar_verificador_formato_incorrecto(self):
        rut_mal_formato = '192428721--8'
        self.assertFalse(self.test_corr.revisar_verificador(rut_mal_formato),
                        'Debe retorna Falso por rut: {0}'.format(rut_mal_formato))

    



tsuite = unittest.TestLoader().loadTestsFromTestCase(TestCorrector)
unittest.TextTestRunner().run(tsuite)