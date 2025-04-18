from flask import Flask, render_template, request, session
import random
from itertools import chain, combinations

app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'


a=1

@app.route('/')
def index():
  return render_template("index.html")




rationals=[]
for i in range(50):
  for j in range(50):
    if i!=0 and j/i not in rationals:
      rationals.append(j/i)
      rationals.append(-j/i)

@app.route("/")
def goback():
  return render_template("index.html")

@app.route("/polysolver")
def polysolver():
  return render_template("polysolver.html")

@app.route("/baseconv")
def baseconv():
  return render_template("baseconv.html")
  
@app.route("/brawl_stars_fr")
def gobrawlstars():
  return render_template("brawl_stars_fr.html")

@app.route("/votingandstuff")
def govoting():
  return render_template("votingandstuff.html")

@app.route("/polypractice")
def gopolypractice():
  session["numberthings"]=[]
  session["totalthings"]=0
  session["listthings"]=[]
  session["turnnumber"]=0
  session["coeffs"]=[]
  session["storepoly"]=""
  session["phrase"]="Please input the degree of polynomial that you want to practice. For now: only 2 and 3 are available."
  return render_template("polypractice.html")
  
# @app.route("/chompbetter")
# def gochomp():
#   return render_template("chompbetter.html")

# @app.route("/geolol")
# def gogeolol():
#   return render_template("geolol.html")

# @app.route("/mathinfo")
# def mathinfo():
#   return render_template("mathinfo.html")

@app.route("/nim", methods=["GET", "POST"])
def gonim():
  session["playnum"] = 0
  session["l1"] = [i for i in range(random.randint(1, 10))]
  session["l2"] = [i for i in range(random.randint(1, 10))]
  session["l3"] = [i for i in range(random.randint(1, 10))]
  return render_template("nim.html", list1=session["l1"], list2=session["l2"], list3=session["l3"])


@app.route("/playnim", methods=["GET", "POST"])
def playnim():
    try:
        session["playnum"] += 1

        # Player move
        list_removed = int(request.form["listremove"])
        number_remove = int(request.form["numberremove"])

        if list_removed == 1:
            session["l1"] = session["l1"][:-number_remove]
        elif list_removed == 2:
            session["l2"] = session["l2"][:-number_remove]
        elif list_removed == 3:
            session["l3"] = session["l3"][:-number_remove]
        else:
            return render_template("nim.html", list1=session["l1"], list2=session["l2"], list3=session["l3"], message="Invalid list selection")

        # Check if player has won
        if not session["l1"] and not session["l2"] and not session["l3"]:
            return render_template("nim.html", list1=session["l1"], list2=session["l2"], list3=session["l3"], message="Player wins!")

        # Computer move
        if session["l1"] or session["l2"] or session["l3"]:
            lchoice = random.choice([i for i in range(1, 4) if len(session[f"l{i}"]) > 0])
            remove = random.randint(1, len(session[f"l{lchoice}"]))
            session[f"l{lchoice}"] = session[f"l{lchoice}"][:-remove]

        # Check if computer has won
        if not session["l1"] and not session["l2"] and not session["l3"]:
            return render_template("nim.html", list1=session["l1"], list2=session["l2"], list3=session["l3"], message="Computer wins!")

        return render_template("nim.html", list1=session["l1"], list2=session["l2"], list3=session["l3"], message="")

    except Exception as e:
        return render_template("nim.html", list1=session.get("l1", []), list2=session.get("l2", []), list3=session.get("l3", []), message=f"An error occurred: {e}")

    if __name__ == "__main__":
      app.run(debug=True)

@app.route("/polysolve", methods=["GET", "POST"])
def polysolve():
  c4=float(request.form["c4"])
  c3=float(request.form["c3"])
  c2=float(request.form["c2"])
  c1=float(request.form["c1"])
  c0=float(request.form["c0"])
  z=0
  phrase=""
  for i in rationals:
    if float(c4)*i**4+float(c3)*i**3+float(c2)*i**2+float(c1)*i+float(c0) > -0.00000001 and float(c4)*i**4+float(c3)*i**3+float(c2)*i**2+float(c1)*i+float(c0) < 0.00000001:
      phrase+=str(i) + " is a root. \n"
      z=z+1
  phrase+="There are " + str(z)+ " simple and possibly inaccurate rational roots of this polynomial that are easily findable with Python."
  return render_template("polysolver.html", phrase=phrase)

  
