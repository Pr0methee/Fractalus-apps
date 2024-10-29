import sqlite3,os,connect,sys,launcherror

try:
    import win32api,tktooltip,psutil,shutil,PIL,sympy,pdf2image
except Exception as err:
    print(err)
    os.system(os.getcwd()+'\\installer.bat')
    raise launcherror.LaunchAgain
    print("Some modules have been installed please launch main.pyw again")
    from tkinter.messagebox import showwarning
    showwarning("Please launch again","Some modules have been installed please launch main.pyw again")
    sys.exit()

if not os.path.exists('H/cache'):
    os.mkdir('H/cache')
    os.mkdir('H/Users')
    conn = sqlite3.connect("H/cache/profils.sq3")
    cur = conn.cursor()
    cur.execute("CREATE TABLE profils (id TEXT, mdp TEXT)")
    cur.execute("CREATE TABLE preferances (user TEXT,bg TEXT,builtinpy TEXT,comlatex TEXT,compy TEXT, errpy TEXT, fctpy TEXT, mm2latex TEXT,mmlatex TEXT,modpy TEXT, mclatex TEXT,mcpy TEXT, mcsql TEXT, strpy TEXT)")

    connect.create_profil('admin','@dmin')