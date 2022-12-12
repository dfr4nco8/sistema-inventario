import cx_Oracle
from flask import Flask, render_template, redirect, request, url_for, make_response, flash

conexion = cx_Oracle.connect(
user='dcfrancor',
password='dcfrancor',
dsn='localhost/xe')


app = Flask(__name__)




@app.route('/', methods = ['POST','GET'])
def inicio():
    resp=make_response(render_template('index.html'))
    resp.set_cookie('usuario', '0')
    resp.set_cookie('name_user','0')
    return resp

@app.route('/home', methods = ['POST','GET'])
def home():
    
    cur_01=conexion.cursor()
    select_numprov= "SELECT * FROM PROVEEDOR"
    select_numcli= "SELECT * FROM CLIENTE"
    select_numprod="SELECT * FROM PROD"
    select_numvent="SELECT * FROM ORDEN"
    select_numvend="SELECT * FROM VENDEDOR"
    cur_01.execute(select_numprov)
    resultado_tamprov=len(cur_01.fetchall())
    cur_01.execute(select_numcli)
    resultado_tamcli=len(cur_01.fetchall())
    cur_01.execute(select_numprod)
    resultado_tamprod=len(cur_01.fetchall())
    cur_01.execute(select_numvent)
    resultado_tamvent=len(cur_01.fetchall())
    cur_01.execute(select_numvend)
    resultado_tamvend=len(cur_01.fetchall())
    numprov=str(resultado_tamprov)
    numcli=str(resultado_tamcli)
    numprod=str(resultado_tamprod)
    numvent=str(resultado_tamvent)
    numvend=str(resultado_tamvend)
    resp = make_response(render_template('home.html',numprov=numprov, numcli=numcli, numprod=numprod, numvent=numvent, numvend=numvend))
    return resp

@app.route('/prov', methods = ['POST','GET'])
def prov():
    cur_01=conexion.cursor()
    select_prov= "SELECT * FROM PROVEEDOR"
    cur_01.execute(select_prov)
    resultados=cur_01.fetchall()

    resultadosjson=[]
    for resultado in resultados: 
        resultadosjson.append({
            "nit":resultado[0],
            "nombre":resultado[1],
            "telefono":resultado[2],
            "direccion":resultado[3],
            "ciudad":resultado[4]
        })

    return render_template('prov.html',resultados=resultadosjson)


@app.route('/agreprov', methods = ['POST','GET'])
def agreprov():
    if request.method == 'POST':
        nit = request.form['nit']
        nombre_prov = request.form['nombre_prov']
        telefono_prov= request.form['telefono_prov']
        direccion_prov= request.form['direccion_prov']
        ciudad_prov=request.form['ciudad_prov']
        print(nit,nombre_prov,telefono_prov,direccion_prov,ciudad_prov)
        cur_01=conexion.cursor()
        insert_datos= "insert into proveedor (nit, nombre_prov, telefono_prov, direccion_prov, ciudad_prov) VALUES (:1, :2, :3, :4, :5)"
        print(insert_datos)
        cur_01.execute(insert_datos,[nit, nombre_prov, telefono_prov, direccion_prov, ciudad_prov])
        conexion.commit()

    return render_template('agreprov.html')

