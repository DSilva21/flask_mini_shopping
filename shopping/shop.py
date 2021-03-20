from flask import Flask, render_template, request,session,redirect,url_for

app = Flask(__name__)
app.secret_key=b'1234'
app.jinja_env.filters['zip'] = zip

import mysql 
import mysql.connector
import glob

dbconfig={'host':'localhost','user':'root','password':'','database':'shop'}
conn=mysql.connector.connect(**dbconfig)
cursor=conn.cursor()

@app.route("/")
def show_category()->'html':
    #쇼핑몰 카테고리 출력
    #1: 전자기기  2:식료품  3:의류
    SQL="SELECT DISTINCT p_category FROM product"
    cursor.execute(SQL)
    data=cursor.fetchall()

    product_list=[]
    table_name=["전자기기","식료품","의류"]
    image_list=[]
    cnt=0

    #카테고리 별로 product_list에 저장
    for i in data:
        SQL="SELECT *FROM product WHERE p_category=%s"
        cursor.execute(SQL,i)
        c=cursor.fetchall()
        product_list.append(c)
    
    SQL="SELECT *FROM product"
    cursor.execute(SQL)
    data=cursor.fetchall()

    #이미지리스트 별도로저장 (이미지 경로를 한꺼번에 저장)
    for i in range(len(data)):
        p_image=data[cnt][5]
        temp_String="image/"+p_image+".jpg"
        image_file=url_for('static',filename=temp_String)
        image_list.append(image_file)
        cnt+=1   

    return render_template("show_category.html", data=product_list,head=table_name,zip=zip)


@app.route('/product_info/',methods=["GET"])
def info()->'html':
    name=request.args.get('no')
    SQL="SELECT *FROM product WHERE p_name=%s"  
    cursor.execute(SQL,(name,))
    data=cursor.fetchall()

    p_image=data[0][5]
    temp_String="image/"+p_image+".jpg"
    image_file=url_for('static',filename=temp_String)

    return render_template("product.html",data=data,image_file=image_file)

@app.route('/category/',methods=["GET"])
def cate()->'html':
    #해당하는 카테고리만 출력
    table_name=["전자기기","식료품","의류"]
    name=request.args.get('no')
    cnt=0
    for i in table_name:
        if name==i:
            idx=cnt+1
        cnt+=1

    print(idx)
    SQL="SELECT *FROM product WHERE p_category=%s"  
    cursor.execute(SQL,(idx,))
    data=cursor.fetchall()
    print(data)
    return render_template("category.html",data=data,head=name)

app.run(debug=True)