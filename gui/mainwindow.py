from PyQt4.QtCore import Qt
from PyQt4.QtGui import QAction, QActionGroup, QFileDialog, QIcon, QKeySequence, QMainWindow, QMenu, QMenuBar, QToolBar

from core.config import Config
from .view import View


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle('Yabai')

        QIcon.setThemeName('oxygenNOT') # TEST
        if not QIcon.hasThemeIcon('document-open'):
            QIcon.setThemeSearchPaths(['gui/icons'])
            QIcon.setThemeName('oxygen_parts')
        # TODO: This way of checking for the theme's existence is ugly
        # as fuck, so you'd better think of a better way to do it.

        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()

        for action in Config.checkedActions:
            if action in View.fitModes:
                fitMode = action
                break
        else:
            fitMode = 'view_fitBest'

        self.view = View('core/black.ori', fitMode)
        self.setCentralWidget(self.view)

        # Add all the action to the view, so that they can be
        # triggered even when there are no menus/toolbars
        # visible as it is in fullscreen mode:
        for action in self.actions.values():
            if not isinstance(action, QActionGroup):
                self.view.addAction(action)

        self.show()


    def createActions(self):

        actions = (
            # (key, text, icon, tooltip,
            #  action, shortcut
            #  group, flags)

            # Note: Having key==group defines a group.

            ('view_fileOpen', 'Open', '', 'document-open',
             lambda: self.view.openFile(QFileDialog.getOpenFileName()) , None,
             None, ()),

            ('view_fitMode', '', '', '',
             None, None,
             'view_fitMode', ('exclusive')),

            ('view_fitBest', 'Best Fit', '', 'zoom-fit-best',
             lambda: self.view.setFitMode('view_fitBest'), None,
             'view_fitMode', ('checkable')),

            ('view_fitWidth', 'Fit Width', '', 'zoom-fit-width',
             lambda: self.view.setFitMode('view_fitWidth'), None,
             'view_fitMode', ('checkable')),

            ('view_fitHeight', 'Fit Height', '', 'zoom-fit-height',
             lambda: self.view.setFitMode('view_fitHeight'), None,
             'view_fitMode', ('checkable')),

            ('view_fitSize', 'Original Size' , '', 'zoom-original',
             lambda: self.view.setFitMode('view_fitSize'), None,
             'view_fitMode', ('checkable')),

            ('view_previous', 'Previous page', '', 'go-previous-view',
             lambda: self.view.previousPage(), 'Left',
             None, ()),

            ('view_next', 'Next page', '', 'go-next-view',
             lambda: self.view.nextPage(), 'Right',
             None, ()),

            ('toggleFullscreen', 'Fullscreen', '', 'view-fullscreen',
             lambda: self.toggleFullscreen(), 'F',
             None, ('checkable'))
        )

        self.actions = {}
        for key, text, tooltip, icon, action, shortcut, group, flags in actions:
            if key == group:
                self.actions[key] = QActionGroup(self)
                if 'exclusive' in flags:
                    self.actions[key].setExclusive(True)
            else:
                self.actions[key] = QAction(self.tr(text), self if not group else self.actions[group], triggered=action)
                if icon: self.actions[key].setIcon(QIcon.fromTheme(icon))
                if shortcut: self.actions[key].setShortcut(QKeySequence(self.tr(shortcut)))
                if 'checkable' in flags:
                    self.actions[key].setCheckable(True)
                    if key in Config.checkedActions:
                        self.actions[key].setChecked(True)


    def createMenus(self):

        menus = (
            ('File',
                 ('view_fileOpen',)),
            ('View',
                ('view_fitBest',
                 'view_fitWidth',
                 'view_fitHeight',
                 'view_fitSize',
                 'toggleFullscreen')),
            ('Go',
                ('view_previous',
                 'view_next'))
        )

        def generate(menus, menuObject):
            for voice in menus:
                if isinstance(voice, tuple):
                    generate(voice[1], menuObject.addMenu(self.tr(voice[0])))
                else:
                    if not voice:
                        menuObject.addSeparator()
                    else:
                        menuObject.addAction(self.actions[voice])
        generate(menus, self.menuBar())


    def createToolBars(self):

        toolbars = (
            ('File',
                ('view_fileOpen',)),
            ('View',
                ('view_fitBest',
                 'view_fitWidth',
                 'view_fitHeight',
                 'view_fitSize',
                 'toggleFullscreen')),
            ('Go',
                ('view_previous',
                 'view_next'))
        )

        self.toolBars = []
        for toolbar, buttons in toolbars:
            toolbarObject = self.addToolBar(self.tr(toolbar))
            for button in buttons:
                if not button:
                    toolbarObject.addSeparator()
                else:
                    toolbarObject.addAction(self.actions[button])
            self.toolBars.append({'toolbar': toolbarObject,
                                  'visibility': False})
            # { toolbar object, visibility "backup" flag }
            # The flag is needed to save the current toolbars'
            # states when the application goes fullscreen.
            # Starts as False so when the fullscreen is toggled
            # for the first time they hide.


    def createStatusBar(self):
        pass


    def toggleFullscreen(self):

        self.setWindowState(self.windowState() ^ Qt.WindowFullScreen)
        self.menuBar().setVisible(not self.menuBar().isVisible())
        for toolbar in self.toolBars:
            currentVisibility = toolbar['toolbar'].isVisible()
            toolbar['toolbar'].setVisible(toolbar['visibility'])
            toolbar['visibility'] = currentVisibility
