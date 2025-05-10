# label_mapper.py

def label_to_int(label):
    mapping = {
        "shoulder_risk": 0,
        "elbow_risk": 1,
        "safe": 2
    }
    return mapping[label]

def int_to_label(index):
    mapping = {
        0: "shoulder_risk",
        1: "elbow_risk",
        2: "safe"
    }
    return mapping[index]
