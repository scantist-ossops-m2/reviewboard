from django.utils.six.moves import cStringIO as StringIO
from reviewboard.diffviewer.parser import (DiffParser, DiffParserError,
                                           ParsedDiffFile)
        preamble = StringIO()
                if self.files:
                    self.files[-1].finalize()

                file_info.prepend_data(preamble.getvalue())
                preamble.close()
                preamble = StringIO()
                preamble.close()
                preamble = StringIO()
                preamble.write(self.lines[i])
                preamble.write(b'\n')
        try:
            if self.files:
                self.files[-1].finalize()
            elif preamble.getvalue().strip() != b'':
                # This is probably not an actual git diff file.
                raise DiffParserError('This does not appear to be a git diff',
                                      0)
        finally:
            preamble.close()
        file_info = ParsedDiffFile()
        file_info.append_data(diff_git_line)
        file_info.append_data(b'\n')
            file_info.append_data(headers[b'new file mode'][1])
            file_info.append_data(headers[b'deleted file mode'][1])
            file_info.append_data(headers[b'old mode'][1])
            file_info.append_data(headers[b'new mode'][1])
                file_info.append_data(headers[b'similarity index'][1])
            file_info.append_data(headers[b'rename from'][1])
            file_info.append_data(headers[b'rename to'][1])
                file_info.append_data(headers[b'similarity index'][1])
            file_info.append_data(headers[b'copy from'][1])
            file_info.append_data(headers[b'copy to'][1])
            file_info.append_data(headers[b'index'][1])
                file_info.append_data(self.lines[linenum])
                file_info.append_data(b'\n')
                file_info.append_data(orig_line)
                file_info.append_data(b'\n')
                file_info.append_data(new_line)
                file_info.append_data(b'\n')
        for attr in ('origInfo', 'newInfo'):