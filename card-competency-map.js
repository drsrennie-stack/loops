/* ============================================================
   BIO 004 Human Anatomy, Fall 2026
   card-competency-map.js

   THE BRIDGE BETWEEN THE CARDS AND MASTERY OS.

   THE PROBLEM THIS SOLVES
   -----------------------
   Mastery OS tracks competencies. The Spaced Recall app tracks
   cards. Nothing connected the two, so a student could answer
   every card in the bank and Mastery OS would still show zero
   mastery on everything.

   Three separate breaks, all confirmed in a browser:

     1. mastery-os-fall-2026.html loaded competenciesfall2026.js,
        which was not in the repo. A 404. window.BIO004_COMPETENCIES
        came back empty, so Mastery OS fell through to a generic
        "Week 1, Week 2" fallback and none of the 196 competencies
        ever appeared.

     2. Mastery OS read localStorage["bio004-progress"].
        bio004-spaced-recall.html writes localStorage["bio004-recall-v2"].
        Different keys. ingestRecall() bailed on its first line
        every single time.

     3. The 2,020 cards carry no competency id. Their fields are
        id, dok, q, a, options, correctIndex, explanation, tags,
        rubric. There was nothing for Mastery OS to match on.

   WHAT THIS FILE IS
   -----------------
   Recall stores progress as topics[topicId].cards[cardId], so the
   join happens at the TOPIC level, which is the level both sides
   actually share. Each of the 44 card topics maps to the
   competencies it provides evidence for.

   Coverage: 2,020 of 2,020 cards reach at least one competency.
   186 of 196 competencies are reachable by card.

   The 10 that are not are lab identification competencies, the
   upper extremity muscles, nerves and vessels and the head and
   neck lab muscles. Those are cadaver and specimen work. They are
   meant to be evidenced by "cadaver identification", not by
   multiple choice, so leaving them cardless is correct rather
   than a gap to fill.
   ============================================================ */

