import unittest
from subject import *
from PyOptHogaMonSimul import *



class optChartTest(unittest.TestCase):
    """
    Documentation for a class.

    More details
    this class is for test of optChart manager functions which gathers the information of hoga, and contract of option   
    from RC event
    """ 

    def test_optChartMemberCheck(self):
        """
        this function is for the test that whether the inserted item in optChart is correct.
        """
        self.optdata = OptData() 
        self.optdata.change_optprice("091213", "201P3450", "3.0", "4.0", "")
        c = self.optdata.get_optChart()
        self.assertEqual(c["201P3450"]["hogaTime"], "091213")
        self.assertEqual(c["201P3450"]["offerho1"], "3.0")
        self.assertEqual(c["201P3450"]["bidho1"], "4.0") #item comparison
    
    
    def test_optChartInsersion(self):
        """
        this functino is for the test that whether several options gathered in optChart is properly inserted or deleted intentionally
        """
        self.optdata = OptData()
        self.optdata.change_optprice("091215", "201P3650", "3.0", "4.0", "")
        self.optdata.change_optprice("091213", "201P3450", "5.0", "4.0", "")
        self.optdata.change_optprice("091220", "201C3850", "10.0", "8.0", "")
        c = self.optdata.get_optChart()
        #print(c)
        self.assertEqual(c["201P3650"]["offerho1"], "3.0")
        self.assertEqual(len(c), 3)  #dictionary size comparison
        del self.optdata.get_optChart()["201P3650"]
        c = self.optdata.get_optChart()
        #print(c)
        self.assertEqual(len(c), 2)

        
class HogaMonSimulTest(unittest.TestCase):
    
    def test_dataload(self):
        self.optmon = PyOptHogaMonSimul.get_instance()
        c = self.optmon.getSampleSize()
        #print(c)
        self.assertEqual(c,0)

if __name__ == '__main__':
    unittest.main()