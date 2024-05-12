__author__ = 'Aman Umrao'

from flask import Flask ,render_template,request,url_for
import matplotlib.pyplot as plt
import numpy as np
app=Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')
@app.route('/average',methods=['GET','POST'])
def average():
    x=''
    if request.method=='GET':
        return render_template('avg.html',source=str(x))
    elif request.method=='POST':
        x=str(request.form['values'])
        try:

            l=str(x).split()
            l=list(map(float,l))

            return render_template('avg.html',source='Average of '+x+' is '+str(sum(l)/len(l)))
        except :
            return render_template('avg.html',source='Input in Improper Format!')
    else :
        return 'Invalid Request'



@app.route('/aboutme')
def aboutme():
    return render_template('aboutme.html')
@app.route('/aman')
def aman():
    return render_template('aman.html')
@app.route('/graph',methods=['GET','POST'])
def graph():
    from matplotlib import pyplot as plt
    from random import randint
    class Interpolate:

        def solve(self,A,B,method):
            if(method=="newton"):
                return (self.Newton(A,B))
            else:
                return (self.Lagrange(A,B))

        def plot(self,coeffs,A,B):
            coeffs.reverse()
            def f(x):
                order,sum=len(coeffs)-1,0
                for i in range(order+1):
                    sum+=(coeffs[i]*(x**(order-i)))
                return sum
            n=int((max(A)-min(A)+2)/0.001)
            x_values=[min(A)-1]
            for i in range(1,n):
                x_values.append(float(str(x_values[0]+(0.001*i))[:5]))
            x_values.append(max(A)+1)
            y_values=[f(x) for x in x_values]
            plt.plot(x_values,y_values,A,B,'r o')
            for x,y in zip(A,B):
                plt.text(x,y,"(%d,%d)"%(x,y),fontsize=12)
            plt.xlabel("x - axis",fontsize=20)
            plt.ylabel("y - axis",fontsize=20)
            plt.title("INTERPOLATION - RESULT",fontsize=30)
            s1=str(randint(0,1000))
            s2=str(randint(0,1000))
            s3=str(randint(0,1000))
            s="static/fig"+s1+s2+s3+".png"
            plt.savefig(s)
            return s
        def Lagrange(self,A,B):

            from numpy import array
            from numpy.polynomial import polynomial as P
            n=len(A)
            w=(-1*A[0],1)
            for i in range(1,n):
                w=P.polymul(w,(-1*A[i],1))
            result=array([0.0 for i in range(len(w)-1)])
            derivative=P.polyder(w)
            for i in range(n):
                result+=(P.polydiv(w,(-1*A[i],1))[0]*B[i])/P.polyval(A[i],derivative)
            s=self.plot(list(result),A,B)
            return s

        def Newton(self,A,B):

            from numpy import array
            from numpy.polynomial import polynomial as P
            n=len(A)
            mat=[[0.0 for i in range(n)] for j in range(n)]
            for i in range(n):
                mat[i][0]=B[i]
            for i in range(1,n):
                for j in range(n-i):
                    mat[j][i]=(mat[j+1][i-1]-mat[j][i-1])/(A[j+i]-A[j])
            res=array((mat[0][0],))
            for i in range(1,n):
                prod=(-1*A[0],1)

                for j in range(1,i):
                    prod=P.polymul(prod,(-1*A[j],1))
                res=P.polyadd(res,array(prod)*mat[0][i])
            s=self.plot(list(res),A,B)
            return s

    x=''
    if request.method=='GET':
        return render_template('graphg.html',y=str(x))
    elif request.method=='POST':
        x1=str(request.form['x-vals'])
        x2=str(request.form['y-vals'])
        x3=str(request.form['method'])
        l1=x1.split()
        l1=[int(i) for i in l1]
        l2=x2.split()
        l2=[int(j) for j in l2]
        ip=Interpolate()
        s=ip.solve(l1,l2,x3)

        return render_template('graph.html',source=s,y='problem in displaying')
    else:
        return 'Invalid Request'


if __name__== '__main__' :

    app.run()