@app.route('/modprov', methods = ['POST','GET'])
def modprov():
    resultadosjson={
                    "Nit":"nit",
                    "Nombre":"nombre",
                    "Telefono":"telefono",
                    "Direccion":"direccion",
                    "Ciudad":"ciudad",          
                    }
    

    if request.method == 'POST':
        nit=request.form['nit']
        nombre = request.form['nombre_prov']
        telefono = request.form['telefono_prov']
        direccion=request.form['direccion_prov']
        ciudad=request.form['ciudad_prov']
        update_proveedor='UPDATE proveedor set '
        update_proveedor_bool=False
        update_proveedor_atributos=[]

        if nombre and nombre!='':
                update_proveedor_bool=True
                update_proveedor_atributos.append("nombre_prov='"+nombre+"'")
        if telefono and telefono!='':
                update_proveedor_bool=True
                update_proveedor_atributos.append("telefono_prov='"+telefono+"'")
        if direccion and direccion!='':
                update_proveedor_bool=True
                update_proveedor_atributos.append("direccion_prov='"+direccion+"'")
        if ciudad and ciudad!='':
                update_proveedor_bool=True
                update_proveedor_atributos.append("ciudad_prov='"+ciudad+"'")
        cur_01=conexion.cursor()
        if update_proveedor_bool:
                update_proveedor=update_proveedor+','.join(update_proveedor_atributos)+" Where nit = "+nit
                print(update_proveedor)
                cur_01.execute(update_proveedor)
                conexion.commit()
        return render_template('modprov.html',form=resultadosjson)

    elif request.method=='GET':
        cur_01=conexion.cursor()
        select_proveedor= "SELECT * FROM PROVEEDOR"
        cur_01.execute(select_proveedor)
        resultadosprov=cur_01.fetchall()

        resultadosprovjson=[]
        for r in resultadosprov: 
            resultadosprovjson.append({
                "nit":r[0],
                "nombre":r[1],
                "telefono":r[2],
                "direccion":r[3],
                "ciudad":r[4]
            })
        return render_template('modprov.html',resultadosprov=resultadosprovjson)



@app.route('/clien', methods = ['POST','GET'])
def clien():
    cur_01=conexion.cursor()
    select_clien= "SELECT * FROM CLIENTE"
    cur_01.execute(select_clien)
    resultados=cur_01.fetchall()

    resultadosjson=[]
    for resultado in resultados: 
        resultadosjson.append({
            "id":resultado[0],
            "nombre":resultado[1],
            "telefono":resultado[2]
        })

    return render_template('clien.html',resultados=resultadosjson)

@app.route('/index', methods = ['POST','GET'])
def iniciolog():
    return render_template('home.html')

@app.route('/agreclien', methods = ['POST','ET'])
def agreclien():
    if request.method == 'POST':
        id_cliente = request.form['id_cliente']
        nombre_cli = request.form['nombre_cli']
        telefono= request.form['telefono']
    
        print(id_cliente,nombre_cli,telefono)
        cur_01=conexion.cursor()
        insert_datos= "insert into cliente (id_cliente, nombre_cli, telefono) VALUES (:1, :2, :3)"
        print(insert_datos)
        cur_01.execute(insert_datos,[id_cliente, nombre_cli, telefono])
        conexion.commit()
 

    return render_template('agreclien.html')

@app.route('/modclien', methods = ['POST','GET'])
def modclien():
    resultadosjson={
                    "Id":"id_cliente",
                    "Nombre":"nombre_cli",
                    "Telefono":"telefono",         
                    }
    

    if request.method == 'POST':
        id=request.form['id_cliente']
        nombre = request.form['nombre_cli']
        telefono = request.form['telefono']
        update_cliente='UPDATE cliente set '
        update_cliente_bool=False
        update_cliente_atributos=[]

        if nombre and nombre!='':
                update_cliente_bool=True
                update_cliente_atributos.append("nombre_cli='"+nombre+"'")
        if telefono and telefono!='':
                update_cliente_bool=True
                update_cliente_atributos.append("telefono='"+telefono+"'")
        cur_01=conexion.cursor()
        if update_cliente_bool:
                update_cliente=update_cliente+','.join(update_cliente_atributos)+" Where id_cliente = "+id
                print(update_cliente)
                cur_01.execute(update_cliente)
                conexion.commit()
        return render_template('modclien.html',form=resultadosjson)

    elif request.method=='GET':
        cur_01=conexion.cursor()
        select_cliente= "SELECT * FROM CLIENTE"
        cur_01.execute(select_cliente)
        resultadosprov=cur_01.fetchall()

        resultadosprovjson=[]
        for r in resultadosprov: 
            resultadosprovjson.append({
                "id":r[0],
                "nombre":r[1],
                "telefono":r[2],
            })
        return render_template('modclien.html',resultadosprov=resultadosprovjson)

