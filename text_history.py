class TextHistory:
    def __init__(self):
        self._text = ''
        self._log_change = []
        self._version = 0

    def text(self):
        return self._text

    def version(self):
        return self._version

    def insert(self, text, version_prod = 1, pos = None):
        if pos is None:
            pos = len(self._text)
        elif 0 <= pos <= len(self._text):
            object_insert = InsertAction(text, pos, self._version, version_prod + self._version)
            self._text = object_insert.apply(text)
        else:
            raise ValueError("pos error")

        self._version = self._version + version_prod
        self._log_change.append([self._version, self._text])
        return self._version

    def replace(self, text, version_prod = 1, pos = None):
        if pos is None:
            pos = len(self._text)
        elif 0 <= pos <= len(self._text):
            object_replace = ReplaceAction(text, pos, self._version, version_prod + self._version)
            self._text = object_replace.apply(self._text)
        else:
            raise ValueError("pos error")

        self._version = self._version + version_prod
        self._log_change.append([self._version, self._text])
        return self._version

    def delete(self, length, version_prod = 1, pos = None):
        if pos is None:
            pos = len(self._text)
        elif 0 <= pos <= len(self._text):
            object_delete = DeleteAction(length, pos, self._version, version_prod + self._version)
            self._text = object_delete.apply(self._text)
        else:
            raise ValueError("pos error")

        self._version = self._version + version_prod
        self._log_change.append([self._version, self._text])
        return self._version

    def action(self, action):
        if type(action) == InsertAction:
            self.insert(action.text, action.to_version - action.from_version, action.pos)
        elif type(action) == ReplaceAction:
            self.replace(action.text, action.to_version - action.from_version, action.pos)
        elif type(action) == DeleteAction:
            self.delete(action.length, action.to_version - action.from_version, action.pos)
        else:
            raise ValueError("error")

        return self._version

    def get_actions(self, from_version, to_version):
        new_list = list()

        if from_version < 0 or to_version < 0:
            raise ValueError("error from_version < 0 or to_version < 0")
        elif from_version > to_version:
            raise ValueError("error from_version > to_version")
        else:
            for idx, i in enumerate(self._log_change):
                if i[0] >= from_version and i[0] <= to_version:
                    new_list.append(i)

        return new_list

class Action:
    def __init__(self, from_version, to_version):
        self._from_version = from_version
        self._to_version = to_version

    def apply(self, old_string):
        return old_string


class InsertAction(Action):
    def __init__(self, text, pos, from_version, to_version):
        self._text = text
        self._pos = pos
        super().__init__(from_version, to_version)

    def apply(self, old_string):
        modif_string = old_string[:self._pos] + self._text + old_string[self._pos + len(self._text):]
        return modif_string


class ReplaceAction(Action):
    def __init__(self, text, pos, from_version, to_version):
        self._text = text
        self._pos = pos
        super().__init__(from_version, to_version)

    def apply(self, old_string):
        modif_string = old_string[:self._pos] + self._text
        if self._pos + len(self._text) < len(old_string):
            modif_string += old_string[self._pos + len(self._text):len(old_string)]

        return modif_string

class DeleteAction(Action):
    def __init__(self, length, pos, from_version, to_version):
        self._length = length
        self._pos = pos
        super().__init__(from_version, to_version)

    def apply(self, old_string):
        modif_string = old_string[:self._pos]
        if self._pos + self._length < len(old_string):
            modif_string += old_string[self._pos + self._length:]
        return modif_string

