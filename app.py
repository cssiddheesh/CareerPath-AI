from flask import Flask, render_template, request, jsonify, session
import sqlite3, json, os, re

app = Flask(__name__)
app.secret_key = "careerpath-ai-demo-secret"
DB = os.path.join(os.path.dirname(__file__), "careerpath.db")

CAREERS = [
 {"name":"Software Developer","icon":"💻","desc":"Designs, builds and maintains software applications.","skills":["Python","Problem Solving","Logical Thinking","Programming","Communication"],"subjects":["Computer Science","Mathematics","Physics"],"courses":["B.Tech/B.E. Computer Science","BCA","B.Sc. Computer Science"],"jobs":["Software Developer","Web Developer","Application Developer"],"future":"Strong opportunities across software, web, mobile and enterprise technology.","weights":{"technology":5,"logical":5,"problem":4,"creativity":2,"communication":2,"leadership":1}},
 {"name":"Data Scientist","icon":"📊","desc":"Uses data, statistics and computing to discover patterns and support decisions.","skills":["Python","Statistics","Data Analysis","Logical Thinking","Problem Solving"],"subjects":["Mathematics","Computer Science","Statistics","Physics"],"courses":["B.Sc/B.Tech Data Science","B.Sc Statistics","B.Tech CSE + Data Science"],"jobs":["Data Scientist","Data Analyst","ML Analyst"],"future":"Growing opportunities in technology, finance, healthcare, research and business.","weights":{"technology":4,"logical":5,"problem":5,"creativity":1,"communication":2}},
 {"name":"AI/ML Engineer","icon":"🤖","desc":"Builds systems that learn from data and automate intelligent tasks.","skills":["Python","Machine Learning","Mathematics","Problem Solving","Data Analysis"],"subjects":["Mathematics","Computer Science","Physics"],"courses":["B.Tech CSE/AI & ML","B.Sc AI/Data Science","B.Tech Data Science"],"jobs":["ML Engineer","AI Engineer","Applied Scientist"],"future":"Rapidly expanding across automation, robotics, healthcare, finance and software.","weights":{"technology":5,"logical":5,"problem":5,"creativity":2,"math":5}},
 {"name":"Doctor","icon":"🩺","desc":"Diagnoses, treats and helps prevent illness while caring for patients.","skills":["Science","Communication","Empathy","Decision Making","Problem Solving"],"subjects":["Biology","Chemistry","Physics"],"courses":["MBBS","BDS","AYUSH programmes"],"jobs":["Doctor","Medical Officer","Clinical Specialist"],"future":"Healthcare continues to need trained professionals in clinical and specialised fields.","weights":{"science":5,"social":4,"communication":4,"problem":4,"empathy":5}},
 {"name":"Engineer","icon":"⚙️","desc":"Applies mathematics and science to design, build and improve systems.","skills":["Mathematics","Problem Solving","Logical Thinking","Technical Skills","Teamwork"],"subjects":["Mathematics","Physics","Chemistry"],"courses":["B.E./B.Tech","Diploma + Engineering pathway"],"jobs":["Mechanical Engineer","Civil Engineer","Electrical Engineer"],"future":"Broad opportunities in infrastructure, manufacturing, energy, electronics and technology.","weights":{"math":5,"logical":4,"problem":5,"technology":3,"creativity":3}},
 {"name":"Teacher","icon":"👩‍🏫","desc":"Helps learners understand concepts, develop skills and grow with confidence.","skills":["Communication","Patience","Leadership","Creativity","Subject Knowledge"],"subjects":["Any strong subject area","Education"],"courses":["B.Ed","Integrated B.A./B.Sc. B.Ed","Subject degree + teacher education"],"jobs":["School Teacher","Trainer","Academic Coordinator"],"future":"Opportunities in schools, training, educational technology and academic leadership.","weights":{"communication":5,"social":5,"leadership":4,"creativity":4,"empathy":5}},
 {"name":"Designer","icon":"🎨","desc":"Creates visual, digital or product experiences that solve user needs.","skills":["Creativity","Design Thinking","Communication","Digital Tools","Problem Solving"],"subjects":["Art","Computer Science","Design","English"],"courses":["B.Des","BFA","UI/UX or Design programmes"],"jobs":["UI/UX Designer","Graphic Designer","Product Designer"],"future":"Digital products, media, branding and user experience create diverse opportunities.","weights":{"creativity":5,"technology":3,"problem":4,"communication":4,"social":2}},
 {"name":"Entrepreneur","icon":"🚀","desc":"Creates and grows ventures by identifying problems and building solutions.","skills":["Leadership","Communication","Creativity","Decision Making","Problem Solving"],"subjects":["Business Studies","Economics","Mathematics","Computer Science"],"courses":["BBA","B.Com","BMS","Any degree + entrepreneurship"],"jobs":["Founder","Business Owner","Product Manager"],"future":"Opportunities depend on innovation, market needs, execution and business skills.","weights":{"leadership":5,"creativity":5,"communication":4,"problem":5,"social":3}},
 {"name":"Chartered Accountant","icon":"📈","desc":"Works with accounting, auditing, taxation, finance and business information.","skills":["Numerical Skills","Analysis","Attention to Detail","Ethics","Communication"],"subjects":["Accountancy","Mathematics","Economics","Business Studies"],"courses":["CA Foundation → CA Intermediate → CA Final","B.Com"],"jobs":["Chartered Accountant","Auditor","Tax Consultant","Financial Analyst"],"future":"Finance and compliance remain important across businesses and organisations.","weights":{"math":5,"logical":5,"business":5,"communication":2,"problem":3}},
 {"name":"Lawyer","icon":"⚖️","desc":"Interprets laws, builds arguments and helps clients understand legal issues.","skills":["Communication","Research","Critical Thinking","Reasoning","Persuasion"],"subjects":["English","Political Science","History","Economics"],"courses":["5-year integrated LL.B.","3-year LL.B. after graduation"],"jobs":["Advocate","Legal Consultant","Corporate Legal Professional"],"future":"Legal services span courts, companies, policy, compliance and public institutions.","weights":{"communication":5,"logical":4,"social":4,"problem":4,"leadership":3}},
 {"name":"Psychologist","icon":"🧠","desc":"Studies behaviour and supports people through evidence-based psychological practice.","skills":["Empathy","Communication","Observation","Research","Problem Solving"],"subjects":["Psychology","Biology","English","Social Science"],"courses":["B.A./B.Sc. Psychology","Master's and relevant professional training"],"jobs":["Psychology Professional","Counselling-related roles","Researcher"],"future":"Mental health, education, research and organisational settings offer varied pathways.","weights":{"empathy":5,"social":5,"communication":5,"science":2,"problem":3}},
 {"name":"Environmental Scientist","icon":"🌱","desc":"Studies environmental systems and develops solutions for sustainability challenges.","skills":["Science","Research","Problem Solving","Data Analysis","Communication"],"subjects":["Biology","Chemistry","Geography","Environmental Science"],"courses":["B.Sc Environmental Science","B.Sc/B.Tech related environmental programmes"],"jobs":["Environmental Scientist","Sustainability Analyst","Research Assistant"],"future":"Climate, conservation, sustainability and environmental regulation are expanding areas.","weights":{"science":5,"problem":4,"logical":3,"social":4,"creativity":2}},
 {"name":"Cybersecurity Specialist","icon":"🔐","desc":"Protects computers, networks and information from security threats.","skills":["Networking","Programming","Problem Solving","Logical Thinking","Attention to Detail"],"subjects":["Computer Science","Mathematics","Physics"],"courses":["B.Tech CSE/Cybersecurity","B.Sc Cybersecurity/Computer Science","Security certifications"],"jobs":["Security Analyst","SOC Analyst","Penetration Testing Professional"],"future":"Demand is driven by increasing digital services, connected systems and security needs.","weights":{"technology":5,"logical":5,"problem":5,"math":3,"creativity":2}}
]

