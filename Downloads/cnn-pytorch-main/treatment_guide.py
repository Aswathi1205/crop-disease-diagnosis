"""
Treatment Guide Module

Provides educational treatment information for crop diseases.
Content is farmer-friendly and follows Indian agricultural context.
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class TreatmentGuide:
    """Treatment guide information for a specific disease"""
    disease_name: str
    overview: str
    prevention_tips: List[str]
    treatment_guidance: str
    advisory: str
    references: List[str]


# Treatment guide database
TREATMENT_GUIDES = {
    "bacterial_leaf_blight": TreatmentGuide(
        disease_name="Bacterial Leaf Blight",
        overview="Bacterial Leaf Blight is a serious bacterial disease of rice caused by Xanthomonas oryzae. It affects leaves, causing water-soaked lesions that turn yellow and eventually lead to leaf wilting and reduced grain yield.",
        prevention_tips=[
            "Use certified disease-free seeds from authorized sources",
            "Plant resistant rice varieties recommended for your region",
            "Maintain proper spacing between plants for good air circulation",
            "Avoid excessive nitrogen fertilization which promotes disease",
            "Practice crop rotation with non-host crops",
            "Remove and destroy infected plant debris after harvest",
            "Avoid overhead irrigation; use drip or furrow irrigation methods",
            "Monitor fields regularly, especially during monsoon season"
        ],
        treatment_guidance="""
**General Management Practices:**
- Remove and burn infected leaves and plants immediately to prevent spread
- Ensure balanced fertilization with emphasis on potassium
- Apply recommended bactericides approved by agricultural authorities at the first sign of infection
- Consider bio-control agents and organic treatments such as Pseudomonas fluorescens
- Maintain optimal water management; avoid water stress and flooding
- Use copper-based formulations as per local agricultural department recommendations

