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

print("""
MicrowaveSuggestionIntent {Amount}
MicrowaveSuggestionIntent {Food}
MicrowaveSuggestionIntent {Amount} {Food}
MicrowaveSuggestionIntent {Amount} {AmountType} {Food}
MicrowaveSuggestionIntent {QuestionPhrasings} {Food}
MicrowaveSuggestionIntent {QuestionPhrasings} {Amount} {Food}
MicrowaveSuggestionIntent {QuestionPhrasings} {Amount} {AmountType} {Food}
MicrowaveSuggestionIntent {QuestionPhrasings} {Food} for
MicrowaveSuggestionIntent {QuestionPhrasings} {Amount} {Food} for
MicrowaveSuggestionIntent {QuestionPhrasings} {Amount} {AmountType} {Food} for
""")


print("""
GetIngredientSuggestion I need a substitution for {ListOfIngredients}
GetIngredientSuggestion Can you give me one for {ListOfIngredients}
GetIngredientSuggestion I need a replacement for {ListOfIngredients}
GetIngredientSuggestion I need an ingredient suggestion
GetIngredientSuggestion Can you give me an ingredient suggestion
GetIngredientSuggestion Can you give me a replacement ingredient
GetIngredientSuggestion Can you suggest an ingredient
GetIngredientSuggestion I need a replacement
GetIngredientSuggestion I need a suggestion
GetIngredientSuggestion I need a new ingredient
GetIngredientSuggestion what other ingredient can I use
GetIngredientSuggestion Please give me a replacement ingredient
GetIngredientSuggestion What's a good substitution for
GetIngredientSuggestion Can you give me a substitution for
GetIngredientSuggestion Is there a substitution for
GetIngredientSuggestion Is there another ingredient for
GetIngredientSuggestion Can you give me a substitution ingredient
GetIngredientSuggestion I need a substitution for {ListOfIngredients}
""")
