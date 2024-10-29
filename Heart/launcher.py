import launcherror
id,mdp='',''
while True:
    try:
        import App
    except launcherror.LaunchAgain as e:
        print('launch again')

        if 'App' in dir():del App
 