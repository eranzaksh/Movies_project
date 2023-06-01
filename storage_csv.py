from istorage import IStorage


class Storage_csv(IStorage):
    def __init__(self, filepath):
        self.filepath = filepath

    @staticmethod
    def pr_red(skk):
        """
        Make a print statement in red color
        """
        print("\033[91m {}\033[00m".format(skk))


