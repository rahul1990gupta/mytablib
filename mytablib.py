from operator import itemgetter


class Row(object):

    def __init__(self, *args):
        self._data = args


class Databook(object):
    pass


class Dataset(object):
    def __init__(self, *args, **kwargs):
        self._data = []
        self._headers = None
        self.title = None

        if args:
            if isinstance(args, tuple) and not isinstance(args[0], tuple):
                self._data = [args]
            else:
                self._data = list(args)

        if "headers" in kwargs:
            self._headers = kwargs["headers"]
        if "title" in kwargs:
            self.title = kwargs["title"]

    def append(self, row_tuple):
        if self.width and len(row_tuple) != self.width:
            raise InvalidDimensions

        if self.headers and (len(row_tuple) != len(self.headers)):
            raise InvalidDimensions

        self._data.append(tuple(row_tuple))

    def append_col(self, col, header=None):
        if callable(col):
            col = map(col, self._data)

        if not self._data:
            self._data = [tuple() for _ in col]
        for i, row_tuple in enumerate(self._data):
            self._data[i] = row_tuple + (col[i],)

        if header and self.headers:
            self.headers += (header, )

    def get_col(self, index):
        return map(itemgetter(index), self._data)

    # Used for slicing _data and accessing values corresponding to a column
    def __getitem__(self, item):
        # When invoked with slice syntax, it will receive a slice object.
        if isinstance(item, str):
            index = self.headers.index(item)
            return self.get_col(index)

        return self._data[item]

    @property
    def width(self):
        if len(self._data) > 0:
            return len(self._data[0])

    @property
    def height(self):
        return len(self)

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, value):
        # Assigned headers should match the data help inside
        if self.width > 0 and self.width != len(value):
            raise InvalidDimensions

        self._headers = tuple(value)

    def __len__(self):
        return len(self._data)

    def __delitem__(self, key):
         del self._data[key]

    def __iter__(self):
        for row in self._data:
            yield row


class InvalidDimensions(Exception):
    pass