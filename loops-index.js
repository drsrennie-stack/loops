/* ============================================================
   BIO 004 Human Anatomy, Fall 2026
   loops-index.js

   The 39 Loops, each tagged with the competencies it gives
   evidence for.

   WHY THIS EXISTS
   ---------------
   Loops lived only as a link out to Kajabi. loops.html in the
   course repo is a 2-byte empty file. Nothing recorded that a
   student had watched one, so Loops could not be filtered by
   weakness and could not count toward anything.

   Source of truth: the LOOPS array in drsrennie-stack/loops
   index.html. Ids, titles and units are read from there, not
   invented.

   WHAT THIS UNLOCKS
   -----------------
   Ten competencies had NO card coverage at all: the upper
   extremity lab muscles, nerves and vessels, the lower limb
   vessels and nerves, and the head and neck lab muscles. Those
   are cadaver and specimen work, which multiple choice cannot
   assess well. Every one of them is covered by a Loop.

   With cards and Loops together, all 196 competencies have at
   least one evidence source. Neither alone gets there.
   ============================================================ */

/* Frames live at images/<dir>/sNN.jpg in the loops repo. */
window.BIO004_LOOPS_BASE = "https://drsrennie-stack.github.io/loops/";
window.BIO004_LOOPS_IMG = function (l, n) {
  return window.BIO004_LOOPS_BASE + "images/" + l.dir + "/s" + (n < 10 ? "0" + n : n) + ".jpg";
};

