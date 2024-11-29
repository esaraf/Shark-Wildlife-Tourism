# A dictionary that maps question ids to question types 


question_type_mapping = {
    "Likert_Type_1": [ # Frequency Based
        "1_1A",
        "1_1B",
        "1_1C",
        "1_1D",
        "1_2A",
        "1_2B",
        "1_2C",
        "1_2D"
    ], 
    
    "Likert_Type_2":[ # Agreement Based
        "2_3A",
        "2_3B",
        "2_3C",
        "2_3D",
        "2_3E",
        "2_3F",
        "2_4A",
        "2_4B",
        "2_4C",
        "2_4D",
        "2_4E",
        "2_4F",
        "2_4G",
        "4_1A",
        "4_2A",
        "4_3A",
        "4_4A",
        "4_5A",
        "4_6A"
    ], 

    "MC":[ # Multiple Choice.... TO DO: Map MC QIDs to specific MC answers
        "1_3C",
        "3_1A",
        "3_2A",
        "3_3A",
        "3_4A",
        "3_5A",
        "3_6A",
        "3_7A"
    ],

    "Polar":[ # Yes / No
        "1_3A",
        "1_4A",
        "3_7A"
    ],

    "Scale":[ # 1 to 10 
        "2_1A",
        "2_2A",
        "2_2B",
        "2_2C",
        "2_2D",
        "2_1B",
        "2_1C"
    ],

    "OPE":[ # Open Ended 
        "1_1E",
        "1_2E",
        "1_3D",
        "1_3B",
        "2_1D",
        "2_2E",
        "5_1A",
        "5_2A",
        "5_3A",
        "5_4A"
    ],

    "ID":[ # Internal Survey ID
        "0_0A"
    ]
}