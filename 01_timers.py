import sys
from PyQt5.QtWidgets import QPushButton, QApplication

class CounterButton(QPushButton):
    '''Simple button widget that counts number of times clicked.'''
    def __init__(self, initval=0, **kwargs):
        super().__init__(**kwargs)
        self._counter = initval
        self.setText('Clicks: {}'.format(self._counter))

    def mouseReleaseEvent(self, event):
        self._counter = self._counter + 1
        self.setText('Clicks: {}'.format(self._counter))
        super().mouseReleaseEvent(event)

#
# In this warmup exercise you will work with QTimers and this simple
# CounterButton implementation.
#
# 1. Implement a simple QApplication that uses the CounterButton
#    class. Make a layout that contains a few CounterButtons (say, 5)
#    and displays them.
#    
# 2. Now, set up a QTimer that, once every two seconds, *subtracts* 1
#    from the click count of the CounterButton. Observe the behavior
#    of your application.
#

