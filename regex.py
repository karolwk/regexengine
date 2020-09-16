import sys

sys.setrecursionlimit(10000)


class RegEx:

    def __init__(self):
        self.pre_char = ""
        self.next_char = ""
        self.rep_chars = ("*", "+", "?")
        self.meta_chars = ("^", "$", "?", "*", "+", ".")
        self.escape = False

    def compare(self, rchar, char):
        """Compares regex char with word char"""
        if len(rchar) > 1 and not self.escape:
            if rchar[0] == "." and (rchar[1] == "*" or rchar[1] == "?"):
                return False
        if rchar[0] == char or (rchar[0] == "." and char and not self.escape) or (not rchar[0] and char):
            self.escape = False
            return True
        return False

    def check_escape(self, regex):
        """Checks for escape sequence"""
        if len(regex) > 1:
            if regex[:1] == "\\":
                self.escape = True
                return True
        return False

    def check_meta(self, regex):
        """Checks for metacharacters"""
        if regex[0] in self.rep_chars:
            return True
        if len(regex) >= 2:
            if regex[1] == "*" or regex[1] == "?":
                return True
        return False

    def check_multi(self, regex, word):
        """Checks for multiple occurences of chars for '*' and '+' meta chars"""
        if len(regex) > 1:
            self.next_char = regex[1]
            # Compare character after meta
            if (regex[0] == "*" or regex[0] == "+") and self.compare(self.next_char, word[0]):
                return False
        # Compare character before meta
        if (regex[0] == "*" or regex[0] == "+") and self.compare(self.pre_char, word[0]):
            return True
        return False

    def compare_regex(self, regex, word):
        """Compares given word with regex value """
        if not len(regex):
            return True
        if len(word):
            if self.check_escape(regex):
                return self.compare_regex(regex[1:], word)
            if self.compare(regex, word[:1]):
                self.pre_char = regex[:1]
                return self.compare_regex(regex[1:], word[1:])
            if self.check_multi(regex, word) and not self.escape:
                return self.compare_regex(regex, word[1:])
            if self.check_meta(regex) and not self.escape:
                self.pre_char = regex[:1]
                return self.compare_regex(regex[1:], word)
        elif not len(word) and len(regex) == 1 and (regex[0] == "$" or regex[0] in self.rep_chars):
            return True
        return False

    def find(self, regex, word):
        """Finds regex in word, by slicing word"""
        if "^" in regex:
            # Case for "^" metacharacter
            return self.compare_regex(regex[1:], word)
        if not len(word) and not len(regex):
            return True
        if len(word) == 0:
            return False
        if not self.compare_regex(regex, word):
            return self.find(regex, word[1:])
        return True


def main():
    regex, word = input().split("|")
    re = RegEx().find(regex, word)
    print(re)


if __name__ == "__main__":
    main()
