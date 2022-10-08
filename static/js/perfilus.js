
lista_Publicaciones={
    "comida":"publicacion1",
    "concierto":"publicacion2",
    "ropa":"publicacion3",
    "gato":"publicacion4"
    }
    lista_usuarios={
        "pedro":{"nombre": "pedro","usuario":"pedro23", "clave":"1234", "foto":"img","rol":"SuperAdmin"},
        "juan":{"nombre": "juan","usuario":"juan", "clave":"1234", "foto":"img","rol":"Admin"},
        "cesar":{"nombre": "Cesar","usuario":"cesar", "clave":"1234", "foto":"img","rol":"Admin"},
        "alejandra":{"nombre": "alejandra","usuario":"alejandra", "clave":"1234", "foto":"img","rol":"UsuarioFinal"},
        "camilo":{"nombre": "Camilo","usuario":"camilo", "clave":"1234", "foto":"img","rol":"UsuarioFinal"},
    }

function eliminar(id_publi){
    for (id_p  of lista_Publicaciones)
    if (id_p =id_publi)
    nom_publi= request.values["nomptxt"]
    cont_publi= request.values["cotptxt"]
    lista_Publicaciones.pop[nom_publi]= cont_publi;
    return render_template ("crearPublicacion.html")
}

        


function modificar(id_publi){
    for (id_p  of lista_Publicaciones)
    if (id_p =id_publi)
    nom_publi= request.values["nomptxt"]
    cont_publi= request.values["cotptxt"]
    lista_Publicaciones[nom_publi]= cont_publi;
    return render_template ("crearPublicacion.html")
    
}

