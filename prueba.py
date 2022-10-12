    with sqlite3.connect("basedatos.db") as con:
        con.row_factory=sqlite3.Row #list base datos
        encrp = hashlib.sha256(contraseña.encode('utf-8'))
        pass_enc = encrp.hexdigest()
        cur=con.cursor()
        # roll 1=usuario 2=administrador 3=super administrador
        cur.execute("SELECT * FROM usuario WHERE nom_usu=?",[nom_usu])
        con.commit()
        row=cur.fetchone()
        if row==None:
            flash( "no se encontra contraseña o usuario")
            return redirect("/")
        elif row["nom_usu"]==nom_usu and row["contraseña"]==pass_enc:
            session['user']=row["nom_usu"]
            session['roll']=row["roll"]
            if session['roll']== "1":
                return redirect("/inicio")
            elif session['roll']== "2":
                return redirect("/admin")
            elif session['roll']== "3":
                return redirect("/admin")
            else:
                flash( "no se encontra contraseña o usuario")
                return "no se encontro tu roll"

        else:
            flash( "no se encontra contraseña o usuario")
            return redirect("/")



    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM usuario WHERE usuario = ? AND contraseña = ?', (username, password))
    user = cursor.fetchone()
    cursor.close()