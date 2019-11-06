class WEBSRV:
    def __init__(self):
        import uos
        files = uos.listdir()
        if("creds.txt" in files):
            f = open("index.html", "r")
            self.html = str(f.read())
            f.close()
        else:
            f = open("creds.html", "r")
            self.html = str(f.read())
            f.close()