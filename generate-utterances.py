import itertools

intentName = "RamsayInsultIntent"

def gen(pattern, *opts):
    for optset in itertools.product(*opts):
        print(intentName + " " + pattern.format(*optset))

insult = ["insult", "make fun of", "mock"]
ramsay = ["ramsay", "gordon ramsay", "the hell's kitchen chef", "hell's kitchen chef"]
target = ["me", "this", "this {FoodName}", "my food", "my {FoodName}"]

gen("{} {}",
    insult,
    target
)

gen("{} {} {} {}",
    ["let's have", 'have', 'make'],
    ramsay,
    insult,
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

gen("{} a {} {}",
    ["give me", "let's have"],
    ramsay,
    ["insult", "burn"]
)

gen("{} {} like {}",
    insult,
    target,
    ramsay
)
