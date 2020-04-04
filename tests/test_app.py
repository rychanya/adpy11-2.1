
import app
from unittest import TestCase
from unittest.mock import patch


class TestApp(TestCase):

    def setUp(self):
        self.dirs = {
                "1": ["2207 876234", "11-2"],
                "2": ["10006"],
                "3": []
            }
        self.docs = [
                {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
                {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
                {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"}
            ]
        with patch('app.update_date', return_value=(self.dirs, self.docs)):
            app.prepare_date()

    def test_check_document_existance(self):
        self.assertTrue(app.check_document_existance('11-2'))

        self.assertFalse(app.check_document_existance('not exs'))

    def test_get_doc_owner_name(self):
        with patch('app.input', return_value='11-2'):
            self.assertEqual(app.get_doc_owner_name(), 'Геннадий Покемонов')

        with patch('app.input', return_value='not exs'):
            self.assertIsNone(app.get_doc_owner_name())

    def test_get_all_doc_owners_names(self):
        self.assertEqual(app.get_all_doc_owners_names(), set([doc['name'] for doc in self.docs]))

    def test_remove_doc_from_shelf(self):
        self.assertIn('11-2', app.directories['1'])

        app.remove_doc_from_shelf('not exs')
        self.assertDictEqual(app.directories, self.dirs)

        app.remove_doc_from_shelf('11-2')
        self.assertNotIn('11-2', app.directories['1'])

    def test_add_new_shelf(self):
        shelf_before = list(app.directories.keys())
        self.assertTrue(shelf_before)

        self.assertTupleEqual(app.add_new_shelf(shelf_before[0]), (shelf_before[0], False))

        new_shelf = 'new'
        with patch('app.input', return_value=new_shelf):
            self.assertTupleEqual(app.add_new_shelf(), (new_shelf, True))

    def test_append_doc_to_shelf(self):
        doc, shelf = 'new doc', '3'

        self.assertNotIn(doc, app.directories[shelf])

        app.append_doc_to_shelf(doc, shelf)
        self.assertIn(doc, app.directories[shelf])

    def test_delete_doc(self):
        with patch('app.input', return_value='not exs'):
            self.assertIsNone(app.delete_doc())

        doc_to_del = '11-2'
        with patch('app.input', return_value=doc_to_del):
            self.assertTupleEqual(app.delete_doc(), (doc_to_del, True))
            for shelf in app.directories.values():
                self.assertNotIn(doc_to_del, shelf)
            self.assertNotIn(doc_to_del, [doc['number'] for doc in app.documents])

    def test_get_doc_shelf(self):
        with patch('app.input', return_value='not exs'):
            self.assertIsNone(app.get_doc_shelf())

        with patch('app.input', return_value='11-2'):
            self.assertEqual(app.get_doc_shelf(), '1')

    def test_move_doc_to_shelf(self):
        doc = '11-2'
        new_shelf = '3'
        old_shelf = '1'

        self.assertIn(doc, app.directories[old_shelf])
        self.assertNotIn(doc, app.directories[new_shelf])

        with patch('app.input', side_effect=[doc, new_shelf]), patch('app.print'):
            app.move_doc_to_shelf()

        self.assertNotIn(doc, app.directories[old_shelf])
        self.assertIn(doc, app.directories[new_shelf])

    def test_add_new_doc(self):
        new_doc_number = '56666'
        new_doc_type = 'pass'
        new_doc_owner_name = 'owner'
        new_doc_shelf_number = '3'

        with patch('app.input', side_effect=[new_doc_number, new_doc_type, new_doc_owner_name, new_doc_shelf_number]):
            self.assertEqual(app.add_new_doc(), new_doc_shelf_number)

        self.assertIn(new_doc_number, app.directories[new_doc_shelf_number])
        self.assertIn(new_doc_number, [doc['number'] for doc in app.documents])
