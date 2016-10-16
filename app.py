import os
import re

class ExampleFile:
    def __init__(self, name):
        self.name = os.path.splitext(name)[0] # without '.txt'
        self.sentences = []
    def addSentence(self, text):
        self.sentences.append(text)
    def search(self, pattern):
        result = []
        for i in range(len(self.sentences)):
            if re.search(pattern, self.sentences[i], flags = re.IGNORECASE):
                result.append((i+1, self.sentences[i]))
        return result
    

class App:
    accents = {'a': ('a','à','â'),
               'e': ('e','é','è','ê','ë'),
               'u': ('u','ù','û','ü'),
               'y': ('y','ÿ'),
               'c': ('c','ç'),
               'i': ('i','ï','î'),
               'o': ('o','ô'),}
    
    def __init__(self, datadir = './examples', isWholeWord = True):
        self.datadir = datadir
        self.examples = []
        self.count = [0,0] # files, lines
        self.isWholeWord = isWholeWord
        self.scandir()
        
    def scandir(self):
        for file in os.listdir(self.datadir):
            path = os.path.join(self.datadir, file)
            if os.path.isdir(path):
                continue
            if file.endswith('.txt'):
                self.proceedFile(file, path)
        self.countExamples()

    def proceedFile(self, filename, path):
        example = ExampleFile(filename)
        for line in open(path, 'r', encoding = "utf-8-sig"): # !!! 'utf-8-sig' means UTF-8(without BOM) so it removes first character '\ufeff' int UTF-8(BOM) files
            s = line.strip()
            if s:
                example.addSentence(s)
        self.examples.append(example)

    def clearExamples(self):
        self.examples = []
        
    def countExamples(self):
        self.count[0] = len(self.examples)
        self.count[1] = sum([len(example.sentences) for example in self.examples])
        
    def makeSearchPattern(self, word):
        def repl(m):
            return "(" + "|".join(self.accents[m.group(0)]) + ")"

        word = word.replace("ae", "æ").replace("oe", "œ")
            
        pattern = re.sub("("+ "|".join(self.accents.keys()) +")", repl, word)

        br = "\\b" if self.isWholeWord else ""
        
        return br + pattern + br
        
    def find(self, word):
        self.pattern = self.makeSearchPattern(word.strip().lower())
        #print(pattern)

        result_dict = dict()
        
        for example in self.examples:            
            result = example.search(self.pattern)
            if result:
                result_dict[example.name] = result

        return result_dict

if __name__ == '__main__':
    app = App(isWholeWord = False)

    while True:
        word = input("\nEnter what you want to find: ")
        result = app.find(word)

        for example in result:
            print(" ", example)
            print(*result[example], sep = "\n")
    