def db():
    con=sqlite3.connect(DB)
    con.row_factory=sqlite3.Row
    return con

def init_db():
    con=db()
    con.execute("""CREATE TABLE IF NOT EXISTS students(
      id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER, grade TEXT,
      subjects TEXT, interests TEXT, hobbies TEXT, skills TEXT, strengths TEXT,
      work_style TEXT, goals TEXT, assessment TEXT, recommendations TEXT)""")
    con.execute("""CREATE TABLE IF NOT EXISTS careers(
      name TEXT PRIMARY KEY, description TEXT, skills TEXT, subjects TEXT,
      courses TEXT, jobs TEXT, future TEXT)""")
    for c in CAREERS:
        con.execute("""INSERT OR REPLACE INTO careers VALUES(?,?,?,?,?,?,?)""",
          (c["name"],c["desc"],json.dumps(c["skills"]),json.dumps(c["subjects"]),
           json.dumps(c["courses"]),json.dumps(c["jobs"]),c["future"]))
    con.commit(); con.close()

@app.route("/")
def home(): return render_template("index.html")

@app.route("/profile")
def profile(): return render_template("profile.html")

@app.route("/assessment")
def assessment(): return render_template("assessment.html")

@app.route("/explorer")
def explorer(): return render_template("explorer.html", careers=CAREERS)

@app.route("/dashboard")
def dashboard(): return render_template("dashboard.html")