window.BIO004_CARD_COMPETENCY_MAP = {
  "t-anatomical-terminology": { title:"The Language of Anatomy", comps:["w1-levels-organization","w1-anatomical-position","w1-planes-sections","w1-directional-terms","w1-regional-terms"] },
  "t-body-cavities": { title:"Body Cavities and Regions", comps:["w1-body-cavities","w1-serous-membranes","w1-mediastinum","w1-peritoneum-relationships","w1-abdominopelvic-map"] },
  "t-cell-anatomy": { title:"Anatomy of the Cell", comps:["w1-generalized-cell","w1-plasma-membrane","w1-nucleus","w1-organelles"] },
  "t-tissues": { title:"Histology: The Four Tissue Types", comps:["w1-germ-layers","w1-epithelial-id","w1-cell-junctions","w1-connective-id","w1-muscle-tissue-id","w1-nervous-tissue-id","w1-body-membranes"] },
  "t-integumentary": { title:"The Integumentary System", comps:["w1-skin-layers","w1-epidermal-strata","w1-dermis-layers","w1-skin-accessory"] },
  "t-bone-histology": { title:"Bone Histology", comps:["w2-cartilage-types","w2-cartilage-growth","w2-bone-shapes","w2-long-bone-gross","w2-compact-spongy","w2-bone-cells","w2-ossification-growth"] },
  "t-axial-skeleton-skull": { title:"The Skull", comps:["w2-skull-bones","w2-skull-markings","w2-sutures-fontanelles","w2-skull-cavities","w2-skull-foramina"] },
  "t-axial-skeleton-spine": { title:"The Vertebral Column and Thoracic Cage", comps:["w2-spine-regions","w2-typical-vertebra","w2-regional-vertebrae","w2-thoracic-cage"] },
  "t-appendicular-skeleton-upper": { title:"The Upper Extremity", comps:["w2-pectoral-girdle","w2-arm-forearm","w2-hand-bones","w2-bone-markings-vocab"] },
  "t-appendicular-skeleton-lower": { title:"The Lower Extremity", comps:["w2-pelvic-girdle","w2-thigh-knee","w2-leg-bones","w2-foot-bones","w2-bone-markings-vocab"] },
  "t-articulations": { title:"Articulations and Joints", comps:["w2-joint-classification","w2-fibrous-cartilaginous","w2-synovial-structure","w2-joint-movements","w2-synovial-types","w2-shoulder-knee"] },
  "t-muscle-types": { title:"Muscle Tissue Types & Properties", comps:["w4-ct-coverings","w4-muscle-organization","w4-muscle-fiber-parts","w4-sarcomere","w4-myofilament-proteins","w4-muscle-tissue-types"] },
  "t-muscle-gross": { title:"Gross Anatomy, CT Sheaths & Attachments", comps:["w4-ct-coverings","w4-muscle-organization","w4-muscle-fiber-parts","w4-sarcomere","w4-myofilament-proteins","w4-muscle-tissue-types","w5-lab-abdominal-wall","w5-lab-thigh-gluteal","w5-lab-leg-muscles"] },
  "t-muscle-naming-mechanics": { title:"Naming, Levers & Coordination", comps:["w4-fascicle-patterns","w4-muscle-roles-naming","w4-lever-systems"] },
  "t-muscle-microanatomy": { title:"Fiber Microanatomy: SR, T-Tubules, Triad", comps:["w4-ct-coverings","w4-muscle-organization","w4-muscle-fiber-parts","w4-sarcomere","w4-myofilament-proteins","w4-muscle-tissue-types"] },
  "t-muscle-sarcomere": { title:"Sarcomere, Myofilaments & Proteins", comps:["w4-ct-coverings","w4-muscle-organization","w4-muscle-fiber-parts","w4-sarcomere","w4-myofilament-proteins","w4-muscle-tissue-types"] },
  "t-endocrine": { title:"Endocrine Anatomy", comps:["w6-endocrine-locate","w6-pituitary","w6-thyroid-parathyroid","w6-adrenal","w6-endocrine-tissue-organs"] },
  "t-blood-plasma": { title:"Blood Composition & Plasma", comps:["w4-blood-composition","w4-formed-elements","w4-hematopoiesis","w4-blood-disorders"] },
  "t-blood-erythrocytes": { title:"Erythrocytes, Hemoglobin & Iron", comps:["w4-blood-composition","w4-formed-elements","w4-hematopoiesis","w4-blood-disorders"] },
  "t-blood-hematopoiesis": { title:"Hematopoiesis & Erythropoiesis", comps:["w4-blood-composition","w4-formed-elements","w4-hematopoiesis","w4-blood-disorders"] },
  "t-blood-leukocytes": { title:"Leukocytes & Platelets", comps:["w4-blood-composition","w4-formed-elements","w4-hematopoiesis","w4-blood-disorders"] },
  "t-blood-groups-disorders": { title:"Blood Groups & Structural Disorders", comps:["w4-blood-composition","w4-formed-elements","w4-hematopoiesis","w4-blood-disorders"] },
  "t-heart": { title:"The Heart", comps:["cv-surfaces","cv-chambers","cv-valves","cv-valve-support","cv-cardiac-muscle","cv-blood-pathway","bvn-great-vessels","cv-coronary","cv-conduction-anat","cv-cardiac-nerves","bvn-vessel-tunics","bvn-vessel-types","bvn-artery-cap-vein-kinds","bvn-circulatory-routes","bvn-vessel-disorders","bvn-fetal-remnants"] },
  "t-cardiac-conduction": { title:"The Cardiac Conduction System", comps:["cv-surfaces","cv-chambers","cv-valves","cv-valve-support","cv-cardiac-muscle","cv-blood-pathway","bvn-great-vessels","cv-coronary","cv-conduction-anat","cv-cardiac-nerves","bvn-vessel-tunics","bvn-vessel-types","bvn-artery-cap-vein-kinds","bvn-circulatory-routes","bvn-vessel-disorders","bvn-fetal-remnants"] },
  "t-blood-vessels": { title:"Blood Vessels, Structure and Types", comps:["cv-surfaces","cv-chambers","cv-valves","cv-valve-support","cv-cardiac-muscle","cv-blood-pathway","bvn-great-vessels","cv-coronary","cv-conduction-anat","cv-cardiac-nerves","bvn-vessel-tunics","bvn-vessel-types","bvn-artery-cap-vein-kinds","bvn-circulatory-routes","bvn-vessel-disorders","bvn-fetal-remnants","w4-lab-ue-arteries-veins"] },
  "t-blood-vessel-disorders": { title:"Blood Vessel Disorders and Fetal Circulation", comps:["cv-surfaces","cv-chambers","cv-valves","cv-valve-support","cv-cardiac-muscle","cv-blood-pathway","bvn-great-vessels","cv-coronary","cv-conduction-anat","cv-cardiac-nerves","bvn-vessel-tunics","bvn-vessel-types","bvn-artery-cap-vein-kinds","bvn-circulatory-routes","bvn-vessel-disorders","bvn-fetal-remnants"] },
  "t-lymph-overview-vessels": { title:"Overview, Lymph, Capillaries & Vessels", comps:["w4-lymph-pathway","w4-lymph-vessels-node","w4-lymphatic-organs","w4-lymphatic-disorders"] },
  "t-lymph-trunks-ducts": { title:"Trunks, Ducts & Lymph Transport", comps:["w4-lymph-pathway","w4-lymph-vessels-node","w4-lymphatic-organs","w4-lymphatic-disorders"] },
  "t-lymph-primary-organs": { title:"Primary Organs: Red Marrow & Thymus", comps:["w4-lymph-pathway","w4-lymph-vessels-node","w4-lymphatic-organs","w4-lymphatic-disorders"] },
  "t-lymph-nodes-spleen": { title:"Lymph Nodes & Spleen", comps:["w4-lymph-pathway","w4-lymph-vessels-node","w4-lymphatic-organs","w4-lymphatic-disorders"] },
  "t-lymph-malt-tonsils": { title:"MALT & Tonsils", comps:["w4-lymph-pathway","w4-lymph-vessels-node","w4-lymphatic-organs","w4-lymphatic-disorders"] },
  "t-respiratory": { title:"The Respiratory System", comps:["resp-zones","resp-upper-tract","resp-larynx","resp-tree","resp-lungs-pleura","resp-histo","resp-thoracic-diaphragm","resp-disorders"] },
  "t-alimentary-canal": { title:"The Alimentary Canal", comps:["w5-canal-wall","w5-enteric-plexuses","w5-peritoneum-folds","w5-retroperitoneal","w5-mouth-pharynx-esophagus","w5-canal-sphincters","w5-stomach","w5-small-intestine","w5-large-intestine","w5-food-pathway","w5-canal-disorders"] },
  "t-accessory-digestive-organs": { title:"Accessory Organs of Digestion", comps:["w5-teeth-tongue","w5-salivary-glands","w5-liver-gross-lobule","w5-bile-path","w5-pancreas","w5-accessory-disorders"] },
  "t-urinary-system": { title:"The Urinary System", comps:["w6-kidney-gross","w6-kidney-internal","w6-nephron-parts","w6-nephron-types","w6-jga-filtration","w6-kidney-bloodsupply","w6-urine-path","w6-urinary-disorders"] },
  "t-reproductive-male": { title:"The Male Reproductive System", comps:["w6-scrotum-testes","w6-sperm-path","w6-sperm-cell","w6-male-glands-penis","w6-male-disorders"] },
  "t-reproductive-female": { title:"The Female Reproductive System", comps:["w6-ovary","w6-ovum-path","w6-uterus","w6-vagina-vulva","w6-mammary"] },
  "t-pregnancy-and-birth": { title:"Pregnancy and Birth", comps:["w6-fertilization-implant","w6-placenta-membranes","w6-gravid-labor"] },
  "t-nervous-tissue": { title:"Functional Organization and Nervous Tissue", comps:["w8-ns-organization","w8-neuron-parts","w8-synapse-parts","w8-neuron-classification","w8-neuroglia","w8-myelination"] },
  "t-neuronal-integration": { title:"Gross Anatomy and Neuronal Integration", comps:["w8-tissue-collections","w8-gray-white-matter","w8-reflex-arc","w8-reflex-types","w8-neuronal-pools"] },
  "t-cns-brain-spinal-cord": { title:"CNS: The Brain and Spinal Cord", comps:["w7-brain-organization","w7-brain-development","w7-cerebrum-surface","w7-cortex-functional-areas","w7-white-matter-tracts","w7-basal-ganglia","w7-diencephalon","w7-cerebellum","w7-limbic-system","w7-circle-of-willis","w8-cord-external","w8-cord-roots","w8-cord-internal","w7-brainstem-regions","w7-midbrain","w7-pons","w7-medulla","w7-cranial-nerve-nuclei","w7-reticular-formation"] },
  "t-cns-meninges-csf": { title:"CNS Meninges and CSF", comps:["w7-cranial-meninges","w7-spinal-meninges-spaces","w7-cord-termination-lp","w7-ventricles","w7-csf-circulation","w7-bbb"] },
  "t-pns": { title:"The Peripheral Nervous System", comps:["w8-nerve-structure","w8-spinal-nerves-rami","w8-sensory-receptors","w8-cranial-nerves","w8-nerve-plexuses"] },
  "t-ans": { title:"The Autonomic Nervous System", comps:["w8-ans-pathway","w8-ans-ganglia-divisions"] },
};
