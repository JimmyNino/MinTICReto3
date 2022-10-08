from datetime import date,datetime
from flask import Flask,render_template,request,redirect,flash,session,send_from_directory,url_for
from werkzeug.utils import escape, secure_filename
import sqlite3 ,hashlib,os
import pathlib
from os import remove



app=Flask(__name__)
app.secret_key = os.urandom(20)

@app.route("/registrarse",methods=["GET","POST"])
def registrarse():
    return render_template ("register.html")
#=====intento de que muestre imagenes ======):
CARPETA= os.path.join('imagenes')
app.config['CARPETA']=CARPETA
@app.route("/imagenes/<nombredelafoto>",methods=["GET","POST"])
def imagenes(nombredelafoto):
    return send_from_directory("imagenes/",nombredelafoto)    

# =====================registrarse==============:)
@app.route("/registrarse/usuario",methods=["GET","POST"])
def crear_usuario():
    # crear usuario
    nom=escape(request.values["txtnom"])
    correo=escape(request.values["txtcorreo"])
    numero=escape(request.values["txtnum"])
    nom_usu=escape(request.values["txtnomusu"])
    contraseña=escape(request.values["txtcon"])
    with sqlite3.connect("basedatos(1).db") as con:
        encrp = hashlib.sha256(contraseña.encode('utf-8'))
        pass_enc = encrp.hexdigest()
        cur=con.cursor()
        # roll 1=usuario 2=administrador 3=super administrador
        cur.execute("INSERT INTO usuario (nombre,correo,numero,nom_usu,contraseña,roll) VALUES (?,?,?,?,?,?)",[nom,correo,numero,nom_usu,pass_enc,1])
        con.commit()
        flash("Guardado con éxito")
        return redirect("/registrarse")

@app.route("/",methods=["POST","GET"])
def intro():
    return render_template ("intro.html")

@app.route("/admin",methods=["POST","GET"])
def inici():
    if 'user' in session:
            if session['roll']== "1":
                return redirect("/inicio")
            elif session['roll']== "2":
                return render_template ("admnistrador.html")
            elif session['roll']== "3":
                return render_template ("admnistrador.html")
            else:
                return "no se encontro tu roll"
    else:
       return redirect("/")


#)
# =================Login==============:)
@app.route("/login",methods=["POST","GET"])
def login():
# verificar datos
    nom_usu=escape(request.values["txtnom_usu"])
    contraseña=escape(request.values["contra"])
    with sqlite3.connect("basedatos(1).db") as con:
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

        

    
@app.route("/inicio",methods=["GET","POST"])
def inicio():
    if 'user' in session:
        if session['roll']== "1":
            with sqlite3.connect("basedatos(1).db") as con:
                con.row_factory=sqlite3.Row #list base datos
                cur=con.cursor()
                # roll 1=usuario 2=administrador 3=super administrador
                cur.execute("SELECT * FROM publicacion" )
                con.commit()
                row=cur.fetchall()
                if row==None:
                    flash("no se ha encontrado publicaciones disponibles")
                    return render_template ("feed.html")
                else:
                    return render_template ("feed.html",datos=row)
        elif session['roll']== "2" or session['roll']== "3":
            return redirect("/admin")
        else:
            return "no se encontro tu roll"
    else:
       return  redirect("/")
          


               


# ELIMINACON DEL mensaje
def mensajes_eliminar():
    publicacion=escape(request.values[""])
    with sqlite3.connect("basedatos(1).db") as con:
            curso = con.cursor()
            curso.execute("DELETE FROM publicaion WHERE imagen = ?", [publicacion])
            con.commit()
            return("/instagram2/basedatos(1).db/publicacion")
    return("No se puede eliminar la imagen")
        
