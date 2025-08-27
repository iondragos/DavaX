import re

OFFENSIVE_KEYWORDS = [
    # English profanity - general
    "fuck", "fucks", "fucking", "motherfucker", "motherfuckers",
    "shit", "shits", "shitty", "bullshit", "horseshit",
    "bitch", "bitches", "bitchy",
    "ass", "asses", "asshole", "assholes", "dumbass", "jackass", "smartass",
    "bastard", "bastards",
    "damn", "dammit", "goddamn", "goddammit",
    "cunt", "cunts",
    "piss", "pissed", "pissing", "piss off",
    "crap", "crappy", "screw you", "screwed",
    "wtf", "omfg", "stfu", "gtfo",

    # Sexually explicit / derogatory
    "slut", "sluts", "whore", "whores", "hoe", "hoes",
    "dick", "dicks", "dickhead", "dickheads",
    "cock", "cocks", "cockhead", "cockbite",
    "pussy", "pussies",
    "tit", "tits", "boobs", "boob", "nipple", "nipples",
    "penis", "vagina", "clit", "clitoris",
    "fap", "jerk off", "jerking", "masturbate", "masturbation",
    "sex", "sexy", "horny", "porn", "porno", "pornography", "pornhub",

    # Homophobia & transphobia
    "fag", "faggot", "fags", "dyke", "tranny", "shemale", "queer"  # note: some terms are reclaimed by communities, but still widely flagged
    "homo", "homos", "lesbo", "lesbos",

    # Ableist or dehumanizing terms
    "retard", "retarded", "idiot", "moron", "dumbass", "lame", "stupid", "crazy",
    "schizo", "psycho", "dumb", "fatass", "ugly",

    # Racist / xenophobic slurs
    "nigger", "nigga", "niggaz",
    "chink", "gook", "wetback", "beaner", "spic", "coon", "porchmonkey",
    "sandnigger", "towelhead", "camel jockey", "paki", "gypsy", "jewboy",
    "cracker", "redskin", "zipperhead", "ape", "monkey"  # ← often racialized slurs

    # Misc hate / insult terms
    "kill yourself", "kys", "go die", "i hope you die", "burn in hell",
    "i’ll rape you", "rape", "rapist", "molest", "molester", "abuse", "abuser",
    "terrorist", "nazi", "hitler", "heil hitler", "gas you", "death to",
    "school shooter", "incel", "simp", "cuck", "beta male", "snowflake", "libtard", "feminazi"
]


def contains_offensive_language(text: str) -> bool:
    lowered = text.lower()
    for word in OFFENSIVE_KEYWORDS:
        if re.search(rf"\b{re.escape(word)}\b", lowered):
            return True
    return False
