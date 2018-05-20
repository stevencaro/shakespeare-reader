
class CircularList():
    def __init__(self, l):
        self.clist = l
        self.start = 0
        self.curr = 0
        self.end = len(l)-1

    def __bool__(self):
        return len(self.clist) > 0

    def __repr__(self):
        return "Pos: {} in: {}".format(self.curr, self.clist)

    def __str__(self):
        return "Pos: {} in: {}".format(self.curr, self.clist)

    def __getitem__(self, k):
        try:
            return self.clist[k]
        except IndexError:
            pass

    def current(self):
        return self.clist[self.curr]

    def next(self):
        if self.curr + 1 > self.end:
            self.curr = 0
        else:
            self.curr += 1
        return self.current()

    def prev(self):
        if self.curr - 1 < 0:
            self.curr = self.end
        else:
            self.curr -= 1
        return self.current()

