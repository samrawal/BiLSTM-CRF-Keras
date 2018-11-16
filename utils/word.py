class Word():
    text = None
    line = None
    token = None
    pos = None

    gold_tag = None
    gold_text = None
    rel_id = None
    
    pred_tag = None

    def __init__(self):
        pass
    def __str__(self):
        string_representation = '{0}//({1}-{2})//{3}'.format(
            self.text, self.start_char, self.end_char, self.gold_concept
        )
        return string_representation
    
