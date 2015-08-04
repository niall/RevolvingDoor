from . import reg

@reg.route('/')
def reg_index():

    return "Reg Works"