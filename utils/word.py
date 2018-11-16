class Word():
    start_char = None
    end_char = None
    text = None
    token = None
    sentence = None
    pos = None

    gold_concept = None
    gold_text = None
    gold_id = None
    rel_id = None
    
    pred_tag = None

    def __init__(self):
        pass

    def __str__(self):
        string_representation = '{0}//({1}-{2})//{3}'.format(
            self.text, self.start_char, self.end_char, self.gold_concept
        )
        return string_representation
    