@app.route('/vent', methods = ['POST','GET'])
def vent():
    if request.method == 'POST':
        cons = request.form['consecutivo_ord']
        fecha=request.form['fecha_ord'].replace('-','/')
        vendedor = request.form['vendedor_id']
        cliente = request.form['cliente_id']
        producto=request.form['prod_id']
        cantidad=request.form['cantidad_det']
        precio = request.form['precio_det']
        fila = request.form['id_detalle']

        print(cons,fecha,vendedor,cliente,producto,cantidad,precio)

        cur_01=conexion.cursor()
        insert_ord= "insert into orden (consecutivo_ord, fecha_ord, precio_total_ord, vendedor_id, cliente_id) VALUES (:1, TO_DATE(:2, 'yyyy/mm/dd'), :3, :4, :5)"
        print(insert_ord)
        cur_01.execute(insert_ord,[cons, fecha, precio, vendedor, cliente])
        conexion.commit()
        cur_01=conexion.cursor()
        insert_det= "insert into detalle (id_detalle, cantidad_det, precio_det, prod_id, consecutivo_ord) VALUES (:1, :2, :3, :4, :5)"
        print(insert_det)
        cur_01.execute(insert_det,[fila, cantidad, precio, producto, cons])
        conexion.commit()
        return render_template('vent.html')

    elif request.method=='GET':
        cur_01=conexion.cursor()
        select_ord= "SELECT * FROM DETALLE"
        cur_01.execute(select_ord)
        resultadosprov=cur_01.fetchall()

        resultadosprovjson=[]
        for r in resultadosprov: 
            resultadosprovjson.append({
                "id":r[0],
                "cantidad":r[1],
                "precio":r[2],
                "producto":r[3],
                "cons":r[4],
            })
        return render_template('vent.html',resultadosprov=resultadosprovjson)

    

@app.route('/consvent', methods = ['POST','GET'])
def consvent():
    cur_01=conexion.cursor()
    select_clien= "SELECT * FROM ORDEN"
    cur_01.execute(select_clien)
    resultados=cur_01.fetchall()
    print(resultados)

    resultadosjson=[]
    for resultado in resultados: 
        resultadosjson.append({
            "cons":resultado[0],
            "fecha":resultado[1],
            "vendedor":resultado[3],
            "cliente":resultado[4],
        })

    return render_template('consvent.html',resultados=resultadosjson)


@app.route('/prod', methods = ['POST','GET'])
def prod():
    cur_01=conexion.cursor()
    select_prod= "SELECT * FROM PROD"
    cur_01.execute(select_prod)
    resultados=cur_01.fetchall()

    resultadosjson=[]
    for resultado in resultados: 
        resultadosjson.append({
            "id":resultado[0],
            "nombre":resultado[1],
            "precio":resultado[2],
            "lote":resultado[3],
            "fabricante":resultado[4],
            "proveedor":resultado[5]
        })

    return render_template('prod.html',resultados=resultadosjson)

@app.route('/agreprod', methods = ['POST','GET'])
def agreprod():
    if request.method == 'POST':
        id = request.form['id_prod']
        nombre = request.form['nombre']
        precio_compra= request.form['precio_compra']
        lote = request.form['lote']
        fabricante = request.form['fabricante_prod']
        proveedor = request.form['proveedor_prod']
    
        print(id,nombre,precio_compra, lote, fabricante, proveedor)
        cur_01=conexion.cursor()
        insert_datos= "insert into prod (id_prod, nombre, precio_compra, lote, fabricante_prod, proveedor_prod) VALUES (:1, :2, :3, :4, :5, :6)"
        print(insert_datos)
        cur_01.execute(insert_datos,[id, nombre, precio_compra, lote, fabricante, proveedor])
        conexion.commit()
 
    return render_template('agreprod.html')
    
