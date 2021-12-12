import sys
from PyQt5.QtWidgets import QPushButton, QApplication, QMainWindow, QWidget, QGridLayout, QLineEdit, QLabel, QTabWidget

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

class ConfigPane(QGridLayout):
    '''Panel of configuration options. Buggy and not very featureful.'''
    def __init__(self, params, on_configure, **kwargs):
        '''The constructor takes a list of integer params of the form (NAME, DEFAULT).'''
        super().__init__(**kwargs)
        self._textinputs = {}

        # Iterate over all config parameters.
        for (i, (p, d)) in enumerate(params):
            # Make the label and add it.
            label = QLabel(text=p)
            self.addWidget(label, i, 0)
            
            # Save the textinput in a local dict so we can recover it by parameter *name*.
            self._textinputs[p] = QLineEdit(text=str(d))
            self.addWidget(self._textinputs[p], i, 1)

        # Add the reconfigure button, bind click to *user-provided*
        # on_configure callback. Messy.
        self._configbutton = QPushButton(text='Reconfigure')
        self._configbutton.clicked.connect(on_configure)
        self.addWidget(self._configbutton, len(params), 0, 1, 2)

    # This is a simple interface to let us get parameters by *name*
    # from outside this class.
    def get_param(self, p):
        '''Return the configuration parameter from the textinput with label p.'''
        return int(self._textinputs[p].text())

# Class to hold a grid of CounterButtons.            
class ButtonPane(QGridLayout):
    '''Widget that contains a number of CounterButtons arranged in a GridLayout.'''
    def __init__(self, num_buttons, cols=1, initval=0, **kwargs):
        super().__init__(**kwargs)

        # Logic to create a grid of CounterButtons in cols columns.
        for i in range(num_buttons):
            self.addWidget(CounterButton(initval=initval), i // cols, i % cols)
        
# The main application.
class TestApp(QApplication):
    '''The main application. The on_configure() method is called when the 'Reconfigure' button pressed on config pane.'''
    def __init__(self, args):
        # Root is a QTabWidget, first tab is ConfigPane, second a ButtonPane.
        super().__init__(args)
        self._root = QTabWidget()
        self._config = QWidget()
        self._buttons = QWidget()
        self._config.setLayout(ConfigPane(params=[('Columns', 2), ('Buttons', 10)], on_configure=self.on_configure))
        self._buttons.setLayout(ButtonPane(num_buttons=10, cols=2))
        self._root.addTab(self._config, 'Configuration')
        self._root.addTab(self._buttons, 'Buttons')
        self._root.setFixedSize(640, 480)
        self._root.show()
        self.exec_()

    # This is the callback we pass into the constructor of ConfigPane
    # so that it can call us back with the Reonfigure button is
    # pressed. Super messy.
    def on_configure(self):
        '''Callback for re-configure request on config pane.'''
        cols = self._config.layout().get_param('Columns')
        buttons = self._config.layout().get_param('Buttons')
        self._root.removeTab(1)
        self._buttons = QWidget()
        self._buttons.setLayout(ButtonPane(num_buttons=buttons, cols=cols))
        self._root.addTab(self._buttons, 'Buttons')

        

# Instantiate and run the application.
app = TestApp(sys.argv)

#
# The remaining exercises are based on this running example.
#
# 1. Take some time to make sure you understand *everything* about how
#    this application works. It is our first non-trivial example of a
#    PyQT5 Application, and your understanding of it will be essential
#    for the rest of the laboratory.
#
# 2. Create a new directory called 'RunningExample'. Copy this file
#    into this new folder and call it 'main.py'. Working in this new
#    directory, we will refactor this running example into a better
#    designed implementation.
#
#
# Part I: Improving CounterButton
# -------------------------------
#
# 3. In the RunningExample directory, copy the 'CounterButton' class
#    implementation into a file called 'counterbutton.py'. Change the
#    implementation to use as Observabel for the internal counter
#    instead of a bare field (like we saw in the lesson yesterday).
#
# 4. Change the 'main.py' file to use the new CounterButton class
#    implementation in 'counterbutton.py'.
# 
# 5. Implement a simple test program *inside* the 'counterbutton.py'
#    file that, when the file is *run* as a script, builds a simple
#    application with a stack of 5 CounterButtons. *HINT*: recall how
#    the __name__ guard is used to implement such functionality.
#
#
# Part II: Improving the ConfigPane implementation
# ------------------------------------------------
#
# 6. As before, copy the ConfigPane class implementation into a new
#    file called 'configpane.py'. Now change the implementation of
#    ConfigPane to use an *Observable* Python dict that maps *names*
#    of configuration parameters to their values (call this new
#    Observable 'configvals'). *NOTE*: you will have to change the
#    implementation of the 'get_param()' method to use this new
#    object. You might also think about implementing a set_param()
#    method... *hint* *hint*.
#
# 7. Add a callback 'on_configure' in the new ConfigPane
#    implementation that listens for clicks of the configure button
#    widget. In this callback, implement the logic to copy the text
#    values from the TextInput widgets into the configvals
#    Observable.
#
# 8. Finally, back in the main Application Class, bind a new callback
#    (call it on_configvals) to changes in 'configvals' in the
#    ConfigPane. In this callback, implement the logic to delete and
#    re-build the ButtonPane with the new configuration parameters.
#
# 
