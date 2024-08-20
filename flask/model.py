class Model:
    def __init__(self, file):
        self.file = file
        self.model = 'model'
        self.status = 'finish'

    def read_data(self):
        print('read_data from {}'.format(self.file))

    def solve(self):
        print('solve')

    def write(self):
        print('write')

    def error(self):
        self.status = 'error'
        print('error')
