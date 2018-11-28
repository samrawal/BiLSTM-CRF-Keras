class Word():
    start_char = None
    end_char = None
    text = None
    token = None
    sentence = None
    pos = None

    gold_concept = None
    iob_tag = None
    gold_text = None
    gold_id = None
    rel_id = None
    
    pred_tag = None

    def __init__(self):
        pass

    def get_concept_tag(self):
        if self.gold_concept != None:
            return '{0}-{1}'.format(self.iob_tag, self.gold_concept)
        else:
            self.iob_tag = 'O'
            return 'O'

    def __str__(self):
        string_representation = '{0}//({1}-{2})//{3}'.format(
            self.text, self.start_char, self.end_char, self.gold_concept
        )
        return string_representation

    # set the Word object as a padding token
    def set_as_pad_token(self):
        self.start_char = -1
        self.end_char = -1
        self.text = 'PADDING_TOKEN'
        self.gold_concept = 'X'
    