#==============buscar publicacion para eliminar============
@app.route("/buscar/publi",methods=["GET","POST"])
def buscar_p():
    if 'user' in session:
        if session['roll']== "1":
            return redirect("/inicio")
        elif session['roll']== "2" or session['roll']== "3":
            with sqlite3.connect("basedatos(1).db") as con:
                con.row_factory=sqlite3.Row #list base datos
                cur=con.cursor()
                cur.execute("SELECT * FROM publicacion")
                con.commit()
                row=cur.fetchall()
            return render_template ("eliminar_publi.html",publicacion=row)
            return redirect("/admin")
        else:
            return "no se encontro tu roll"
    else:
        redirect("/") 

#======buscar publicacion eliminar

@app.route("/buscar/publiE",methods=["GET","POST"])
def buscar_publiE():
    buscar_nom_publi=request.values["txtbpubli"]
    with sqlite3.connect("basedatos(1).db") as con:
        con.row_factory=sqlite3.Row #lista de diccionario
                # crea un cursor para manipular la base de datos
        cur=con.cursor()
                #prepara sentencia SQL
        cur.execute("SELECT * FROM publicacion WHERE nom_publi=?",[buscar_nom_publi])
        con.commit()
        row=cur.fetchall()
        global publicaciones
        return render_template("eliminar_publi.html", publicaciones = row)      


#=================== ELIMINACON DE LA PUBLICACION===inici
@app.route('/publi/eliminar/<int:id>' ,methods=["GET","POST"])
def eliminar_publi(id):
    with sqlite3.connect("basedatos(1).db") as con:
        con.row_factory=sqlite3.Row 
        cur=con.cursor()
        cur.execute("SELECT imagen FROM publicacion WHERE  id_publi= ?", [id])
        row=cur.fetchone()
        remove("imagenes/"+row["imagen"])
        print("row")
        cur.execute("DELETE  FROM publicacion WHERE id_publi=?",[id])
        con.commit()
        redirect("/buscar/publi")
        flash("fue eliminada la publicacion exitosamente")
        return redirect("/buscar/publi")




@app.route("/eliminar/usuario",methods=["GET","POST"])
def eliminar_usu():
    if 'user' in session:
        if session['roll']== "1":
            return redirect("/configuracion")
        elif session['roll']== "2":
            return render_template ("eliminar_usu.html")
        elif session['roll']== "3":
            return render_template ("eliminar_usu.html")
        else: 
            return "no se encontro tu roll"
    else:
        return redirect("/")           
    
# ===========buscar Usuario ===================
@app.route("/buscar/usuE",methods=["GET","POST"])
def eliminar_usuario():
    buscar_nom_usu=request.values["txtbusu"]
    with sqlite3.connect("basedatos(1).db") as con:
        con.row_factory=sqlite3.Row #lista de diccionario
                # crea un cursor para manipular la base de datos
        cur=con.cursor()
                #prepara sentencia SQL
        cur.execute("SELECT * FROM usuario WHERE nom_usu=?",[buscar_nom_usu])
        con.commit()
        row=cur.fetchall()
        global datos
        return render_template("eliminar_usu.html", datos = row)

# ===========buscar Eliminar ===================

@app.route("/usuario/eliminar/<int:id>", methods=["GET", "POST"])
def usuario_eliminar(id):
    with sqlite3.connect("basedatos(1).db") as con:
        cur = con.cursor()
        cur.execute("DELETE FROM usuario WHERE id_usu = ?", [id])
        con.commit()#lista de diccionario
        flash("usuario eliminado")
        return redirect("/eliminar/usuario")
# =========== Editar roll===================
@app.route("/usuario/editarroll/<int:id>", methods=["GET", "POST"])
def usuario_editroll(id):
    with sqlite3.connect("basedatos(1).db") as con:
        con.row_factory=sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM usuario WHERE id_usu = ?", [id])
        row=cur.fetchall()
        global datos
        con.commit()
        return render_template('editar_roll.html',datos=row)        
# =========== guardarroll ===================

@app.route("/guardar/roll/<id>", methods=["GET", "POST"])
def usuario_guardarroll(id):
    id_usu=request.values["txtid"]
    roll_usu=request.values["txtroll"]
    with sqlite3.connect("basedatos(1).db") as con:
        cur = con.cursor()
        cur.execute("UPDATE usuario SET roll=?  WHERE id_usu=?", [roll_usu,id_usu])
        con.commit()        
        flash("se ha editado exitosamente el rol del usuario")
        return redirect("/eliminar/usuario")
    # =================perfil usuario===========no sirve
