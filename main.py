import Levenshtein
import os
import urwid

def walkFiles(baseDir):
    '''Find absolute paths of files that are descendants of baseDir'''
    filePaths = []
    for dirPath, dirNames, fileNames in os.walk(baseDir):
        for fileName in fileNames:
            filePaths.append(os.path.join(dirPath, fileName))
    return filePaths

def isSubsequence(p, s):
    '''Is p a subsequence of s'''
    i = 0
    j = 0
    while i < len(p) and j < len(s):
        while j < len(s) and p[i] != s[j]:
            j += 1
        i += 1
    return j < len(s)

class FileFinder:
    '''Find files and try to match them with a given pattern'''
    def __init__(self, baseDir):
        self._filePaths = walkFiles(baseDir)
        self._partialLine = ''

    def addFilePaths(self, s):
        s = self._partialLine + s
        lines = s.split(os.linesep)
        for i in range(len(lines)):
            if lines[i] == '':
                continue
            self._filePaths.append(lines[i])

    def _matchFiles(self, pattern):
        '''Find matching files

        A file matches if the pattern is a subsequence of one of its path
        components. Matches are sorted by increasing Levenshtein (edit)
        distance in the result list.'''
        matches = []
        for filePath in self._filePaths:
            for token in filePath.split(os.path.sep):
                if not isSubsequence(pattern, token):
                    continue
                matches.append((filePath, Levenshtein.distance(pattern, token)))
                break
        matches.sort(key=lambda m: m[1])
        return matches

    def __call__(self, pattern):
        return map(lambda m: m[0], self._matchFiles(pattern))

class FileFinderUI:
    '''The terminal UI is powered by urwid 

    It consists of an edit widget in which the user enters a pattern, and a
    list of buttons for the matching files. Selecting a file causes the UI to
    finish running and outputs the file path to stdout.'''
    def __init__(self, fileFinder):
        self._outputFilePath = ''
        self._fileFinder = fileFinder

    def _makePatternEdit(self, listbox, prompt='> '):
        def editHandler(edit, text):
            del listbox.body[2:]
            for filePath in self._fileFinder(text):
                listbox.body.append(self._makeFilePathButton(filePath))
        edit = urwid.Edit(prompt)
        urwid.connect_signal(edit, 'change', editHandler)
        return edit

    def _makeFilePathButton(self, label):
        def buttonHandler(button, label):
            self._outputFilePath = label
            raise urwid.ExitMainLoop()
        button = urwid.Button(label)
        urwid.connect_signal(button, 'click', buttonHandler, label)
        return button

    def _makeTopLevelListbox(self):
        listbox = urwid.ListBox(urwid.SimpleFocusListWalker([]))
        listbox.body += [
            self._makePatternEdit(listbox),
            urwid.Divider()
        ]
        return listbox

    def run(self):
        listbox = self._makeTopLevelListbox()
        mainLoop = urwid.MainLoop(listbox)
        try:
            mainLoop.run()
        except KeyboardInterrupt:
            pass
        print(self._outputFilePath)

if __name__ == '__main__':
    FileFinderUI(FileFinder(os.getcwd())).run()