@app.route('/modprod', methods = ['POST','GET'])
def modprod():
    resultadosjson={
                    "Id":"id_prod",
                    "Nombre":"nombre",
                    "Precio":"precio_compra",
                    "Lote":"lote",
                    "Fabricante":"fabricante_prod",
                    "Proveedor":"proveedor_prod",          
                    }
    

    if request.method == 'POST':
        id=request.form['id_prod']
        nombre = request.form['nombre']
        precio = request.form['precio_compra']
        lote = request.form['lote']
        fabricante = request.form['fabricante_prod']
        proveedor = request.form['proveedor_prod']
        update_proveedor='UPDATE prod set '
        update_proveedor_bool=False
        update_proveedor_atributos=[]

        if nombre and nombre!='':
                update_proveedor_bool=True
                update_proveedor_atributos.append("nombre='"+nombre+"'")
        if precio and precio!='':
                update_proveedor_bool=True
                update_proveedor_atributos.append("precio_compra='"+precio+"'")
        if lote and lote!='':
                update_proveedor_bool=True
                update_proveedor_atributos.append("lote='"+lote+"'")
        if fabricante and fabricante!='':
                update_proveedor_bool=True
                update_proveedor_atributos.append("fabricante_prod='"+fabricante+"'")
        if proveedor and proveedor!='':
                update_proveedor_bool=True
                update_proveedor_atributos.append("proveedor_prod='"+proveedor+"'")
        cur_01=conexion.cursor()
        if update_proveedor_bool:
                update_proveedor=update_proveedor+','.join(update_proveedor_atributos)+" Where id_prod = "+id
                print(update_proveedor)
                cur_01.execute(update_proveedor)
                conexion.commit()
        return render_template('modprod.html',form=resultadosjson)

    elif request.method=='GET':
        cur_01=conexion.cursor()
        select_proveedor= "SELECT * FROM PROD"
        cur_01.execute(select_proveedor)
        resultadosprov=cur_01.fetchall()

        resultadosprovjson=[]
        for r in resultadosprov: 
            resultadosprovjson.append({
                "id":r[0],
                "nombre":r[1],
                "precio":r[2],
                "lote":r[3],
                "fabricante":r[4],
                "proveedor":r[5]
            })
        return render_template('modprod.html',resultadosprov=resultadosprovjson)

@app.route('/eliprod', methods = ['POST','GET'])
def eliprod():
    resultadosjson={
                    "Id":"id_prod",
                    "Nombre":"nombre",
                    "Precio":"precio_compra",
                    "Lote":"lote",
                    "Fabricante":"fabricante_prod",
                    "Proveedor":"proveedor_prod",          
                    }
    

    if request.method == 'POST':
        id=request.form['id_prod']      

        cur_01=conexion.cursor()
        delete='DELETE from PROD where id_prod = '+id
        cur_01.execute(delete)
        conexion.commit()
        return render_template('eliprod.html')

    elif request.method=='GET':
        cur_01=conexion.cursor()
        select_proveedor= "SELECT * FROM PROD"
        cur_01.execute(select_proveedor)
        resultadosprov=cur_01.fetchall()

        resultadosprovjson=[]
        for r in resultadosprov: 
            resultadosprovjson.append({
                "id":r[0],
                "nombre":r[1],
                "precio":r[2],
                "lote":r[3],
                "fabricante":r[4],
                "proveedor":r[5]
            })
        return render_template('eliprod.html',resultadosprov=resultadosprovjson)

@app.route('/invent', methods = ['POST','GET'])
def invent():
    if request.method == 'POST':
        id = request.form['id_prod']
        nombre = request.form['nombre']
        precio_compra= request.form['precio_compra']
        lote = request.form['lote']
        fabricante = request.form['fabricante_prod']
        proveedor = request.form['proveedor_prod']
    
        print(id,nombre,precio_compra, lote, fabricante, proveedor)
        cur_01=conexion.cursor()
        insert_datos= "insert into prod (id_prod, nombre, precio_compra, lote, fabricante_prod, proveedor_prod) VALUES (:1, :2, :3, :4, :5, :6)"
        print(insert_datos)
        cur_01.execute(insert_datos,[id, nombre, precio_compra, lote, fabricante, proveedor])
        conexion.commit()
 
    return render_template('invent.html')

@app.route('/reginvent', methods = ['POST','GET'])
def reginvent():
    return render_template('reginvent.html')

if __name__ == '__main__':
    app.run(debug=True)