@app.route("/api/profile", methods=["POST"])
def save_profile():
    data=request.json or {}
    session["student"]=data
    con=db()
    cur=con.execute("""INSERT INTO students
      (name,age,grade,subjects,interests,hobbies,skills,strengths,work_style,goals)
      VALUES(?,?,?,?,?,?,?,?,?,?)""",
      (data.get("name",""),data.get("age"),data.get("grade",""),
       data.get("subjects",""),data.get("interests",""),data.get("hobbies",""),
       data.get("skills",""),data.get("strengths",""),data.get("work_style",""),
       data.get("goals","")))
    session["student_id"]=cur.lastrowid
    con.commit(); con.close()
    return jsonify({"ok":True})

def score_careers(answers, profile):
    # Assessment answers are 1-5. Profile keywords add a small contextual signal.
    text=" ".join(str(v) for v in profile.values()).lower()
    keyword_map={
      "technology":["technology","coding","computer","programming","software","ai","robot"],
      "logical":["math","logic","numbers","analysis","analytical","problem solving"],
      "problem":["problem","challenge","puzzle","research"],
      "creativity":["art","design","creative","drawing","music","writing"],
      "communication":["communication","speaking","english","writing","debate"],
      "leadership":["leadership","leader","organize","team"],
      "social":["helping","community","social","people","service"],
      "science":["science","biology","chemistry","physics","medicine"],
      "empathy":["help","care","empathy","listening"],
      "math":["math","mathematics","numbers","accounting"],
      "business":["business","commerce","finance","entrepreneur","marketing"]
    }
    context={k:min(2,sum(1 for w in words if w in text)) for k,words in keyword_map.items()}
    results=[]
    for c in CAREERS:
        raw=0; maxraw=0
        for trait,w in c["weights"].items():
            val=float(answers.get(trait,3))
            raw += val*w
            maxraw += 5*w
            raw += context.get(trait,0)*w*0.35
        pct=max(50,min(99,round(raw/maxraw*100)))
        results.append((pct,c))
    results.sort(key=lambda x:x[0], reverse=True)
    return results[:5]

@app.route("/api/assess", methods=["POST"])
def assess():
    data=request.json or {}
    profile=session.get("student",{})
    top=score_careers(data,profile)
    rec=[]
    for pct,c in top:
        why=f"This career matches your assessment pattern, especially your strengths in {', '.join([k.replace('_',' ') for k,v in c['weights'].items() if float(data.get(k,3))>=4][:3]) or 'the assessed areas'}."
        rec.append({**c,"score":pct,"why":why})
    sid=session.get("student_id")
    if sid:
        con=db()
        con.execute("UPDATE students SET assessment=?, recommendations=? WHERE id=?",
                    (json.dumps(data),json.dumps(rec),sid))
        con.commit(); con.close()
    session["recommendations"]=rec
    return jsonify({"recommendations":rec})

@app.route("/api/results")
def results():
    return jsonify({"student":session.get("student",{}),"recommendations":session.get("recommendations",[])})

@app.route("/api/career/<path:name>")
def career(name):
    for c in CAREERS:
        if c["name"].lower()==name.lower(): return jsonify(c)
    return jsonify({"error":"Career not found"}),404

@app.route("/api/chat", methods=["POST"])
def chat():
    q=(request.json or {}).get("message","").lower()
    rec=session.get("recommendations",[])
    if "suitable" in q or "recommend" in q:
        ans="Based on your assessment, your leading options are: "+", ".join(x["name"] for x in rec[:3])+". Explore them using the Career Roadmap and Skill Gap sections."
    elif "data scientist" in q:
        ans="A Data Scientist commonly develops skills in Python, statistics, data analysis and machine learning. Mathematics and Computer Science are useful subjects."
    elif "cyber" in q:
        ans="Cybersecurity pathways benefit from Computer Science, networking, programming, logical thinking and security practice."
    elif "after class 12" in q or "after 12" in q:
        ans="After Class 12, compare degree pathways, entrance requirements, course content, costs, location and your own interests before deciding."
    elif "biology" in q and "technology" in q:
        ans="You can explore biotechnology, bioinformatics, health technology, medical technology and computational biology."
    else:
        ans="I can help you explore careers, subjects, skills, courses and roadmaps. Try asking about a specific career or your interests."
    return jsonify({"answer":ans})

@app.route("/api/action-plan")
def action_plan():
    return jsonify({"days":[
      {"day":"Week 1","title":"Explore","items":["Review your top 5 careers","Read one reliable career profile each day","List questions about your preferred career"]},
      {"day":"Week 2","title":"Build Skills","items":["Choose one core skill","Practise for 30–45 minutes a day","Complete a beginner activity or lesson"]},
      {"day":"Week 3","title":"Create","items":["Build a small project","Document what you learned","Ask a teacher/mentor for feedback"]},
      {"day":"Week 4","title":"Plan","items":["Compare courses and pathways","Identify subject requirements","Set three next-step goals"]}
    ]})

init_db()
if __name__=="__main__":
    app.run(debug=True)
