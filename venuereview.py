from flask import Flask,render_template,request,redirect,url_for
from DBConnection import Db
app = Flask(__name__)
venuepicpath="C:\\Users\\SSD\\PycharmProjects\\venuereview\\static\\venuepic\\"

@app.route('/')
def login():
    return render_template('admin/LOGIN.html')

@app.route('/login',methods=['post'])
def loginpost():
    username=request.form['textfield']
    pswd=request.form['textfield2']
    db=Db()
    res=db.selectOne("select *from login where username='"+username+"' and password='"+pswd+"'")
    if res!=None:
        return redirect(url_for('adminhome'))
    else:
        return '<script>alert ("invalid username or password");window.location="/";</script>'
@app.route('/adminhome')
def adminhome():
    return render_template('admin/adminhome.html')

@app.route('/admin_add_category')
def admin_add_category():
    return render_template('admin/Addcat.html')
@app.route('/admin_add_categorypost',methods=['post'])
def admin_add_categorypost():
    category=request.form['textfield']
    db = Db()
    db.insert("INSERT INTO category values (NULL ,'"+category+"')")
    return '<script>alert ("success");window.location="/adminhome";</script>'

@app.route('/admin_add_venue')
def admin_add_venue():
    db=Db()
    res=db.select("select * from category")
    return render_template('admin/Addvenue.html',data=res)
@app.route('/admin_add_venuepost',methods=['post'])
def admin_add_venuepost():
    venue=request.form['textfield']
    category = request.form['select']
    description = request.form['textarea']
    latitude = request.form['textfield2']
    longitude = request.form['textfield3']
    pic=request.files['pic']
    pic.save(venuepicpath+pic.filename)
    db = Db()
    db.insert("insert into venue (vname,cid,image,description,latitude,longitude)values ('"+venue+"','"+category+"','"+pic.filename+"','"+description+"','"+latitude+"','"+longitude+"')")

    return '<script>alert ("success");window.location="/adminhome";</script>'

@app.route('/admin_category_manage')
def admin_category_manage():
    return render_template('admin/EDIT_CATEGORY.html')
@app.route('/admin_category_managepost',methods=['post'])
def admin_category_managepost():
    category=request.form['textfield']
    return render_template('admin/admin_category_manage.html')


@app.route('/admin_reviews')
def admin_reviews():
    db = Db()
    res = db.select("select category.*,venue.* from category,venue where venue.cid=category.cid")
    if len(res) > 0:
        return render_template('admin/VIEW VENUE1.html', data=res)
    else:
        return '<script>alert ("no data");window.location="/adminhome";</script>'
@app.route('/view_review/<id>')
def view_review(id):
    db = Db()
    res = db.select("select review.*,user.* from review,user where review.uid=user.ulid and review.vid='"+id+"'")
    if len(res) > 0:
        return render_template('admin/REVIEWS.html', data=res)
    else:
        return '<script>alert ("no data");window.location="/adminhome";</script>'
@app.route('/admin_search')
def admin_search():
    return render_template('admin/search.html')

@app.route('/admin_venue_manage')
def admin_venue_manage():
    return render_template('admin/VENUE MANAGEMENT.html')
@app.route('/admin_venue_managepost',methods=['post'])
def admin_venue_managepost():
    venue=request.form['textfield']
    category=request.form['select']
    description=request.form['textarea']
    latitude=request.form['textfield2']
    longitude=request.form['textfield3']
    return render_template('admin/VENUE MANAGEMENT.html')

@app.route('/admin_view_users')
def admin_view_users():
    db = Db()
    res = db.select("select *from user")
    if len(res) >0:
        return render_template('admin/VIEWUSERS.html',data=res)
    else:
        return '<script>alert ("no data");window.location="/adminhome";</script>'



@app.route('/admin_view_venue')
def admin_view_venue():
    db = Db()
    res = db.select("select category.*,venue.* from category,venue where venue.cid=category.cid")
    if len(res) > 0:
        return render_template('admin/VIEW VENUE.html',data=res)
    else:
        return '<script>alert ("no data");window.location="/adminhome";</script>'

@app.route('/admin_delete_venue/<id>')
def admin_delete_venue(id):
    db=Db()
    res=db.delete("delete from venue where vid='"+id+"'")
    return '<script>alert ("deleted");window.location="/adminhome";</script>'

@app.route('/admin_view_cat')
def admin_view_cat():
    db=Db()
    res=db.select("select *from category")
    if len(res)>0:
       return render_template('admin/VIEW CAT.html',data=res)
    else:
        return '<script>alert ("no data");window.location="/adminhome";</script>'
@app.route('/admin_delete_cat/<id>')
def admin_delete_cat(id):
    db=Db()
    res=db.delete("delete from category where cid='"+id+"'")
    return '<script>alert ("deleted");window.location="/adminhome";</script>'
if __name__ == '__main__':
    app.run()
