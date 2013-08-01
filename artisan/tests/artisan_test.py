# stdlib
from unittest import TestCase
import os
import urllib
import socket
import shutil

# module
from artisan.artisan import Artisan


class ApiTest(TestCase):

    #
    # Create new artisan & cache a few paths
    #
    @classmethod
    def setUpClass(self):
        # root directories
        self.execDir    = os.path.join(os.getcwd(), 'artisan/tests/emails')
        self.srcDir     = os.path.join(self.execDir, 'dev')
        self.devDir     = os.path.join(self.execDir, 'dev')

        # cache a couple of these paths for later use
        self.srcMaster  = os.path.join(self.srcDir, 'masters/01')
        self.srcMessage = os.path.join(self.srcDir, 'messages/success')
        self.devMaster  = os.path.join(self.devDir, 'masters/01')
        self.devMessage = os.path.join(self.devDir, 'messages/success')

        # init artisan
        self.artisan = Artisan(cwd=self.execDir)
        self.artisan.build()


    #
    # Remove build dir (dev)
    #
    @classmethod
    def tearDownClass(self):
        self.artisan.process.kill()
        shutil.rmtree(self.devDir)


    #
    # See if template was written to file system
    #
    def test_write(self):
        filePath = os.path.join(self.devMessage, 'index.html')
        self.assertTrue(os.path.isfile(filePath))


    #
    # 
    #
    def test_server(self):
        self.artisan.serve()
        status = urllib.urlopen("http://localhost:8080/messages/success/index.html").getcode()
        self.assertEqual(status, 200)

    # #
    # # See if images were coppied from src to dev
    # #
    # def test_sync(self):
        


    # #
    # # Test to see if style were moved inline
    # #
    # def test_premailer(self):
        


if __name__ == '__main__':
    unittest.main()