window.BIO004_LOOPS = [
  { id:"intro", title:"Introduction Loop", unit:"Intro to Anatomy", dir:"intro", frames:89,
    comps:["w1-levels-organization","w1-anatomical-position","w1-planes-sections","w1-directional-terms","w1-regional-terms","w1-body-cavities","w1-serous-membranes","w1-mediastinum","w1-peritoneum-relationships","w1-abdominopelvic-map"] },
  { id:"tissues", title:"Tissues Loop", unit:"Tissues & Histology", dir:"tissues", frames:63,
    comps:["w1-germ-layers","w1-epithelial-id","w1-cell-junctions","w1-connective-id","w1-muscle-tissue-id","w1-nervous-tissue-id","w1-body-membranes","w1-generalized-cell","w1-plasma-membrane","w1-nucleus","w1-organelles"] },
  { id:"skin", title:"Integumentary Loop", unit:"Skin", dir:"skin", frames:25,
    comps:["w1-skin-layers","w1-epidermal-strata","w1-dermis-layers","w1-skin-accessory"] },
  { id:"bone", title:"Bone Tissue Loop", unit:"Bone Tissue", dir:"bone", frames:65,
    comps:["w2-cartilage-types","w2-cartilage-growth","w2-bone-shapes","w2-long-bone-gross","w2-compact-spongy","w2-bone-cells","w2-ossification-growth"] },
  { id:"skull", title:"Axial Skull Loop", unit:"Axial Skull", dir:"skull", frames:63,
    comps:["w2-skull-bones","w2-skull-markings","w2-sutures-fontanelles","w2-skull-cavities","w2-skull-foramina"] },
  { id:"appendicular", title:"Appendicular Loop", unit:"Appendicular Skeleton", dir:"appendicular", frames:83,
    comps:["w2-bone-markings-vocab","w2-pectoral-girdle","w2-arm-forearm","w2-hand-bones","w2-pelvic-girdle","w2-thigh-knee","w2-leg-bones","w2-foot-bones"] },
  { id:"boneaxial2", title:"Bone & Axial Loop II", unit:"Bone & Axial II", dir:"boneaxial2", frames:85,
    comps:["w2-spine-regions","w2-typical-vertebra","w2-regional-vertebrae","w2-thoracic-cage","w2-joint-classification","w2-fibrous-cartilaginous","w2-synovial-structure","w2-joint-movements","w2-synovial-types","w2-shoulder-knee"] },
  { id:"muscles-upper", title:"Muscles — Upper", unit:"Upper Extremity, Chest & Back", dir:"muscles-upper", frames:144,
    comps:["w4-lab-chest-anterior-arm","w4-lab-forearm-compartments","w4-lab-posterior-shoulder-cuff","w5-lab-abdominal-wall","w5-lab-thigh-gluteal","w5-lab-leg-muscles"] },
  { id:"muscles-lower", title:"Muscles — Trunk & Lower", unit:"Muscles: Abdomen, Pelvis & Leg", dir:"muscles-lower", frames:37,
    comps:["w5-lab-abdominal-wall","w5-lab-thigh-gluteal","w5-lab-leg-muscles"] },
  { id:"muscles-head", title:"Muscles — Head & Neck", unit:"Muscles: Head, Neck & Eye", dir:"muscles-head", frames:13,
    comps:["w7-lab-facial-expression","w7-lab-mastication","w7-lab-neck","w7-lab-extraocular"] },
  { id:"sarcomere", title:"Sarcomere Loop", unit:"Sarcomere", dir:"sarcomere", frames:13,
    comps:["w4-ct-coverings","w4-muscle-organization","w4-muscle-fiber-parts","w4-sarcomere","w4-myofilament-proteins","w4-muscle-tissue-types"] },
  { id:"microanatomy", title:"Muscle Microanatomy Loop", unit:"Muscle Microanatomy", dir:"microanatomy", frames:27,
    comps:["w4-ct-coverings","w4-muscle-organization","w4-muscle-fiber-parts","w4-sarcomere","w4-myofilament-proteins","w4-muscle-tissue-types"] },
  { id:"muscletissue", title:"Muscle Tissue Loop", unit:"Muscle Tissue", dir:"muscletissue", frames:15,
    comps:["w4-ct-coverings","w4-muscle-organization","w4-muscle-fiber-parts","w4-sarcomere","w4-myofilament-proteins","w4-muscle-tissue-types","w1-germ-layers","w1-epithelial-id","w1-cell-junctions","w1-connective-id","w1-muscle-tissue-id","w1-nervous-tissue-id","w1-body-membranes"] },
  { id:"abdominal-muscles", title:"Abdominal Muscles Loop", unit:"Abdominal Muscles", dir:"abdominal-muscles", frames:21,
    comps:["w5-lab-abdominal-wall","w5-lab-thigh-gluteal","w5-lab-leg-muscles"] },
  { id:"abdominal-fascia", title:"Abdominal Fascia Loop", unit:"Abdominal Wall & Fascia", dir:"abdominal-fascia", frames:11,
    comps:["w5-lab-abdominal-wall","w5-lab-thigh-gluteal","w5-lab-leg-muscles"] },
  { id:"esophagus", title:"Esophagus Loop", unit:"Esophagus", dir:"esophagus", frames:9,
    comps:["w5-canal-wall","w5-enteric-plexuses","w5-peritoneum-folds","w5-retroperitoneal","w5-mouth-pharynx-esophagus","w5-canal-sphincters","w5-stomach","w5-small-intestine","w5-large-intestine","w5-food-pathway","w5-canal-disorders"] },
  { id:"parotid", title:"Parotid Gland Loop", unit:"Parotid Gland & Duct", dir:"parotid", frames:9,
    comps:["w5-teeth-tongue","w5-salivary-glands","w5-liver-gross-lobule","w5-bile-path","w5-pancreas","w5-accessory-disorders"] },
  { id:"stomach", title:"Stomach Loop", unit:"Stomach", dir:"stomach", frames:27,
    comps:["w5-canal-wall","w5-enteric-plexuses","w5-peritoneum-folds","w5-retroperitoneal","w5-mouth-pharynx-esophagus","w5-canal-sphincters","w5-stomach","w5-small-intestine","w5-large-intestine","w5-food-pathway","w5-canal-disorders"] },
  { id:"pharynx", title:"Pharynx Loop", unit:"Pharynx & Oral Cavity", dir:"pharynx", frames:27,
    comps:["w5-canal-wall","w5-enteric-plexuses","w5-peritoneum-folds","w5-retroperitoneal","w5-mouth-pharynx-esophagus","w5-canal-sphincters","w5-stomach","w5-small-intestine","w5-large-intestine","w5-food-pathway","w5-canal-disorders"] },
  { id:"cadaver-ue", title:"Cadaver UE Loop", unit:"Cadaver: Back, Thorax & Upper Arm", dir:"cadaver-ue", frames:77,
    comps:["w4-lab-chest-anterior-arm","w4-lab-forearm-compartments","w4-lab-posterior-shoulder-cuff","w4-lab-ue-arteries-veins","w4-lab-ue-nerves"] },
  { id:"forearm-cadaver", title:"Forearm Cadaver Loop", unit:"Cadaver: Forearm & Arm", dir:"forearm-cadaver", frames:63,
    comps:["w4-lab-chest-anterior-arm","w4-lab-forearm-compartments","w4-lab-posterior-shoulder-cuff","w4-lab-ue-nerves"] },
  { id:"upper-leg-cadaver", title:"Upper Leg Cadaver Loop", unit:"Upper Leg (Cadaver)", dir:"upper-leg-cadaver", frames:69,
    comps:["w5-lab-abdominal-wall","w5-lab-thigh-gluteal","w5-lab-leg-muscles","w5-lab-abdominal-vessels","w5-lab-lower-limb-vessels-nerves"] },
  { id:"lower-leg-cadaver", title:"Lower Leg Cadaver Loop", unit:"Lower Leg (Cadaver)", dir:"lower-leg-cadaver", frames:39,
    comps:["w5-lab-abdominal-wall","w5-lab-thigh-gluteal","w5-lab-leg-muscles","w5-lab-abdominal-vessels","w5-lab-lower-limb-vessels-nerves"] },
  { id:"colon", title:"Colon Loop", unit:"Colon & Intestines", dir:"colon", frames:29,
    comps:["w5-canal-wall","w5-enteric-plexuses","w5-peritoneum-folds","w5-retroperitoneal","w5-mouth-pharynx-esophagus","w5-canal-sphincters","w5-stomach","w5-small-intestine","w5-large-intestine","w5-food-pathway","w5-canal-disorders"] },
  { id:"pancreas", title:"Pancreas Loop", unit:"Pancreas & Ducts", dir:"pancreas", frames:43,
    comps:["w5-teeth-tongue","w5-salivary-glands","w5-liver-gross-lobule","w5-bile-path","w5-pancreas","w5-accessory-disorders"] },
  { id:"liver", title:"Liver Loop", unit:"Liver: Models & Cadaver", dir:"liver", frames:73,
    comps:["w5-teeth-tongue","w5-salivary-glands","w5-liver-gross-lobule","w5-bile-path","w5-pancreas","w5-accessory-disorders"] },
  { id:"urinary", title:"Urinary System Loop", unit:"Urinary System", dir:"urinary", frames:43,
    comps:["w6-kidney-gross","w6-kidney-internal","w6-nephron-parts","w6-nephron-types","w6-jga-filtration","w6-kidney-bloodsupply","w6-urine-path","w6-urinary-disorders"] },
  { id:"renal-micro", title:"Renal Model Loop", unit:"Renal (Model & Microanatomy)", dir:"renal-micro", frames:69,
    comps:["w6-kidney-gross","w6-kidney-internal","w6-nephron-parts","w6-nephron-types","w6-jga-filtration","w6-kidney-bloodsupply","w6-urine-path","w6-urinary-disorders"] },
  { id:"reproductive-female", title:"Female Reproductive Loop", unit:"Female Reproductive", dir:"reproductive-female", frames:21,
    comps:["w6-ovary","w6-ovum-path","w6-uterus","w6-vagina-vulva","w6-mammary"] },
  { id:"reproductive-male", title:"Male Reproductive Loop", unit:"Male Reproductive", dir:"reproductive-male", frames:17,
    comps:["w6-scrotum-testes","w6-sperm-path","w6-sperm-cell","w6-male-glands-penis","w6-male-disorders"] },
  { id:"reproductive-cadaver", title:"Reproductive Cadaver Loop", unit:"Reproductive (Cadaver)", dir:"reproductive-cadaver", frames:49,
    comps:["w6-scrotum-testes","w6-sperm-path","w6-sperm-cell","w6-male-glands-penis","w6-male-disorders","w6-ovary","w6-ovum-path","w6-uterus","w6-vagina-vulva","w6-mammary"] },
  { id:"respiratory", title:"Respiratory Loop", unit:"Respiratory System", dir:"respiratory", frames:145,
    comps:["resp-zones","resp-upper-tract","resp-larynx","resp-tree","resp-lungs-pleura","resp-histo","resp-thoracic-diaphragm","resp-disorders"] },
  { id:"heart", title:"Heart Loop", unit:"The Heart", dir:"heart", frames:157,
    comps:["cv-surfaces","cv-chambers","cv-valves","cv-valve-support","cv-cardiac-muscle","cv-blood-pathway","bvn-great-vessels","cv-coronary","cv-conduction-anat","cv-cardiac-nerves","bvn-vessel-tunics","bvn-vessel-types","bvn-artery-cap-vein-kinds","bvn-circulatory-routes","bvn-vessel-disorders","bvn-fetal-remnants"] },
  { id:"neuro-brain", title:"Brain: Lateral & Superior", unit:"Brain (Lateral & Superior)", dir:"neuro-brain", frames:47,
    comps:["w7-brain-organization","w7-brain-development","w7-cerebrum-surface","w7-cortex-functional-areas","w7-white-matter-tracts","w7-basal-ganglia","w7-diencephalon","w7-cerebellum","w7-limbic-system","w7-circle-of-willis"] },
  { id:"neuro-brain-midsagittal", title:"Brain: Midsagittal", unit:"Brain (Midsagittal)", dir:"neuro-brain-midsagittal", frames:61,
    comps:["w7-brain-organization","w7-brain-development","w7-cerebrum-surface","w7-cortex-functional-areas","w7-white-matter-tracts","w7-basal-ganglia","w7-diencephalon","w7-cerebellum","w7-limbic-system","w7-circle-of-willis","w7-cranial-meninges","w7-spinal-meninges-spaces","w7-cord-termination-lp","w7-ventricles","w7-csf-circulation","w7-bbb"] },
  { id:"neuro-brain-cow", title:"Circle of Willis", unit:"Circle of Willis", dir:"neuro-brain-cow", frames:28,
    comps:["w7-brain-organization","w7-brain-development","w7-cerebrum-surface","w7-cortex-functional-areas","w7-white-matter-tracts","w7-basal-ganglia","w7-diencephalon","w7-cerebellum","w7-limbic-system","w7-circle-of-willis"] },
  { id:"neuro-brain-inferior", title:"Brain: Inferior View", unit:"Brain (Inferior View)", dir:"neuro-brain-inferior", frames:30,
    comps:["w7-brain-organization","w7-brain-development","w7-cerebrum-surface","w7-cortex-functional-areas","w7-white-matter-tracts","w7-basal-ganglia","w7-diencephalon","w7-cerebellum","w7-limbic-system","w7-circle-of-willis","w8-cranial-nerves"] },
  { id:"neuro-cranial-nerves", title:"Cranial Nerves", unit:"Cranial Nerves (I-XII)", dir:"neuro-cranial-nerves", frames:25,
    comps:["w8-cranial-nerves","w7-brainstem-regions","w7-midbrain","w7-pons","w7-medulla","w7-cranial-nerve-nuclei","w7-reticular-formation"] },
  { id:"spine", title:"Spinal Cord Loop", unit:"Spinal Cord & Spinal Nerves", dir:"spine", frames:94,
    comps:["w8-cord-external","w8-cord-roots","w8-cord-internal","w8-nerve-plexuses","w8-nerve-structure","w8-spinal-nerves-rami","w8-sensory-receptors"] },
];

/* Loops that give evidence for a competency. Returns [] for an
   unknown id rather than throwing. */
window.BIO004_LOOPS_FOR = function (competencyId) {
  return (window.BIO004_LOOPS || []).filter(function (l) {
    return l.comps.indexOf(competencyId) >= 0;
  });
};
