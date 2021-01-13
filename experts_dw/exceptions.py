class ExpertsDwException(Exception):
    '''Base class for experts_dw exceptions.'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
