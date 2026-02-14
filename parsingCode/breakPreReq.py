test1 = '((STAT 121C and JSA 391C) and (CS 123C, 123XS, or 391XS)) or (CS 101C, 101XS, MATH 124C, or 152XS)'
test2 = "((STAT 121C and JSA 391C) and (CS 123C or CS 123XS or CS 391XS)) or (CS 101C or CS 101XS or MATH 124C or MATH 152XS)"
test3 = 'CS 123C, 123XS, or CS 235'
test4 = '(CS 125C, 235XS, and MATH 139C) and CS 124XS'
test5 = 'CS 235C'
test6 = '(CS 211C or 211XS)'
test7 = '(CS 262C or 262XS) and (CS 310C or 310XS)'
testList = [test1,test2,test3,test4,test5,test6,test7]

import re
import itertools

######################################################################
# Chat-GPT Generated Code: 
######################################################################

def tokenize(text):
    # Remove commas
    text = text.replace(",", "")
    # Tokenize parentheses, operators, and courses
    pattern = r'\(|\)|and|or|[A-Z]+\s*\d+[A-Z]*'
    return re.findall(pattern, text)

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self):
        tok = self.peek()
        self.pos += 1
        return tok

    # OR level
    def parse_expression(self):
        paths = self.parse_term()

        while self.peek() == "or":
            self.consume()
            right = self.parse_term()
            paths = paths + right  # OR = branch

        return paths

    # AND level
    def parse_term(self):
        paths = self.parse_factor()

        while self.peek() == "and":
            self.consume()
            right = self.parse_factor()

            # AND = extend every existing path
            paths = [
                p1 + p2
                for p1, p2 in itertools.product(paths, right)
            ]

        return paths

    def parse_factor(self):
        if self.peek() == "(":
            self.consume()
            paths = self.parse_expression()
            self.consume()  # consume ')'
            return paths
        else:
            course = self.consume().replace(" ", "")
            return [[course]]

######################################################################
# Human Written (Shruti Written) Code:
######################################################################

def commasReduction(text):
    stack = [] 

    for char in range(len(text)):
        if text[char] == '(':

            wordToPush = ''
            for nextChar in text[char+1:]:
                if nextChar == '(':
                    continue
                elif nextChar == ')':
                    if wordToPush not in stack:
                        stack.append(wordToPush)
                    break
                else:
                    wordToPush += nextChar

    if '(' not in text:
        stack.append(text)
    
    return stack

def replaceCommasAnd(stack):
    newStack = []
    dictionaryReplacement = {}
    for item in stack:
        newItem = item
            
        if ', or ' in item:
            newItem = newItem.replace(', or ', ' or ')
        if ', and ' in item:
            newItem = newItem.replace(', and ', ' and ')

        if ' or ' in item:
            newItem = newItem.replace(', ',' or ')
        elif ' and ' in item:
            newItem = newItem.replace(', ',' and ')

        dictionaryReplacement[item]=newItem
    return dictionaryReplacement

def textReplacementDictionary(dictionary,originalText):
    for phrase in dictionary:
        originalText = originalText.replace(phrase,dictionary[phrase])
    return originalText

def addSubjects(dictionaryReplacement):
    #print(dictionaryReplacement)
    priorWord = ''
    
    for item in dictionaryReplacement:
        listWords = dictionaryReplacement[item].split(' ')
        dept = ''
        counter = 0
        for word in listWords:
            if word in ('and','or'):
                pass
            elif not any(char.isdigit() for char in word):
                dept = word
            elif any(char.isdigit() for char in word) and priorWord != dept:
                newword = dept + ' ' + word
                listWords[counter] = newword
            priorWord = word
            counter += 1
        words = ' '.join(listWords)
        dictionaryReplacement[item]=words
        #print(f'key: {item}\nvalue: {words}\n')
    return dictionaryReplacement

def manipulateNoCommas(text):
    dictionary2 = {}
    for item in text:  
        dictionary2[item] = item
    return dictionary2

def replaceText(text):
    rephrasedText = text 
    textWithoutCommas = commasReduction(text)
    #print(textWithoutCommas)
    if ',' in text:
        extendedDictionary = replaceCommasAnd(textWithoutCommas)
    else:
        extendedDictionary = manipulateNoCommas(textWithoutCommas)    
    updatedSubjectDictionary = addSubjects(extendedDictionary)
    rephrasedText = textReplacementDictionary(updatedSubjectDictionary,text)
    
    return rephrasedText

def parseResult(text):
    textRephrased = replaceText(text)
    tokens = tokenize(textRephrased)
    parser = Parser(tokens)
    result = parser.parse_expression()

    result = [sorted(path) for path in result]
    return result