**Recommended Fertilizers:**
- **Potassium-rich fertilizers**: [Muriate of Potash (MOP)](https://www.iffco.in/en/products/muriate-of-potash-mop) or [Sulphate of Potash (SOP)](https://www.iffco.in/en/products)
- **Balanced NPK**: Apply NPK 20:20:20 or NPK 19:19:19 as per soil test recommendations
- **Micronutrients**: Zinc sulphate and [Ferrous sulphate](https://www.iffco.in/en/products) for deficiency correction

**Organic and Eco-friendly Options:**
- Application of [Trichoderma viride](https://www.iffco.in/en/products/bio-fertilizers) based bio-fungicides
- [Neem-based organic pesticides](https://www.neemfoundation.org/)
- Plant extracts like garlic or ginger solutions as preventive sprays
""",
        advisory="This information is for educational purposes only. Farmers are advised to consult local agricultural officers or agricultural universities before applying any treatment.",
        references=[
            "[Indian Council of Agricultural Research (ICAR) - Rice Knowledge Management Portal](http://www.rkmp.co.in/)",
            "[Tamil Nadu Agricultural University (TNAU) - Crop Protection Guidelines](https://agritech.tnau.ac.in/crop_protection/crop_prot_crop%20diseases_cereals_rice.html)"
        ]
    ),
    
    "brown_spot": TreatmentGuide(
        disease_name="Brown Spot",
        overview="Brown Spot is a fungal disease caused by Bipolaris oryzae (formerly Helminthosporium oryzae). It appears as oval brown spots on leaves and can significantly reduce grain quality and yield, especially in nutrient-deficient soils.",
        prevention_tips=[
            "Use healthy, certified seeds treated with recommended fungicides",
            "Ensure adequate soil fertility, especially potassium and silicon",
            "Avoid water stress during critical growth stages",
            "Maintain proper plant spacing for air circulation",
            "Practice balanced fertilization; avoid nitrogen excess",
            "Remove alternate host plants and crop residues",
            "Use resistant or tolerant rice varieties",
            "Implement proper water management to avoid drought stress"
        ],
        treatment_guidance="""
**General Management Practices:**
- Apply recommended fungicides approved by agricultural authorities at early disease stages
- Improve soil health through organic matter addition and balanced fertilization
- Ensure adequate potassium and silicon nutrition through soil amendments
- Use seed treatment with approved fungicides before sowing
- Spray protective fungicides during tillering and flowering stages

**Recommended Fertilizers:**
- **Potassium fertilizers**: [Muriate of Potash (MOP)](https://www.iffco.in/en/products/muriate-of-potash-mop) @ 50 kg/ha
- **Silicon sources**: Rice husk ash or [Calcium Silicate](https://www.iffco.in/en/products) @ 200-300 kg/ha
- **Balanced NPK**: NPK 4:2:1 ratio based on soil test
- **Organic manures**: [Vermicompost](https://www.iffco.in/en/products/bio-fertilizers) or well-decomposed FYM @ 5-10 tons/ha

**Organic and Eco-friendly Options:**
- Application of [Trichoderma viride](https://www.iffco.in/en/products/bio-fertilizers) or [Pseudomonas fluorescens](https://www.iffco.in/en/products/bio-fertilizers)
- Use of [neem oil](https://www.neemfoundation.org/) or neem-based products as preventive sprays
- Bordeaux mixture application as per recommended doses
- Proper composting and green manuring to improve soil health
- Bio-fortification with silicon-rich amendments like rice husk ash
""",
        advisory="This information is for educational purposes only. Farmers are advised to consult local agricultural officers or agricultural universities before applying any treatment.",
        references=[
            "[International Rice Research Institute (IRRI) - Rice Disease Management](http://www.knowledgebank.irri.org/training/fact-sheets/pest-management)",
            "[ICAR-Indian Institute of Rice Research - Disease Management Guidelines](https://icar-iirr.org/)"
        ]
    ),
    
    "leaf_scald": TreatmentGuide(
        disease_name="Leaf Scald",
        overview="Leaf Scald is a fungal disease caused by Microdochium oryzae (formerly Rhynchosporium oryzae). It produces characteristic scalded or bleached lesions on leaves, particularly in cool, humid conditions, affecting photosynthesis and grain filling.",
        prevention_tips=[
            "Plant resistant or tolerant rice varieties suitable for your area",
            "Use disease-free certified seeds",
            "Avoid dense planting; maintain recommended spacing",
            "Practice crop rotation with non-rice crops",
            "Remove and destroy infected plant debris",
            "Avoid excessive nitrogen application",
            "Ensure good field drainage to reduce humidity",
            "Monitor fields regularly during cool, humid weather"
        ],
        treatment_guidance="""
**General Management Practices:**
- Apply recommended fungicides approved by agricultural authorities when symptoms first appear
- Ensure balanced nutrition with adequate potassium
- Improve field drainage to reduce leaf wetness duration
- Remove severely infected plants to reduce disease spread
- Use foliar sprays of approved fungicides during vulnerable growth stages

**Recommended Fertilizers:**
- **Potassium fertilizers**: [Sulphate of Potash (SOP)](https://www.iffco.in/en/products) @ 40-50 kg/ha
- **Balanced NPK**: NPK 20:10:10 for better disease resistance
- **Micronutrients**: [Zinc sulphate](https://www.iffco.in/en/products) @ 25 kg/ha and Manganese sulphate @ 10 kg/ha
- **Organic sources**: [Neem cake](https://www.neemfoundation.org/) @ 200-250 kg/ha

**Organic and Eco-friendly Options:**
- Application of [Trichoderma harzianum](https://www.iffco.in/en/products/bio-fertilizers) based bio-fungicides
- Use of copper-based organic fungicides as per recommendations
- [Neem oil](https://www.neemfoundation.org/) or neem cake extracts as preventive measures
- Plant-based extracts such as garlic or turmeric solutions
- Maintain soil health through organic amendments and green manuring
- Use of bio-control agents like [Bacillus subtilis](https://www.iffco.in/en/products/bio-fertilizers)
""",
        advisory="This information is for educational purposes only. Farmers are advised to consult local agricultural officers or agricultural universities before applying any treatment.",
        references=[
            "[Food and Agriculture Organization (FAO) - Rice Disease Management](http://www.fao.org/agriculture/crops/core-themes/theme/pests/pm/)",
            "[ICAR - National Rice Research Institute (NRRI) - Disease Control](https://icar-nrri.in/)"
        ]
    )
}


def get_treatment_guide(disease_name: str) -> Optional[TreatmentGuide]:
    """
    Get treatment guide for a specific disease.
    
    Args:
        disease_name: Name of the disease (e.g., 'bacterial_leaf_blight')
        
    Returns:
        TreatmentGuide object if found, None otherwise
    """
    # Normalize disease name to lowercase and replace spaces with underscores
    normalized_name = disease_name.lower().replace(' ', '_').replace('-', '_')
    
    return TREATMENT_GUIDES.get(normalized_name)


def get_all_disease_names() -> List[str]:
    """
    Get list of all diseases with treatment guides.
    
    Returns:
        List of disease names
    """
    return list(TREATMENT_GUIDES.keys())