@app.route("/baseconving", methods=["GET", "POST"])
def baseconving():
  a=int(request.form["base"])
  b=int(request.form["number"])
  if a>36:
    return render_template("baseconv.html", phrase="This base is too big for conventional stuff. Please choose a base between 1 and 36.")
  else:
    match1=[]
    i=0
    while a**(i+1)<b+1:
      i+=1
    str1="Your converted number: "
    for j in range(i, -1, -1):
      k=0
      while b-a**j>-1:
        b=b-a**j
        k+=1
      if k>9:
        k=chr(k+55).upper()
      str1=str1+str(k)
    return render_template("baseconv.html", thing=str1)
#note to self: do a thing with ord(goes to 96+letter value like a=97, to convert btwn large bases)
@app.route("/baseconving2", methods=["GET", "POST"])
def baseconving2():
  a=str(request.form["number2"])
  b=int(request.form["base2"])
  numconv=0
  for i in range(len(a)):
    if ord(a[i])<58:
      valnum=ord(a[i])-48
    else:
      valnum=ord(a[i])-55
    numconv+=valnum*b**(len(a)-i-1)
  return render_template("baseconv.html", thing2=numconv)
  
def powerset(iterable):
  s = list(iterable)
  return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))
  
@app.route("/polypracticing", methods=["GET", "POST"])
def polypracticing():
  session["turnnumber"]+=1
  if session["turnnumber"]==1:
  # session["numberthings"]+=1
    deg=request.form["deg"]
    ook=" "
    for i in range(int(deg)):
      a=random.randint(0,15)
      b=random.randint(1,3)
      if b==1:
        c=a
      else:
        c=0-a
      session["numberthings"].append(c)
      ook=ook+str(c)+" "
    plist=list(powerset(session["numberthings"]))
    plist1=[]
    for i in plist:
      reali=str(i)
      plistap=[]
      if len(reali)==2:
        plist1.append(plistap)
      elif len(reali)==4:
        reali=reali[1]
        plistap.append(reali)
        plist1.append(plistap)
      else:
        modifi=reali[1:len(reali)-1]
        listifi=modifi.split(',')
        if "" in listifi:
          listifi.remove("")
        plist1.append(listifi)
    for i in range(int(deg)+1):
      sum=0
      for j in plist1:
        prod=1
        if len(j)==i:
          for k in range(len(j)):
            if " " in j[k]:
              j[k]=j[k].replace(" ","")
            if j[k]!="":
              prod=prod*int(j[k])
          sum+=prod
      session["coeffs"].append(sum)
    rphrase="Factor "
    for i in range(len(session["coeffs"])):
      if session["coeffs"][i]!=0:
        if i!=len(session["coeffs"])-1:
          rphrase+=str(session["coeffs"][i])+"x^"+str(len(session["coeffs"])-i-1)
        else:
          rphrase+=str(session["coeffs"][i])
      if (len(session["coeffs"])-i)%2==0:
        rphrase+="-"
      else:
        rphrase+="+"
    if "--" in rphrase:
      rphrase=rphrase.replace("--","+")
    if "+-" in rphrase:
      rphrase=rphrase.replace("+-","-")
    session["storepoly"]=rphrase
    return render_template("polypractice.html", phrase=rphrase)
  else:
    root1=int(request.form["root1"])
    if root1 in session["numberthings"]:
      session["numberthings"].remove(root1)
      if len(session["numberthings"])>0:
        phrases="Correct. "+str(root1)+" is a root. Enter another root. The polynomial: "+session["storepoly"]
      else:
        phrases="All roots correct! Good job!"
    else:
      phrases="Incorrect. "+str(root1)+" is not a root. Enter another root. The polynomial: " + session["storepoly"]
    return render_template("polypractice.html", phrase=phrases)
    


app.run(host='0.0.0.0', port=81)
