
html = """
<!DOCTYPE html>
        <html>

        <header>
        <META HTTP-EQUIV="content-type" CONTENT="text/html; charset=utf-8">
        <style>
        body {background-color: rgb(243, 108, 84);
                font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;}
        h1   {color: rgb(255, 255, 255);}
        p    {color: red;}
        </style>
        </header>

        <body>

        <h1>Coolt att denna hemsidan körs på en pico</h1>
        <p>Gött me kebab</p>
        <a href="https://youtu.be/dQw4w9WgXcQ">Pico SDK</a><br>


        </body>
        </html>
"""

html_bad_request = """
<!DOCTYPE html>
        <html>

        <header>
        <META HTTP-EQUIV="content-type" CONTENT="text/html; charset=utf-8">
        <style>
        body {background-color: rgb(243, 108, 84);
                font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;}
        h1   {color: red;}
        p    {color: red;}
        </style>
        </header>

        <body>

        <h1>400 Bad request</h1>
        <p>Plz försök igen...</p>

        </body>
        </html>
"""
