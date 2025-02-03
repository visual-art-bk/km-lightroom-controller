from pywinauto import WindowSpecification

def get_state_legacy(win_specs: WindowSpecification):
    current_state = win_specs.legacy_properties()["Value"]
    return current_state
    