@app.route("/perfil/usuario",methods=["GET"])
def ver_perfil():
    if 'user' in session:
        if session['roll']== "1":
            return render_template ("perfilUsuario.html")
        elif session['roll']== "2":
            return redirect("/admin")
        elif session['roll']== "3":
            return redirect("/admin")
        else:
            return "no se encontro tu roll"
    else:
       return redirect("/")
    
@app.route("/crearpublicacion",methods=["GET"])
def cre_publicacion():
    if 'user' in session:
        if session['roll']== "1":
            return render_template ("crearPublicacion.html")
        elif session['roll']== "2":
            return redirect("/admin")
        elif session['roll']== "3":
            return redirect("/admin")
        else:
            return "no se encontro tu roll"
    else:
       return redirect("/")
    
  
# =============crear publicacion=============
@app.route("/crear_publicacion",methods=["POST"])
def crearpublicacion():
    if session['user']:
        nom=session['user']
        titulo=escape(request.values["tituloptxt"])
        img=request.files["img-uploader"]
        nom_img=img.filename
        descricion=escape(request.values["destxt"])
        now=datetime.now()
        tiempo=now.strftime("%Y%H%M%S")+"_"
        fecha=tiempo
        with sqlite3.connect("basedatos(1).db") as con:
            con.row_factory=sqlite3.Row
            cur=con.cursor()

            cur.execute("SELECT id_usu FROM  usuario where nom_usu=? ",[nom])
            con.commit()        
            row=cur.fetchone()
            print(row['id_usu'])
            id_us=row['id_usu']

            if img.filename!=" ":
                nuv_nom_Fot=tiempo+nom_img
                img.save(("imagenes/"+nuv_nom_Fot))  

            cur.execute("INSERT INTO publicacion (nom_publi,imagen,contenido_publi,fecha_publi,id_usu) VALUES (?,?,?,?,?)",[titulo,nuv_nom_Fot,descricion,fecha,id_us])
            con.commit()    
            
            
            flash("se ha creado exitosamente tu publicación")
            return redirect("/crearpublicacion")
    else:
        return redirect("/")
    # ============configuracion ============

 
@app.route("/configuracion",methods=["GET","POST"])
def configuracion():
    if 'user' in session:
             return render_template ("configuracion.html")
    else:
        return redirect("/")
     

    # ============configuracion usuario============
@app.route("/configuracion/usuario",methods=["GET","POST"])
def configuracionUsu():
    nom_usu_A=escape(request.values["tANomusu"])
    nom_usu_N=escape(request.values["tNNomusu"])
    nom=escape(request.values["tNom"])
    correo=escape(request.values["tcorreo"])
    numero=escape(request.values["tnumero"])
    # crear numbre de usuario antiguo
    with sqlite3.connect("basedatos(1).db") as con:
        con.row_factory=sqlite3.Row #lista de diccionario
        # crea un cursor para poder hacer manipulacion a la base de datos
        cur=con.cursor()
        cur.execute("SELECT * FROM usuario WHERE nom_usu=?",[ nom_usu_A])
        row=cur.fetchone()
        if row['nom_usu']== nom_usu_A:
            cur.execute("UPDATE usuario  SET  nombre=?, correo=?, numero=? ,nom_usu=? WHERE nom_usu=?",[nom,correo,numero,nom_usu_N,nom_usu_A])
            con.commit()
            flash("sus datos han sido actializados exitosamente")
            return redirect("/configuracion")
        else:
            request.values["tANomusu"]=""
            request.values["tNNomusu"]=""
            request.values["tNom"]=""
            request.values["tcorreo"]=""
            request.values["tnumero"]=""
            flash("ERROR sus datos no fueron guardados exitosamente")
            return redirect("/configuracion")

# ===========configutacion contrasena==================

