import sys
import random

class Node: #Prefix와 다음 노드를 저장
    def __init__(self, data=None):
        self.data = Prefix()
        self.next = None

class Prefix: #2개의 단어와 Suffix를 저장 
    def __init__(self, pword1, pword2):
        self.pword1 = pword1
        self.pword2 = pword2
        self.suf = None
        self.sumFreq = 0
        
class Suffix: #단어와 빈도를 저장
    def __init__(self, sword, freq=1):
        self.sword = sword
        self.freq = freq
        #self.freq = freq if freq is not None else 1
        self.next = None

class MarkovChainClass:
    def __init__(self):
        self.NHASH = 4093         #해시 테이블의 크기
        self.MULTIPLIER = 31      #해시 값을 계산하는 데 사용하는 상수
        self.MAX = 200            #생성할 문장의 최대 길이를 지정하는 상수
        self.htable = [None] * self.NHASH   #hash table 배열 (Prefix 노드들을 저장함)
        self.inputString = ""     #사용자로부터 입력 받은 파일명을 저장하는 변수
    
    # def main():
    #     MKCC = MarkovChainClass()
    #     #사용자로부터 파일 이름을 입력 받음.
    #     filename = input("읽을 파일 이름을 입력하시오(ex. HarryPotter.txt): ").strip()
    #     try:
    #         MKCC.read_file(filename)
    #         # with open(filename, 'r') as f:
    #         #     if not MKCC.read_file(filename):
    #         #         print("파일을 읽을 수 없습니다.")
    #         #         sys.exit()
    #     except IOError:
    #         print("파일을 열 수 없습니다.")
    #         sys.exit()

    #     print("File Read.")
    #     MKCC.print_hash_table()  # 해시 테이블이 제대로 만들어졌는지 확인
    #     print("Markov Chain >>\n")
    #     MKCC.print_fake_text()

    def read_file(self, filename):
        try:
            with open(filename, 'r') as file:
                self.inputString = file.read()
                key1, key2, suffix, token = None
                lineBuffer = file.readline()
                tokenizer = lineBuffer.split()
                while lineBuffer:
                    for token in tokenizer:
                        key1, key2 = key2, suffix
                        suffix = token

                        if not key1: #key1이 null인데 토큰이 없다면
                            if not tokenizer:
                                # 줄 바꿔서 다음 토큰 가져옴
                                lineBuffer = file.readline().strip()  # 개행문자 제거
                                if not lineBuffer:
                                    #EOF = True
                                    break
                                continue
                            else:
                                continue

                        if not tokenizer: # 다음 토큰이 없다면(줄의 끝 이라면) 다음 줄 읽어놓음(다음 토큰은 다음 줄의 첫 단어)
                            lineBuffer = file.readline().strip()  # 개행문자 제거
                            if not lineBuffer:
                                #EOF = True
                                break
                            tokenizer = lineBuffer.split()

                        # key1, key2 로 해슁한 index 에 node 추가한다
                        p = Prefix(key1, key2)
                        index = self.Hash(key1, key2)
                        index = abs(index)

                        # 노드가 없다면 처음으로 추가
                        if self.htable[index] is None:
                            newN = Node(p)
                            self.htable[index] = newN
                            # suffix 가 있다면 추가
                            if suffix is not None:
                                s = Suffix(suffix)
                                self.htable[index].data.suf = s
                                self.htable[index].data.sumFreq += 1
                        # 노드가 존재한다면 연결
                        else:
                            head = self.htable[index]
                            before = None
                            hasSamePrefix = False
                            while head is not None:
                                # 생성된 prefix가 기존의 prefix들 중 일치한다면
                                if head.data.pword1 == key1 and head.data.pword2 == key2:
                                    # suffix 입력됬으면 추가
                                    if suffix is not None:
                                        nowP = head.data
                                        hasSameSuffix = False
                                        # suffix 처음 생성시
                                        if nowP.suf is None:
                                            tmpS = Suffix(suffix)
                                            nowP.suf = tmpS
                                            nowP.sumFreq += 1
                                        # suffix 존재시 연결
                                        else:
                                            beforeS = None
                                            tmpS = nowP.suf
                                            while tmpS is not None:
                                                # 동일한 suffix 존재시 freq 상승
                                                if tmpS.sword == suffix:
                                                    tmpS.freq += 1
                                                    nowP.sumFreq += 1
                                                    hasSameSuffix = True
                                                    break
                                                beforeS = tmpS
                                                tmpS = tmpS.next
                                            # 여기까지오면 동일한 suffix 없으므로 추가
                                            if not hasSameSuffix:
                                                newS = Suffix(suffix)
                                                nowP.sumFreq += 1
                                                beforeS.next = newS
                                    hasSamePrefix = True
                                    break
                                before = head
                                head = head.next
                            # 여기까지 오면 동일한 prefix 없으므로 추가
                            if not hasSamePrefix:
                                newN = Node(p)
                                before.next = newN
                                # 여기서도 suffix 입력됬으면 추가해줘야함
                                if suffix is not None:
                                    newS = Suffix(suffix)
                                    p.suf = newS
                                    
                                    p.sumFreq += 1

        except FileNotFoundError:
            print("No such file or directory found.")
        #EOF = False
        
    def print_hash_table(self):
        print("Print HashTable")
        for i in range(self.NHASH):
            node = self.htable[i]
            if node is None:
                continue
            p = node.data
            print("#{}: Prefix: {}, {}\t\tSuffix: ".format(i, p.pword1, p.pword2), end="")
            s = p.suf
            while s is not None:
                print("{0}({1}), ".format(s.sword, s.freq), end="")
                s = s.next
            print()

    def Hash(self, key1, key2):
        h = 0
        p = key1
        for i in range(len(p)):
            chr = ord(p[i])
            h = self.MULTIPLIER * h + chr
        p = key2
        for i in range(len(p)):
            chr = ord(p[i])
            h = self.MULTIPLIER * h + chr
        return h % self.NHASH

    def make_prefix(key1, key2):
        p = Prefix()
        p.pword1 = key1
        p.pword2 = key2
        p.sumFreq = 0
        p.suf = None
        return p

    def make_suffix(suffix):
        s = Suffix()
        s.sword = suffix
        s.freq = 1
        s.next = None
        return s

    def make_node(p):
        newNode = Node()
        newNode.data = p
        newNode.next = None
        return newNode

    def print_fake_text(self):
        randIndex = 0
        while self.htable[randIndex] is None:
            randIndex = abs(random.randint(0, 2**32-1)) % self.NHASH
        print(self.htable[randIndex].data.pword1, self.htable[randIndex].data.pword2, end=' ')
        self.make_fake_text(self.htable[randIndex].data, 0)

    def make_fake_text(self, prefix, count):
        if prefix is None or count == 1000:
            return -1
        randSuffix = self.get_random_suffix(prefix)
        if randSuffix is None:
            return -1
        print(randSuffix.sword, end=' ')
        nextPrefix = self.find_prefix(prefix.pword2, randSuffix.sword)
        return self.make_fake_text(nextPrefix, count+1)

    def get_random_suffix(p):
        i = 0
        randNum, sequenceNum = 0, 0
        weightArray = []
        suf = p.suf
        if suf is None or p.sumFreq == 0:
            return None
        while suf is not None:
            if i == 0:
                # 첫 suffix 의 freq는 그냥 추가
                weightArray.append(suf.freq)
                suf = suf.next
                i += 1
                continue
            # 현재 suffix의 freq와 이전이 값들을 누적하여 추가
            weightArray.append(suf.freq + weightArray[i-1])
            suf = suf.next
            i += 1
        randNum = random.randint(-(2**31), (2**31)-1) % p.sumFreq
        for j in range(len(weightArray)):
            # 처음으로 randNum 이 누적 freq보다 작거나 같은 suffix 찾는다
            if randNum <= weightArray[j]:
                sequenceNum = j
                break
        # sequenceNum 번째로 나오는 suffix 찾아서 반환
        suf = p.suf
        while sequenceNum > 0:
            suf = suf.next
            sequenceNum -= 1
        return suf

    def find_prefix(self, key1, key2):
        index = self.Hash(key1, key2)
        index = abs(index)
        id = int(index)
        n = self.htable[id]
        while n is not None:
            # 주어진 key와 같은 prefix 찾으면 반환
            if n.data.pword1 == key1 and n.data.pword2 == key2:
                return n.data
            n = n.next
        return None


    def main():
        MKCC = MarkovChainClass()
        #사용자로부터 파일 이름을 입력 받음.
        filename = input("읽을 파일 이름을 입력하시오(ex. HarryPotter.txt): ").strip()
        try:
            MKCC.read_file(filename)
            # with open(filename, 'r') as f:
            #     if not MKCC.read_file(filename):
            #         print("파일을 읽을 수 없습니다.")
            #         sys.exit()
        except IOError:
            print("파일을 열 수 없습니다.")
            sys.exit()

        print("File Read.")
        MKCC.print_hash_table()  # 해시 테이블이 제대로 만들어졌는지 확인
        print("Markov Chain >>\n")
        MKCC.print_fake_text()
        
MarkovChainClass.main()