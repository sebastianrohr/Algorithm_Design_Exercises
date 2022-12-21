import sys


class Matching:
    class StackQueue:
        def __init__(self, size):
            self.size = size
            self.array = [i for i in range(self.size)]
            self.lastIndex = size

        def pop(self):
            if self.lastIndex == 0:
                raise IndexError

            output = self.array[self.lastIndex - 1]

            self.lastIndex -= 1

            return output

        def put(self, value):
            self.lastIndex += 1
            self.array[self.lastIndex - 1] = value

        def isEmpty(self):
            if self.lastIndex == 0:
                return True
            else:
                return False

    def __init__(self):
        self.n = None
        self.names = list()
        self.rejecters = list()
        self.proposers = list()
        self.pointers = list()

    def convStrIndex(self, string):
        return (int(string)) // 2

    def rejecterPreferences(self, preferenceString):

        pref = preferenceString.strip().split(" ")[1:]

        return {self.convStrIndex(value): idx for idx, value in enumerate(pref)}

    def proposersPreferences(self, preferenceString):

        prefs = preferenceString.strip().split(" ")[1:]

        self.pointers.append(
            {
                self.convStrIndex(prefs[i]) - 1: self.convStrIndex(prefs[i + 1]) - 1
                for i in range(len(prefs) - 1)
            }
        )

        return self.convStrIndex(prefs[0]) - 1

    def loadInput(self):
        lines = sys.stdin.readlines()

        for idx, line in enumerate(lines):
            if line.startswith("n="):
                self.n = int(line.strip().split("=")[1])
                nIndex = idx
                break

        self.names = [
            lines[i].strip().split()[1]
            for i in range(nIndex + 1, nIndex + (self.n * 2) + 1)
        ]

        prefIndexStart = (
            nIndex + (self.n * 2) + 2
        )  # +2 skips the empty line between names and preferences

        # Initialize all arrays
        self.proposers = [None] * self.n
        self.pointers = [None] * self.n
        self.rejecters = [None] * self.n

        for i in range(prefIndexStart, prefIndexStart + (self.n * 2)):

            splitLine = lines[i].strip().split(" ")
            nameIndex = int(splitLine[0][:-1])

            prefs = splitLine[1:]

            if (nameIndex % 2) != 0:  # if it is an uneven number, then it is a proposer

                self.pointers[(nameIndex - 1) // 2] = {
                    self.convStrIndex(prefs[i]) - 1: self.convStrIndex(prefs[i + 1]) - 1
                    for i in range(len(prefs) - 1)
                }

                self.proposers[(nameIndex - 1) // 2] = self.convStrIndex(prefs[0]) - 1

            else:  # if it is an even number, then it is a rejecter

                self.rejecters[(nameIndex - 1) // 2] = {
                    self.convStrIndex(value): idx for idx, value in enumerate(prefs)
                }

    def gale(self):
        # queue = [i for i in range(self.n)]  # Initiate queue
        queue = self.StackQueue(self.n)

        self.engage = [None] * self.n  # Initiate engagement array
        while not queue.isEmpty():  # while queue is not empty
            # print(queue.array)
            current_proposer = (
                queue.pop()
            )  # returns last element of the array, constant time
            current_preference = self.proposers[
                current_proposer
            ]  # find their current preference

            partner = self.engage[
                current_preference
            ]  # find who the current partner of the preference is

            if partner is None:
                self.engage[
                    current_preference
                ] = current_proposer  # if they have no partner, become engaged to the rejecter

            else:
                # dictionary lookups, ensuring indexing in constant time
                if (
                    self.rejecters[current_preference][current_proposer]
                    < self.rejecters[current_preference][partner]
                ):  # Who does the rejecter prefer

                    self.engage[current_preference] = current_proposer

                    self.proposers[partner] = self.pointers[partner][
                        self.proposers[partner]
                    ]
                    queue.put(partner)
                else:
                    self.proposers[current_proposer] = self.pointers[current_proposer][
                        self.proposers[current_proposer]
                    ]
                    queue.put(current_proposer)
            # print(self.engage)

    def formatOutput(self):
        for pair in sorted(
            [(rejecter, proposer) for rejecter, proposer in enumerate(self.engage)],
            key=lambda x: x[1],
        ):

            name1 = self.names[pair[1] * 2]
            name2 = self.names[(pair[0] * 2) + 1]

            print(name1 + " -- " + name2, end="\r\n")


# ! Has to write to standard output STDOUT

gale = Matching()
gale.loadInput()
gale.gale()
gale.formatOutput()