@app.route("/configuracion/contraseña",methods=["POST"])
def configuracionContra():
    cont_A=escape(request.values["tAcon"])
    nom_usu=escape(request.values["tnomusu"])
    contra_N=escape(request.values["tNcon"])
    ccontra_RN=escape(request.values["tNRcon"])
    encrip = hashlib.sha256(cont_A.encode('utf-8'))
    pass_enc = encrip.hexdigest()
    with sqlite3.connect("basedatos(1).db") as con:
        #Cambiar Contraseña
        con.row_factory=sqlite3.Row #lista de diccionario
                # crea un cursor para manipular la base de datos
        cur=con.cursor()
                #prepara sentencia SQL, preferiblemente no concatenar
        cur.execute("SELECT * FROM usuario WHERE nom_usu=?",[nom_usu])
        row=cur.fetchone()
        if row==None:
            flash( "ERROR Contraseña invalida")
            return redirect("/configuracion")
        elif row['contraseña']== pass_enc:
            if contra_N == ccontra_RN:
                cont_A=contra_N
                encrip = hashlib.sha256(cont_A.encode('utf-8'))
                pass_enc = encrip.hexdigest()
                cur.execute("UPDATE usuario SET contraseña =? WHERE nom_usu=?",[pass_enc,nom_usu])
                con.commit()
                flash("sucontraseña fue exitosamente actualizada")
                return redirect("/configuracion")
            else:
                contra_N=""
                ccontra_RN=""
                flash("ERROR Contraseña invalida")
                return redirect("/configuracion")
        else:
            flash("ERROR Contraseña invalida")
            return redirect("/configuracion")

    # ===========buscar usuario===================

@app.route("/buscar/Usu",methods=["GET","POST"])
def buscar_usu():
    return render_template ("buscarUsuario.html")
# ======================buscar publicacion========

@app.route("/buscar/publi",methods=["GET","POST"])
def buscar_public():
    if 'user' in session:
        return render_template ("buscarPublicacion.html")
    else:
        return redirect("/")
        

@app.route("/mensajes",methods=["GET","POST"])
def m_u():
    if 'user' in session:
        return render_template ("mensajeria.html")
    else:
        return redirect("/")
        
# =============mensajes de usuario===============
    
@app.route("/mensajes/Usu",methods=["GET","POST"])
def mensajesUsu():
    nom_usu_ori=escape(request.values["tONomusu"])
    nom_usu_des=escape(request.values["tDNomusu"])
    hora=escape(request.values["date"])
    cont_msj=escape(request.values["tContmsj"])
    with sqlite3.connect("basedatos(1).db") as con:
        con.row_factory=sqlite3.Row
        curso=con.cursor()
        row=curso.fetchone()
        if row['nom_usu']== nom_usu_ori:
            curso.execute("INTO FROM mensaje SET nom_usu_ori=?, nom_us_des=?, hora_msj=?, cont_msj=? WHERE nom_usu_ori=?",[nom_usu_ori, nom_usu_des, hora, cont_msj])
            con.commit()
            return("/instagram2/instagram2/templates/mensajeria.html/mensajes/Usu")
        else:
            request.values["tONomusu"]=""
            request.values["tDNomusu"]=""
            request.values["date"]=""
            request.values["tContmsj"]=""
            return("/instagram2/instagram2/templates/mensajeria.html/mensajes/Usu")

# ELIMINACION DE MENSAJES
@app.route("/eliminarMensajes",methods=["GET", "POST"])
def mensajes_eliminar():
    cont_msj=escape(request.values["tContmsj"])
    
    with sqlite3.connect("basedatos(1).db") as con:
            curso = con.cursor()
            curso.execute("DELETE FROM mensajes WHERE cont_msj = ?", [cont_msj])
            con.commit()
            return("/instagram2/instagram2/templates/mensajeria.html")
    return("No se puede eliminar el mensaje")
# CERRAR SESION
@app.route("/logout",methods=["GET","POST"])
def loguot():
    session.clear()
    return redirect ("/")


app.run(debug=True)

