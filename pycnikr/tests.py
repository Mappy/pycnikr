from django.test import TestCase

class PycnikrTests(TestCase):

    example_path = '/srv/pycnikr/pycnikr/style_sheets/example.py'

    def test_home(self):
        response = self.client.get('')
        self.assertIn('example', response.content)
        self.assertIn('example2', response.content)

    def test_template(self):
        response = self.client.get('/example')
        self.assertIn('container', response.content)

    def test_save(self):
        with open(self.example_path) as fd:
            example = fd.read()
        try:
            response = self.client.post('/save/example',
                                        data=example,
                                        content_type='application/octet-stream')
            self.assertEquals('Style sheet successfully saved',
                              response.content)
        except:
            raise
        finally:
            with open(self.example_path, 'w') as fd:
                fd.write(example)


    def test_preview(self):
        with open(self.example_path) as fd:
            example = fd.read()
        response = self.client.post('/preview/example',
                                    data=example,
                                    content_type='application/octet-stream')
        self.assertEquals('Style sheet successfully applied', response.content)

