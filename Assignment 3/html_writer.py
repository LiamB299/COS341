from classes import *


class HtmlWriter:

    def __init__(self):
        file = open('output.html', 'w+')
        file.write("""
        <!DOCTYPE html>
            <html>
                <head>
                    <style>
                        table {
    border-collapse: collapse;
}

th {
    border: 1px solid black;
    padding: 8px;
}

td {
    border: 1px solid black;
    padding: 8px;
}
                    </style>
                </head>
            <body>
        """)
        file.close()

        self.file = open('output.html', 'a+')

    def write_vars(self, varss: VariableTable):
        self.file.write("<h1>Variables</h1>")
        self.file.write(varss.print_html())

    def write_procs(self, procs: ProcedureTable):
        self.file.write("<h1>Procedures</h1>")
        self.file.write(procs.print_html())

    # def write_errors(self, errors):
    #     self.file.write("<h1>Errors</h1>")
    #     self.file.write(procs.print_html())

    def __del__(self):
        self.file.write("""
            </body>
        </html>
        """)
        self.file.close()
