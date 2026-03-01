from flask import Flask, request, jsonify
import os
import json

app = Flask(__name__)

DB_FILE = "answer.json"

def get_answer():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f).get("answer")
    return None

def save_answer(answer):
    with open(DB_FILE, "w") as f:
        json.dump({"answer": answer}, f)

@app.route("/")
def home():
    saved = get_answer()
    saved_script = f"showResult('{saved}');" if saved else ""

    html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Eid Mubarak ❤️</title>
<style>
body{{margin:0;background:black;color:white;font-family:Segoe UI;text-align:center;overflow:hidden}}

#eid{{position:absolute;top:40%;width:100%;font-size:4rem;
background:linear-gradient(90deg,#ffd700,#ff6ec7);
-webkit-background-clip:text;color:transparent;transition:2s;}}

#message{{position:absolute;top:55%;width:100%;opacity:0;transition:2s;font-size:1.5rem;}}

#openBtn{{position:absolute;top:70%;left:50%;transform:translateX(-50%);
padding:15px 40px;border:none;border-radius:30px;
background:linear-gradient(90deg,#ff6ec7,#ffd700);cursor:pointer;opacity:0;}}

#proposal{{position:fixed;width:100%;height:100%;background:black;
display:none;flex-direction:column;justify-content:center;align-items:center;}}

.choice{{padding:15px 30px;margin:10px;font-size:1.2rem;
border:none;border-radius:30px;cursor:pointer;}}

.yes{{background:#00ff99;color:black}}
.no{{background:#ff4d6d;color:white}}

#response{{margin-top:30px;font-size:1.5rem}}
</style>
</head>

<body>

<div id="eid">EID MUBARAK</div>
<div id="message"></div>
<button id="openBtn">Open My Heart 💌</button>
<div id="proposal"></div>

<script>

const YOUR_MESSAGE = `
On this blessed Eid,
I pray that one day
we celebrate every Eid together.
`;

const PROPOSAL_TEXT = "Will You Marry Me? 💍";
const YES_MESSAGE = "You made me the happiest man alive ❤️✨";
const NO_MESSAGE = "I respect your decision... but my heart feels heavy 💔";

setTimeout(()=>{{
document.getElementById("eid").style.top="20%";
document.getElementById("message").innerHTML=YOUR_MESSAGE;
document.getElementById("message").style.opacity=1;
}},5000);

setTimeout(()=>{{
document.getElementById("openBtn").style.opacity=1;
}},10000);

document.getElementById("openBtn").onclick=()=>{{
document.getElementById("eid").style.display="none";
document.getElementById("message").style.display="none";
document.getElementById("openBtn").style.display="none";

let p=document.getElementById("proposal");
p.style.display="flex";

if("{saved}"!="None"){{
showResult("{saved}");
}}else{{
p.innerHTML=`
<h2>${{PROPOSAL_TEXT}}</h2>
<button class="choice yes" onclick="sendAnswer('YES')">YES ❤️</button>
<button class="choice no" onclick="sendAnswer('NO')">NO 💔</button>
<div id="response"></div>
`;
}}
}};

function sendAnswer(ans){{
fetch("/submit",{{
method:"POST",
headers:{{"Content-Type":"application/json"}},
body:JSON.stringify({{answer:ans}})
}})
.then(res=>res.json())
.then(data=>{{
if(data.status==="saved"){{showResult(ans);}}
}});
}}

function showResult(ans){{
let p=document.getElementById("proposal");
p.innerHTML=`<h2>${{PROPOSAL_TEXT}}</h2><div id="response"></div>`;
let r=document.getElementById("response");

if(ans==="YES"){{r.innerHTML=YES_MESSAGE;celebrate();}}
else{{r.innerHTML=NO_MESSAGE;}}
}}

function celebrate(){{
for(let i=0;i<50;i++){{ 
let f=document.createElement("div");
f.innerHTML="🎉";
f.style.position="absolute";
f.style.left=Math.random()*100+"vw";
f.style.top=Math.random()*100+"vh";
f.style.fontSize="30px";
document.body.appendChild(f);
setTimeout(()=>f.remove(),1000);
}}
}}

</script>

</body>
</html>
""".format(saved=saved)

    return html


@app.route("/submit", methods=["POST"])
def submit():
    if get_answer():
        return jsonify({"status": "locked"})
    data = request.get_json()
    answer = data.get("answer")
    save_answer(answer)
    return jsonify({"status": "saved"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)