from random import choice, randint


class Markov():

    def __init__(self, fname):
        self.chain = self.process_file(fname)
        self.starts = None

    def process_file(self, fname):
        """ This should be dynamic; changing with your corpus as necessary"""

        chain = {}

        with open(fname, 'r') as f:

            # iterate over lines
            for line in f:
                line = line.strip()
                line = line.split(' ')
                prefix = ('', '')

                # iterate over words
                for word in line:
                    if word != '':

                        # Add prefix to chain
                        if prefix not in chain.keys():
                            chain[prefix] = {'suffixes': [], 'end': False}

                        # Add next word to suffix list
                        if word not in chain[prefix]['suffixes']:
                            chain[prefix]['suffixes'].append(word)

                        # Add end flag if prefix[1] contains a period
                        if len(prefix[1]) > 0 and prefix[1][-1] == '.':
                            chain[prefix]['end'] = True

                        # Update prefix i.e: (quick, brown) -> (brown, fox)
                        prefix = (prefix[1], word)

                # Add final prefix to chain
                if prefix not in chain:
                    chain[prefix] = {'suffixes': [], 'end': False}

                # Add an end flag to ending prefix
                chain[prefix]['end'] = True

        return chain

    def generate(self):
        chain = self.chain
        prefix = choice(list(chain.keys()))
        text = prefix[0]

        while len(text.split(' ')) < 100:  # Limit output length here
            text += ' ' + prefix[1]

            if len(chain[prefix]['suffixes']) == 0:
                return text

            if chain[prefix]['end'] and randint(1, 100) < 101:
                return text

            prefix = (prefix[1], choice(chain[prefix]['suffixes']))

        return text

    def chain_to_txt(self):
        """ Save the chain to a text file to reduce overhead"""
        pass


if __name__ == '__main__':
    mark = Markov('metamorphosis.txt')
    text = mark.generate()
    print(text)
