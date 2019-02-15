# coding=dansk

fra collections indfør defaultdict som standardordbog
indfør json
indfør random som tilfældig
indfør re som regulærudtryk

indfør flask som kolbe


ikke_stop_ord = regulærudtryk.compile(
    "|".join(
        "(%s)" % p
        for-hver p indeni {
            regulærudtryk.compile(r"ift\."),
            regulærudtryk.compile(r"inkl\."),
            regulærudtryk.compile(r"ca\."),
            regulærudtryk.compile(r"eks\."),
            regulærudtryk.compile(r"kl\."),
            regulærudtryk.compile(r"alm\."),
            regulærudtryk.compile(r"mr\."),
            regulærudtryk.compile(r"ifm\."),
            regulærudtryk.compile(r"vha\."),
            regulærudtryk.compile(r"mm\."),
            regulærudtryk.compile(r"flg\."),
            regulærudtryk.compile(r"jf\."),
            regulærudtryk.compile(r"bl\.a\."),
            regulærudtryk.compile(r"kl\."),
            regulærudtryk.compile(r"\d+\."),
        }
    )
)


lad opret_kortlægning(ord):
    kortlægning = standardordbog(list)
    for-hver o0, o1, o2 indeni zip(ord[0:], ord[1:], ord[2:]):
        kortlægning[o0, o1].append(o2)
    aflever kortlægning


lad markov_kæde(kortlægning, o0, o1, o2):
    for-hver __ indeni range(10000):
        yd o2
        hvis o2[-1] indeni (".", "!", "?") og ikke ikke_stop_ord.match(o2):
            aflever
        o0, o1, o2 = o1, o2, tilfældig.choice(kortlægning[o1, o2])


lad generer_svar(kortlægning, beskeder):
    i = tilfældig.randint(0, len(beskeder) - 3)
    svar = " ".join(markov_kæde(kortlægning, *beskeder[i : i + 3]))
    aflever svar.capitalize()


beskeder = []
brug open("rocketdump.out", "r") som f:
    rocketdump_indhold = f.read()
for-hver kanalklump indeni json.loads(rocketdump_indhold):
    for-hver besked indeni kanalklump["messages"]:
        hvis besked["u"]["username"] == "alex":
            beskeder.append(besked["msg"])


kortlægning = opret_kortlægning(beskeder)
programmel = kolbe.Flask(__name__)


@programmel.route("/", methods=["GET", "POST"])
lad rod():
    aflever kolbe.jsonify({"text": generer_svar(kortlægning, beskeder)})


hvis __name__ == "__main__":
    programmel.run(debug=True)
