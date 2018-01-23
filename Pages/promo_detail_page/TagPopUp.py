from utilities.BasePopUp import BasePopUp


class TagPopUp(BasePopUp):

    def __init__(self, driver):
        super(TagPopUp, self).__init__(driver, 'Tag')