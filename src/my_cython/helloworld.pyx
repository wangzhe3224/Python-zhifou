# print("Hello World")

cdef class Test:
    cdef public str date
    cdef public str writer

    def __init__(self, date, writer):
        self.date = date 
        self.writer = writer