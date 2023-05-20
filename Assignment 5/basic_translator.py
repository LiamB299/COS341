import re


class BasicTranslator:
    def __init__(self, source_code: str):
        self.ordered_source: dict | None
        self.ordered_source = None
        self.source = source_code

    def _define_line_numbers(self):
        lines = re.split(r'\n', self.source)
        self.ordered_source = {}

        for i, line in enumerate(lines):
            self.ordered_source[i + 1] = line

    def _remove_labels(self):
        line: str
        new_code = self.ordered_source.copy()
        for line_number, line in self.ordered_source.items():
            if line.find('label_') >= 0 > line.find('GOTO'):
                for goto_line_number, goto_line in self.ordered_source.items():
                    if 0 <= goto_line.find('GOTO') and goto_line.find(line[:-1]) > 0:
                        if goto_line.find('GOTO') == 0:
                            new_code[goto_line_number] = f'GOTO {line_number}'
                        else:
                            new_code[goto_line_number] = goto_line[:goto_line.find('GOTO')-1] + f" GOTO {line_number}"
                new_code[line_number] = ''
        self.ordered_source = new_code

    def _update_gotos_lines(self):
        line: str
        last_line = len(self.ordered_source)
        new_code = self.ordered_source.copy()
        for line_number, line in self.ordered_source.items():
            if line.find('GOTO') >= 0:
                # goto the line
                start_line = int(line[line.find("GOTO")+4:])
                while start_line != last_line:
                    if self.ordered_source[start_line] != '':
                        if line.find('GOTO') == 0:
                            new_code[line_number] = f'GOTO {start_line}'
                        else:
                            new_code[line_number] = line[:line.find('GOTO') - 1] + f" GOTO {start_line}"
                        break
                    start_line += 1
        self.ordered_source = new_code

    def _remove_empty_lines(self):
        final_code = {}
        for line_number, line in self.ordered_source.items():
            if line != '':
                final_code[line_number] = line
        self.ordered_source = final_code

    def _update_var_names(self):
        for line_number, line in self.ordered_source.items():
            if line[0] in ['n', 'b', 's']:
                self.ordered_source[line_number] = f'LET {line}'

    def printer(self):
        self._define_line_numbers()
        self._remove_labels()
        self._update_gotos_lines()
        self._remove_empty_lines()
        self._update_var_names()

        for line_number, line in self.ordered_source.items():
            print(line_number, line)
