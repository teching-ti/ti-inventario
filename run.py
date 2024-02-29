from app import app

if __name__== 'main':
    #esta línea solo sirve en el servidor local, debera eliminarse el modo debug al se subido a producción
    app.run(debug=True)