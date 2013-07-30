# *-* coding: utf-8 *-*

from PySide import QtGui


class RawAnalyzer(object):

    def __init__(self, parent=None):
        self.Wdg = parent
        self.DBMS = ''
        self.QtdDBs = 0
        self.DBNames = []
        self.QtdTBs = 0
        self.Info = self.Wdg.Info
        self.TabData = self.Wdg.tabData

    def getDBInfo(self):
        self.Info.appendPlainText('[INFO]Getting Database information...')
        self.DBMS = self.getDBMS()
        if self.DBMS is False:
            self.Info.appendPlainText('''[ERROR]Failed to find Database
                information!!!\n
                [ERROR]Please, check if this site is vulnerable and see the raw
                data for more information.''')
            return
        else:
            self.Info.appendPlainText('''[INFO] %s DBMS was found'''
            % (self.DBMS))
        self.QtdDBs = self.getDatabases()
        if self.QtdDBs == 0:
            self.Info.appendPlainText('''[Warning] Failed to count databases\n
                [Warning]See the raw data to check if was found some database
                this analyze is not goig to work.\n
                [Warning]Please, restart''')
            return
        else:
            self.Info.appendPlainText('''[INFO] %d databases were found'''
                % (self.QtdDBs))
        self.DBNames = self.getDBNames()
        for i in range(self.QtdDBs):
            Out = '[INFO]\t Database '
            Out += str(i) + ': '
            Out += self.DBNames[i]
            self.Info.appendPlainText(Out)
        for D in self.DBNames:
            self.TabData.addDB(D)
        self.Info.appendPlainText('[INFO]Databases scanning complete!')
        self.Wdg.tabWidget.setCurrentIndex(2)

    def getDBNames(self):
        DBNames = []
        Edt = self.Wdg.RawData
        Cursor = QtGui.QTextCursor()
        for DB in range(self.QtdDBs):
            Edt.find('[*]')
            Edt.moveCursor(Cursor.StartOfLine)
            Edt.moveCursor(Cursor.EndOfLine, Cursor.KeepAnchor)
            Text = Edt.textCursor().selectedText()
            Text = Text.split()
            Text = Text[-1]
            DBNames.append(str(Text))
        return DBNames

    def getDatabases(self):
        QtdDBs = 0
        Edt = self.Wdg.RawData
        Cursor = QtGui.QTextCursor()
        Edt.find('available databases')
        Edt.moveCursor(Cursor.StartOfLine)
        Edt.moveCursor(Cursor.EndOfLine, Cursor.KeepAnchor)
        Text = Edt.textCursor().selectedText()
        Text = Text.split()
        Text = Text[-1]
        QtdDBs = Text[1]
        QtdDBs = int(QtdDBs)
        return (QtdDBs)

    def getDBMS(self):
        Edt = self.Wdg.RawData
        Cursor = QtGui.QTextCursor()
        Edt.moveCursor(Cursor.Start)
        Edt.find('[INFO] the back-end DBMS is')
        Edt.moveCursor(Cursor.StartOfLine)
        Edt.moveCursor(Cursor.EndOfLine, Cursor.KeepAnchor)
        Text = Edt.textCursor().selectedText()
        Text = Text.split()
        #if cant find dbms, return false to after check this error
        if len(Text) > 0:
            return(Text[-1])
        else:
            return False

    def AnalyzeTables(self, DB):
        self.QtdTBs = self.getQtdTable(DB)
        if self.QtdTBs is False:
            self.Info.appendPlainText('''[ERROR]Failed to find database tables.
                [ERROR]See the raw data for more information.
                [ERROR]Please restart the analyze.''')
        else:
            self.Info.appendPlainText('[INFO]%s tables was found on database %s'
                 % (self.QtdTBs, DB))

    def getQtdTable(self, DB):
        Edt = self.Wdg.RawData
        Cursor = QtGui.QTextCursor()
        a = Edt.find('Database: ' + DB)
        if a is False:
            return False
        a = Edt.find('[')
        if a is False:
            return False
        Edt.moveCursor(Cursor.StartOfLine)
        Edt.moveCursor(Cursor.EndOfLine, Cursor.KeepAnchor)
        Text = Edt.textCursor().selectedText()
        Text = Text.split()
        Text = Text[0]
        Text = Text[1:]
        if len(Text) < 2:
            return False
        else:
            return(int(Text))

