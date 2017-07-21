import itertools

intentName = "RamsayInsultIntent"

def gen(pattern, *opts):
    for optset in itertools.product(*opts):
        print(intentName + " " + pattern.format(*optset))

ramsay = ["ramsay", "gordon ramsay", "the hell's kitchen chef"]
target = ["me", "this", "my food"]

gen("{} {} {} {}",
    ["let's have", 'have', 'make'],
    ramsay,
    ["insult", "make fun of", "mock"],
    target
)

gen("{} {} {} {}",
    ["what does", "what's", "what do you think"],
    ramsay,
    ["think of", "think about", "make of"],
    target
)

gen("get an insult from {} about {}",
    ramsay,
    target
)
