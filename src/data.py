#!/usr/bin/env python3
"""The single source of truth for the Module 1 practice lab exam.

Dr. Rennie's numbering and her slide order are kept exactly. What changes is
the wording of each prompt: every question is retagged into the short, uniform
style used on the practice exam tool, so a student reads the same shape of
sentence every time instead of a different phrasing on every slide.

Fields
  n     her question number
  s     slide file stem
  tag   the question as the student reads it
  a     the answer printed on the key
  alt   other wordings the key accepts
  core  what the grader insists on: a list of groups, all of which must be
        satisfied, each satisfied by any one stem matching at the start of a
        word. Word start matching is what keeps "dermis" out of "epidermis".
  no    stems that make an answer wrong even when core is satisfied, unless a
        stem in "yes" is also present. This separates keratinized from non
        keratinized stratified squamous.
"""

# The three slides carrying 33 to 38 arrived on 2 September and are in. Nothing
# is held back now, so the run is the full 52.
PENDING = []

TITLE = "Module 1 Practice Lab Exam"
COURSE = "BIO 004 Human Anatomy"
SCHOOL = "Solano Community College"
BYLINE = "Dr. Sharilyn Rennie"

QUESTIONS = [
 dict(n=1, s="s01", tag="Name this tissue",
      a="Cardiac muscle tissue",
      alt=["cardiac muscle", "heart muscle", "myocardium"],
      core=[["cardiac", "heart", "myocard"]]),

 dict(n=2, s="s01", tag="Name the structure at the tip of the arrow",
      a="Intercalated disc",
      alt=["intercalated disk"],
      core=[["intercalated"]]),

 dict(n=3, s="s02", tag="Name this tissue",
      a="Areolar connective tissue",
      alt=["loose connective tissue", "loose areolar connective tissue"],
      core=[["areolar", "loose"]]),

 dict(n=4, s="s02", tag="Name the structure at the tip of the arrow",
      a="Collagen fiber",
      alt=["collagen fibre", "collagenous fiber", "collagen"],
      core=[["collagen"]]),

 dict(n=5, s="s03", tag="Name this tissue",
      a="Stratified cuboidal epithelium",
      alt=["stratified cuboidal epithelial tissue"],
      core=[["stratified"], ["cuboidal"]]),

 dict(n=6, s="s03", tag="Name the structure between the two arrowheads. Be specific.",
      a="Lumen of the duct",
      alt=["duct lumen", "lumen"],
      core=[["lumen"]]),

 dict(n=7, s="s04", tag="Name this tissue",
      a="Smooth muscle tissue",
      alt=["smooth muscle", "visceral muscle", "non striated muscle"],
      core=[["smooth", "visceral"], ["muscle"]]),

 dict(n=8, s="s04", tag="Name one location where this tissue is found",
      a="The wall of a hollow organ: stomach, intestines, urinary bladder, "
        "uterus, blood vessels, or the airways",
      alt=["stomach", "intestine", "urinary bladder", "uterus", "blood vessel",
           "bronchus", "ureter", "esophagus"],
      core=[["stomach", "intestin", "bowel", "colon", "bladder", "uter",
             "blood vessel", "vessel", "arter", "vein", "venule", "arteriol",
             "airway", "bronch", "trachea", "gi", "digestive", "respiratory",
             "ureter", "urethra", "esophag", "oesophag", "gut", "viscera",
             "hollow", "iris"]]),

 dict(n=9, s="s05", tag="Name this tissue",
      a="Skeletal muscle tissue",
      alt=["skeletal muscle", "striated voluntary muscle"],
      core=[["skeletal", "voluntary"], ["muscle"]]),

 dict(n=10, s="s05", tag="Name one function of this tissue",
      a="Moves the skeleton under voluntary control. It also holds posture "
        "and produces heat.",
      alt=["voluntary movement", "moves bones", "body movement", "posture",
           "heat production"],
      core=[["move", "motion", "locomot", "contract", "posture", "heat",
             "thermo", "skelet", "bone", "voluntary", "stabil", "breath",
             "ventilat"]]),

 dict(n=11, s="s06", tag="Name this tissue",
      a="Compact bone",
      alt=["compact bone tissue", "osseous tissue", "dense bone"],
      core=[["compact", "osseous", "bone"]]),

 dict(n=12, s="s06", tag="Name one function of this tissue",
      a="Supports and protects the body. It also gives muscles levers to pull "
        "on, stores calcium and phosphate, and houses bone marrow.",
      alt=["support", "protection", "levers for movement", "calcium storage",
           "houses marrow"],
      core=[["support", "protect", "lever", "movement", "move", "calcium",
             "mineral", "phosph", "storage", "store", "marrow", "blood cell",
             "hematopo", "haematopo", "weight", "structur", "rigid", "frame"]]),

 dict(n=13, s="s07", tag="Name this tissue",
      a="Dense regular connective tissue",
      alt=["dense regular collagenous connective tissue"],
      core=[["dense"], ["regular"]]),

 dict(n=14, s="s07", tag="Name one function of this tissue",
      a="Attaches muscle to bone and bone to bone, and resists tension along "
        "one line of pull.",
      alt=["attaches muscle to bone", "attaches bone to bone",
           "resists tension in one direction"],
      core=[["attach", "connect", "anchor", "join", "bind", "tension", "pull",
             "force", "tendon", "ligament", "resist", "strength", "strong",
             "stabil", "withstand"]]),

 dict(n=15, s="s08", tag="Name this tissue",
      a="Pseudostratified ciliated columnar epithelium",
      alt=["pseudostratified columnar epithelium", "respiratory epithelium"],
      core=[["pseudostratified", "pseudo", "respiratory"]]),

 dict(n=16, s="s08", tag="Name the function of the structure at the tips of the arrows",
      a="The cilia sweep mucus and the debris caught in it along the surface, "
        "away from the lungs.",
      alt=["move mucus", "propel mucus", "mucociliary escalator",
           "sweep debris out of the airway"],
      core=[["move", "moves", "sweep", "propel", "push", "transport", "waft",
             "beat", "clear", "escalat", "mucus", "mucous", "muco", "debris",
             "particle", "trap"]]),

 dict(n=17, s="s09", tag="Name this tissue",
      a="Stratified squamous epithelium, non keratinized",
      alt=["non keratinized stratified squamous epithelium",
           "moist stratified squamous epithelium"],
      core=[["stratified"], ["squamous"]],
      no=["keratin"], yes=["non keratin", "nonkeratin", "not keratin"]),

 dict(n=18, s="s09", tag="Name one location where this tissue is found",
      a="Esophagus, oral cavity, pharynx, vagina, or the anal canal",
      alt=["esophagus", "mouth", "oral cavity", "pharynx", "vagina",
           "anal canal"],
      core=[["esophag", "oesophag", "oral", "mouth", "buccal", "cheek",
             "tongue", "pharyn", "vagina", "anal", "anus", "larynx",
             "epiglott", "lip"]]),

 dict(n=19, s="s10", tag="Name the body cavity outlined in orange",
      a="Mediastinum",
      alt=["mediastinal cavity", "the mediastinum"],
      core=[["mediastin"]]),

 dict(n=20, s="s10", tag="Name the superior border of this cavity",
      a="The superior thoracic aperture, also called the thoracic inlet, at "
        "the level of the first rib and T1",
      alt=["superior thoracic aperture", "thoracic inlet", "first rib",
           "level of T1", "root of the neck"],
      core=[["superior thoracic", "thoracic inlet", "thoracic aperture",
             "aperture", "inlet", "first rib", "1st rib", "rib 1", "t1",
             "root of the neck", "neck", "clavicle", "manubri"]]),

 # Slide 11 was a muscle section neither of us was sure of. Replaced at her
 # direction with the adipose panel from her own Tissues II bank, so students
 # meet a picture they have already seen in Loops.
 dict(n=21, s="s11", tag="Name this tissue",
      a="Adipose tissue",
      alt=["adipose", "fat", "fat tissue", "adipose connective tissue"],
      core=[["adipose", "fat"]]),

 dict(n=22, s="s11", tag="Name one location where this tissue is found",
      a="The hypodermis, the subcutaneous layer. Also around the kidneys, behind "
        "the eyeball, in the breast and in the omentum.",
      alt=["hypodermis", "subcutaneous layer", "around the kidneys",
           "behind the eyeball", "breast", "omentum", "bone marrow"],
      core=[["hypodermis", "hypoderm", "subcutaneous", "subcutis", "kidney",
             "renal", "eye", "orbit", "breast", "omentum", "mesenter",
             "marrow", "abdomen", "abdominal", "buttock", "hip", "thigh",
             "around organs", "vital organ", "organ", "under the skin",
             "beneath the skin", "yellow marrow", "visceral"]]),

 dict(n=23, s="s12", tag="Name this entire layer at the bracket",
      a="Dermis",
      alt=["the dermis", "dermal layer"],
      core=[["dermis", "dermal"]]),

 dict(n=24, s="s12", tag="Name the structure at the tip of the arrow",
      a="Apocrine sweat gland",
      alt=["apocrine gland"],
      core=[["apocrine"]]),

 dict(n=25, s="s13", tag="Name this tissue",
      a="Transitional epithelium",
      alt=["urothelium", "transitional epithelial tissue"],
      core=[["transitional", "urotheli"]]),

 dict(n=26, s="s13", tag="Name one function of this tissue",
      a="Stretches so the organ can fill and empty, and keeps urine from "
        "leaking into the wall.",
      alt=["stretches", "allows distension", "protects the wall from urine",
           "allows the bladder to fill"],
      core=[["stretch", "distend", "distens", "expand", "accommodat", "fill",
             "empt", "volume", "recoil", "protect", "barrier", "imperme",
             "urine", "leak", "water"]]),

 dict(n=27, s="s14",
      tag="Give the LETTER of the abdominal quadrant that contains the spleen",
      a="C",
      alt=["letter C", "quadrant C"],
      core=[["c"]]),

 dict(n=28, s="s14",
      tag="Give the NAME of the abdominal quadrant that contains the cecum",
      a="Right lower quadrant (RLQ)",
      alt=["RLQ", "right lower quadrant"],
      core=[["right lower", "rlq"]]),

 dict(n=29, s="s15", tag="Name this tissue",
      a="Reticular connective tissue",
      alt=["reticular tissue", "reticular connective"],
      core=[["reticular"]]),

 dict(n=30, s="s15", tag="Name one location where this tissue is found",
      a="Spleen, lymph nodes, tonsils, or bone marrow",
      alt=["spleen", "lymph node", "tonsil", "bone marrow", "thymus"],
      core=[["spleen", "lymph", "tonsil", "marrow", "thymus", "liver",
             "lymphoid", "peyer"]]),

 dict(n=31, s="s16", tag="Name this tissue",
      a="Simple squamous epithelium",
      alt=["simple squamous epithelial tissue"],
      core=[["simple"], ["squamous"]]),

 dict(n=32, s="s16", tag="Name the function this tissue is carrying out here",
      a="Rapid diffusion. The barrier is one cell thin, so oxygen and carbon "
        "dioxide cross it quickly.",
      alt=["gas exchange", "diffusion",
           "rapid exchange across a thin barrier"],
      core=[["diffus", "exchange", "gas", "o2", "oxygen", "carbon dioxide",
             "co2", "respirat", "thin", "rapid", "filtrat", "transport",
             "permeab", "absorb"]]),

 dict(n=33, s="s17", tag="Name the structure outlined in orange",
      a="Dermal papilla",
      alt=["dermal papillae", "papilla of the dermis"],
      core=[["dermal papilla", "papilla"]]),

 dict(n=34, s="s17", tag="Name the structure at the tip of the arrow",
      a="Tactile corpuscle, also called a Meissner corpuscle",
      alt=["Meissner corpuscle", "Meissner's corpuscle", "tactile corpuscle"],
      core=[["tactile", "meissner", "meisner"]]),

 dict(n=35, s="s18", tag="Name the body region at letter B",
      a="Sural region, the calf",
      alt=["sural", "calf", "posterior leg"],
      core=[["sural", "calf"]]),

 dict(n=36, s="s18",
      tag="Which body plane would separate A and B into superior and inferior "
          "compartments?",
      a="Transverse plane",
      alt=["horizontal plane", "cross sectional plane", "axial plane"],
      core=[["transverse", "horizontal", "cross section", "axial"]]),

 dict(n=37, s="s19", tag="Name this tissue",
      a="Elastic cartilage",
      alt=["elastic cartilage tissue"],
      core=[["elastic"], ["cartilage", "chondr"]]),

 dict(n=38, s="s19", tag="Name one location where this tissue is found",
      a="The external ear, the epiglottis, or the auditory tube",
      alt=["external ear", "auricle", "pinna", "epiglottis", "auditory tube",
           "eustachian tube"],
      core=[["ear", "auricle", "pinna", "epiglott", "auditory tube",
             "eustachian", "larynx"]]),

 dict(n=39, s="s20", tag="Name this tissue",
      a="Elastic connective tissue",
      alt=["elastic tissue", "elastic connective"],
      core=[["elastic", "elastin"]]),

 dict(n=40, s="s20", tag="Name one function of this tissue",
      a="Stretches and springs back, so the structure recoils to its resting "
        "shape after every pulse or breath.",
      alt=["stretch and recoil", "allows recoil", "allows stretching",
           "springs back"],
      core=[["stretch", "recoil", "spring", "rebound", "elastic", "expand",
             "distend", "flexib", "return", "resil", "pressure", "pulse",
             "flow"]]),

 dict(n=41, s="s21", tag="Name this tissue",
      a="Keratinized stratified squamous epithelium",
      alt=["stratified squamous epithelium, keratinized", "epidermis"],
      core=[["stratified", "epiderm"], ["squamous", "epiderm"]],
      no=["non keratin", "nonkeratin"], yes=[]),

 dict(n=42, s="s21", tag="Name the structure at the arrow and inside the bracket",
      a="Dermal papilla",
      alt=["dermal papillae", "papilla of the dermis"],
      core=[["dermal papilla", "papilla"]]),

 dict(n=43, s="s22", tag="Name the structure at the tip of the arrow",
      a="Eccrine sweat gland",
      alt=["merocrine sweat gland", "eccrine gland", "sweat gland"],
      core=[["eccrine", "merocrine", "sweat", "sudorif"]]),

 dict(n=44, s="s22", tag="Name this region at the bracket",
      a="Hypodermis",
      alt=["subcutaneous layer", "subcutaneous tissue", "superficial fascia",
           "subcutis"],
      core=[["hypodermis", "hypoderm", "subcutaneous", "subcutis",
             "superficial fascia"]]),

 dict(n=45, s="s23", tag="Name this tissue",
      a="Simple cuboidal epithelium",
      alt=["simple cuboidal epithelial tissue"],
      core=[["simple"], ["cuboidal"]]),

 dict(n=46, s="s23",
      tag="Name one location where this tissue is found. Be specific.",
      a="The duct of a salivary gland. It is also in kidney tubules, thyroid "
        "follicles and pancreatic ducts.",
      alt=["salivary gland duct", "kidney tubule", "renal tubule",
           "thyroid follicle", "pancreatic duct", "gland duct"],
      core=[["salivary", "duct", "kidney", "renal", "tubule", "thyroid",
             "follicle", "pancrea", "ovary", "ovarian", "bronchiol", "gland",
             "liver", "choroid"]]),

 dict(n=47, s="s24", tag="Name this protein",
      a="Keratin",
      alt=["keratin protein"],
      core=[["keratin"]]),

 dict(n=48, s="s24", tag="Name this specific layer",
      a="Stratum granulosum",
      alt=["granular layer", "stratum granulosum of the epidermis"],
      core=[["granulosum", "granular"]]),

 dict(n=49, s="s25", tag="Name the body region at letter B",
      a="Brachial region, the arm",
      alt=["brachial", "brachium", "arm"],
      core=[["brachi", "arm"]],
      no=["forearm", "antebrachi"], yes=[]),

 dict(n=50, s="s25",
      tag="Fill in the blank. Body region A is ______ (directional term) to "
          "body region B.",
      a="Proximal",
      alt=["superior", "proximal to B"],
      core=[["proximal", "superior", "cephal", "cranial"]]),

 dict(n=51, s="s26", tag="Name the structure at the tip of the arrow",
      a="Goblet cell",
      alt=["goblet cells", "mucous cell"],
      core=[["goblet"]]),

 dict(n=52, s="s26", tag="Name the function of this structure",
      a="Secretes mucus, which traps debris and keeps the surface moist.",
      alt=["secretes mucus", "produces mucus", "makes mucin",
           "lubricates and protects the surface"],
      core=[["secret", "produc", "make", "makes", "release", "mucus",
             "mucous", "mucin", "lubric", "moist", "trap", "protect",
             "barrier"]]),
]


# ---------------------------------------------------------------------------
# Answers I am not sure enough about to let stand without her eyes on them.
# Keyed by question number, the value is why it is flagged, written for her to
# read. build_review.py turns these into the check sheet. Keeping the reasons
# here rather than in the sheet means the sheet cannot go stale.
# ---------------------------------------------------------------------------
# She went through all seventeen on 2 September and confirmed sixteen as keyed.
# The one correction: question 4 is a COLLAGEN fibre, not an elastic one, and
# the EF and CF labels printed on that slide are now covered so the picture
# does not answer its own question. Nothing is outstanding, so the sheet has
# nothing left to flag. Add a question number here if a new doubt comes up.
FLAGS = {
}

for _q in QUESTIONS:
    if _q["n"] in FLAGS:
        _q["flag"] = FLAGS[_q["n"]]


def slides():
    """Slide stem -> the questions on it, in her order."""
    out = []
    for q in QUESTIONS:
        if out and out[-1][0] == q["s"]:
            out[-1][1].append(q)
        else:
            out.append((q["s"], [q]))
    return out
